from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
from threading import Thread
import requests

MATCH_URL = "http://kong:8000/api/v1/match"
SEAT_URL = "http://kong:8000/api/v1/seat"
BILLING_URL = "http://kong:8000/api/v1/billing"


####### RabbitMQ  #######
def start_rabbitmq_consumer():
    def callback(ch, method, properties, body):
        pass

    credentials = pika.PlainCredentials("ticketboost", "veryS3ecureP@ssword")
    parameters = pika.ConnectionParameters("rabbitmq", 5672, "/", credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue="match", durable=True)
    channel.basic_consume(queue="match", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def run_consumer_thread():
    consumer_thread = Thread(target=start_rabbitmq_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Publish to AMQP - to update subsequent services about the match booking
def publish_to_amqp():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    # Publish to user to update match booking
    channel.queue_declare(queue="user")
    channel.basic_publish(
        exchange="",
        routing_key="user",
        body="User has purchased ticket for match with id {123} !",
    )

    # Publish to Match Queue to update ticket availablity
    channel.queue_declare(queue="match")
    channel.basic_publish(
        exchange="", routing_key="match", body="Match with id {123} has been booked!"
    )

    # Publish to seat reservation to remove ticket lock
    channel.queue_declare(queue="seat")
    channel.basic_publish(
        exchange="", routing_key="seat", body="Seat with id {123} has been booked!"
    )

    # Publish to notification
    channel.queue_declare(queue="notification")
    channel.basic_publish(
        exchange="",
        routing_key="notification",
        body="Notification for match with id {123} has been sent!",
    )

    connection.close()

# HANDLE SELECT SEAT AND QUANTITY FLOW
@app.route("/init-match-booking/<match_id>", methods=["GET"])
def init_match_booking(match_id):

    readyToPay = False
    # get userid
    user_id = request.args.get("userid")
    ticket_category = request.args.get("cat")

    # Retrieve match details
    match_details = retrieve_match_from_match_service(match_id)
    match_details["match_id"] = match_id
    # Retrieve ticket availability
    seatCount = match_details["seats"]
    if seatCount == 0:
        return jsonify(
            {"message": "No seats available for this match!"}
        )  # Return to frontend if unavailable.
    else:
        # TODO: Add minus seat count for the selected seat from Match Service
        response, locked = reserve_seat_for_user(match_id, user_id, ticket_category)

        readyToPay = True  # Upon readyToPay being true, frontend should progress to match checkout UI.
    return (response, locked, readyToPay)
    # return jsonify(match_details, {"seatCount": seatCount})


# app.route("/continue-match-booking/<match_id>", methods=["GET"])

def continue_match_booking(match_id, user_id, ticket_category):
    # TODO: Call billing service to send billing/purchase details, and wait for response
    """
    This method should send the billing details to the billing service. An example of the payload of billing details is:
    {
        "match_id": "1234",
        "match_name": "Arsenal vs Chelsea",
        "tickets": [
            {"category": "A", "quantity": 2},
            {"category": "B", "quantity": 3},
            {"category": "C", "quantity": 4},
        ],
        "user_id": "123"
    }
    """
    payload = { # hardcoded now, but should be dynamic
        "match_id": match_id,
        "match_name": "Arsenal vs Chelsea",
        "tickets": [
            {"category": "A", "quantity": 2},
            {"category": "B", "quantity": 3},
            {"category": "C", "quantity": 4},
        ],
        "user_id": user_id,
    }
    
    # Send to billing service to create a checkout session
    response = requests.post(BILLING_URL + "/checkout", json=payload)

    # Check if the checkout_session was created successfully
    if response["code"] == 200:
        checkout_session = response["checkout_session"]
        return jsonify({"checkout_session": checkout_session})
    else:
        return jsonify({"error": "Unable to create checkout session."}) 

# Receive the transaction status from billing service
@app.route("/process-webhook", methods=["POST"])
def process_webhook():
    """
    This method receives a POST request from the billing service.
    If the status is "success", it publishes the match and user data to the RabbitMQ queue.
    Sample payload sent over by billing microservice:
    payload = {
            "status": "success",
            "payment_intent": "pi_3OvDsfF4chEmCmGg1efgabcI,
    }
    """
    data = request.json
    print("The Match Booking orcha received the following from billing service: ")
    print(data)
    ############################################################################################################
    ############################################################################################################
    # may be need to get other match booking detials from other services before sending over to the RabbitMQ
    ############################################################################################################
    ############################################################################################################
    # if data["status"] == "success":
    #     print("Publishing to RabbitMQ")
    #     publish_to_amqp()
    return jsonify({"message": "Match booking successful!"})


def retrieve_match_from_match_service(match_id):
    url = MATCH_URL

    query = """
    query GetMatchDetails($id: String) {
        match_details(_id: $id) {
            _id
            name
            description
            venue
            home_team
            away_team
            home_score
            away_score
            date
            seats
        }
    }
    """

    variables = {"id": match_id}
    headers = {"Content-Type": "application/json"}
    payload = {"query": query, "variables": variables}
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        match_details = response_json.get("data", {}).get("match_details")
        return match_details
    else:
        raise Exception(
            f"Query failed to run with a status code {response.status_code}. {response.text}"
        )


def reserve_seat_for_user(match_id, user_id, ticket_category):
    # returns response.json and boolean value for if successful or not
    payload = {
        "user_id": user_id,
        "match_id": match_id,
        "ticket_category": ticket_category,
    }
    response = requests.post(SEAT_URL + "/reserve", json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Seat reservation was successful
        return response.json(), True
    elif response.status_code == 409:
        # Seat is currently on hold
        return response.json(), False
    elif response.status_code == 404:
        # No available seats
        return response.json(), False
    else:
        # Other errors
        return {"error": "An unexpected error occurred."}, False


@app.route("/")
def hello():
    return "Match Booking orcha is alive!"


# def consume_message(channel, method, properties, body):
#     # Process the consumed message here
#     print("Received message:", body.decode())

# def start_consuming():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()
#     channel.queue_declare(queue='my_queue')
#     channel.basic_consume(queue='my_queue', on_message_callback=consume_message, auto_ack=True)
#     channel.start_consuming()

if __name__ == "__main__":
    app.run(port=9101, debug=True, host="0.0.0.0")
