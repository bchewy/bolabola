from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
from threading import Thread
import requests
import json
from prometheus_flask_exporter import PrometheusMetrics


MATCH_URL = "http://kong:8000/api/v1/match"
SEAT_URL = "http://kong:8000/api/v1/seat"
BILLING_URL = "http://kong:8000/api/v1/billing"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
metrics = PrometheusMetrics(app)

# Metrics:
match_booking_attempts = metrics.counter(
    "match_booking_attempts",
    "Number of attempts to book a match",
    labels={"outcome": None},
)


# Publish to AMQP - to update subsequent services about the match booking
def publish_to_amqp(data):
    rabbitmq_url = "amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/"
    parameters = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    match_booking_attempts.labels(outcome=True).inc()

    # Publish to user to update match booking - DONE
    category = ""
    if data["metadata"]["A"] != "0":
        category = "A"
    elif data["metadata"]["B"] != "0":
        category = "B"
    elif data["metadata"]["C"] != "0":
        category = "C"
    quantity = (
        int(data["metadata"]["A"])
        + int(data["metadata"]["B"])
        + int(data["metadata"]["C"])
    )
    user_message = {
        "user_id": data["metadata"]["user_id"],
        "match_id": data["metadata"]["match_id"],
        "category": category,
        "ticket_ids": data["metadata"]["ticket_ids"],
        "payment_intent": data["payment_intent"],
        "quantity": quantity,
    }
    channel.basic_publish(
        exchange="booking",
        routing_key="booking.user",
        body=json.dumps(user_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to Match Queue to update ticket availablity - DONE
    match_message = {"match_id": data["metadata"]["match_id"], "quantity": quantity}
    channel.basic_publish(
        exchange="booking",
        routing_key="booking.match",
        body=json.dumps(match_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to seat reservation to remove ticket lock - DONE
    seat_message = {
        "user_id": data["metadata"]["user_id"],
        "ticket_ids": data["metadata"]["ticket_ids"],
    }
    channel.basic_publish(
        exchange="booking",
        routing_key="booking.seat",
        body=json.dumps(seat_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to notification - DONE
    notification_message = {
        "user_id": data["metadata"]["user_id"],
        "email": data["metadata"]["email"],  # Assuming email is part of the metadata
        "match": retrieve_match_from_match_service(data["metadata"]["match_id"]),
        "quantity": quantity,
    }
    channel.basic_publish(
        exchange="booking",
        routing_key="booking.notification",
        body=json.dumps(notification_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    connection.close()


def publish_fail_msg(data):
    rabbitmq_url = "amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/"
    parameters = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Publish to notification
    notification_message = {
        "user_id": data["metadata"]["user_id"],
        "email": data["metadata"]["email"],  # Assuming email is part of the metadata
        "match_id": data["metadata"]["match_id"],
        "message": "Your ticket has been unreserved. Please try to book a new ticket again",
    }
    channel.basic_publish(
        exchange="booking",
        routing_key="booking.notification",
        body=json.dumps(notification_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to seat reservation to remove ticket lock and remove userid from the seat
    seat_message = {
        "user_id": data["metadata"]["user_id"],
        "ticket_ids": data["metadata"]["ticket_ids"],
    }
    channel.basic_publish(
        exchange="booking",
        routing_key="booking.seat_fail",
        body=json.dumps(seat_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    connection.close()


# RETURNS AVAILABLE TICKETS
@app.route("/availabletickets/<match_id>", methods=["GET"])
def get_available_tickets(match_id):
    availableticket = ""
    response = requests.get(SEAT_URL + "/availabletickets/" + match_id)
    availableticket = response.json()
    print(
        "Retrieving available tickets, for the match id {}, available tickets: {}".format(
            match_id, availableticket
        )
    )
    return jsonify(availableticket)


# HANDLE SELECT SEAT AND QUANTITY FLOW
# THIS CALL SHOULD ONLY HAPPEN IN THE VIEWS/CHECKOUT PAGE
@app.route("/init-match-booking/<match_id>", methods=["POST"])
def init_match_booking(match_id):

    # RETRIEVE THE USER ID, TICKET CATEGORY AND QUANTITY FROM THE FRONTEND
    user_id = request.json.get("user_id")
    email = request.json.get("email")
    ticket_category = request.json.get("category")
    seatUserPurchasing = request.json.get("quantity")

    # Retrieve match details
    match_details = retrieve_match_from_match_service(match_id)
    if match_details is None:
        return jsonify({"error": "Match details not found!"})
    print("=====================================")
    print("Match Details here: ", match_details)
    print("=====================================")

    # Check ticket availability - from seat service # we will use frontend, no logic here as
    # we will always assume that the seats are available as long as the user has gone in here.
    # Depending on the quantity, the user can reserve 4 seats.

    # =====================RESERVE PORTION ========
    # by right - all

    # Reserve the seat
    reserve_seat_payload = {
        "user_id": user_id,
        "match_id": match_id,
        "category": ticket_category,
        "quantity": seatUserPurchasing,  # Assuming this is the seat number, though it's named as quantity
    }
    reserve_seat_response = requests.post(
        SEAT_URL + "/reserve", json=reserve_seat_payload
    )

    print("=============== RESULTS OF RESERVATION ===============")
    print(reserve_seat_response.json())
    print("======================================================")
    if reserve_seat_response.status_code != 200:
        return (
            jsonify({"error": "Seats have already been reserved"}),
            reserve_seat_response.status_code,
        )

    # print("Debug log for seat reservation:", reserve_seat_response.json())
    # # Check if reservation was successful
    # if reserve_seat_response.status_code != 200:
    #     return (
    #         jsonify({"error": "Failed to reserve seat"}),
    #         reserve_seat_response.status_code,
    #     )

    # ============ BILLING PORTION ============

    # once lock - call billing
    # Send to billing service to create a checkout session
    payload_to_billing = {
        "match_id": match_id,
        "match_name": match_details["name"],
        "tickets": [{"category": ticket_category, "quantity": seatUserPurchasing}],
        "user_id": user_id,
        "ticket_ids": reserve_seat_response.json()["ticket_ids"],
        "email": email,
    }
    response = requests.post(BILLING_URL + "/checkout", json=payload_to_billing)

    print("Response from billing service: ", response.json())
    # Check if the checkout_session was created successfully
    # Response object is not subscriptiable, but retrieve the checkout url
    checkout_url = response.json()["checkout_session"]["url"]
    if checkout_url:
        return checkout_url
    else:
        return jsonify({"error": "Seomthing went wrong."})


# Receive the transaction status from billing service
@app.route("/process-webhook", methods=["POST"])
def process_webhook():
    """
    This method receives a POST request from the billing service.
    If the status is "success", it publishes the match and user data to the RabbitMQ queue.
    Sample payload sent over by billing microservice:


    Sample payload received from billing microservice:
    {
        'status': 'complete',
        'payment_intent': 'pi_3OxQrhF4chEmCmGg0DaRyjoU',
        'metadata': {
                'user_id': '106225716514519006902',
                'email': 'example@example.com',
                'A': '0',
                'B': '0'
                'C': '2',
                'match_id': '65fe9fb32082209e71e8f34a',
                'ticket_ids': '1',
            }
    }
    """
    data = request.json
    print("The Match Booking orcha received the following from billing service: ")
    print(data)

    if data["status"] == "complete":

        # Publish to RabbitMQ
        # data here should be about match and shit
        publish_to_amqp(data)

        return jsonify({"message": "Match booking info sent to AMQP"})


# User does not pay in time
@app.route("/fail-booking", methods=["POST"])
def failed_booking():
    """
    This method receives a POST request from the billing service in the event the user fails to pay in 5 minutes.

    Sample payload received from billing microservice:
    {
        'status': 'cancelled',
        'metadata': {
                'user_id': '106225716514519006902',
                'email': 'example@example.com',
                'match_id': '65fe9fb32082209e71e8f34a',
                'ticket_ids': '1'
            }
    }
    """
    data = request.json
    print(
        "The Match Booking orcha FAIL BILLING received the following from billing service: "
    )
    print(data)

    # Publish to RabbitMQ
    if data["status"] == "expired":
        # send a message to the frontend to inform the user that the payment link has expired
        publish_fail_msg(data)
        return jsonify({"message": "Payment link expired!"})

    elif data["status"] == "cancelled":
        # send a message to the frontend to inform the user that the payment link has been cancelled
        publish_fail_msg(data)
        return jsonify({"message": "Payment link cancelled!"})

    else:
        publish_fail_msg(data)
        return jsonify({"error": "Unexpected status received."})


def retrieve_match_from_match_service(match_id):
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
    response = requests.post(MATCH_URL, headers=headers, json=payload)

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
