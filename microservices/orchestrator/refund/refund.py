from flask import Flask, request, jsonify
import pika
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

MATCH_URL = "http://kong:8000/api/v1/match"

# Hardcoded credentials and connection details for RabbitMQ
rabbitmq_user = "ticketboost"
rabbitmq_password = "veryS3ecureP@ssword"
rabbitmq_host = "rabbitmq"  # Name of the RabbitMQ service in Docker Compose
rabbitmq_port = 5672
rabbitmq_vhost = "/"

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host=rabbitmq_vhost,
    credentials=credentials,
)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Pong!"})

@app.route('/initiate-refund', methods=['POST'])
def refund():
    """
    1.1. receives ticket and user information from frontend
    1.2. call the user service to get the payment_intent
    2. calls billing service for refund
    3. receives a status from billing service, success/failure
    4. if success, send ticket information to RabbitMQ to update db

    SAMPLE PAYLOAD FORMAT FROM FRONTEND
    {
        "user_id": "1234",
        "ticket_info": {
            "match_id": "5678",
            "category": "A",
            "quantity": 2,
            "ticket_ids": "123,456"
            },
        "email": "example@example.com"
    }

    Sends the following JSON payload to the billing service:
    {
        "user_id": "1234",
        "match_id": "5678",
        "category": "A",
        "quantity": 2,
        "payment_intent": "pi_1NirD82eZvKYlo2CIvbtLWuY",
        "email": "example@example.com"
    }

    Receives the following JSON payload from the billing service:
    {
        "status": "succeeded",
        "message": "Refund successful",
        "metadata": {
            "user_id": "1234",
            "match_id": "5678",
            "category": "A",
            "quantity": 2,
            "payment_intent": "pi_1NirD82eZvKYlo2CIvbtLWuY",
            "ticket_ids": "123,456",
            "email": "example@example.com"
        },
    }
    """
    # 1.1. receive ticket and user information from frontend
    data_from_frontend = request.json
    print("Data from frontend")
    print(data_from_frontend)

    # 1.2. call the user service to get the payment_intent
    user_id = data_from_frontend["user_id"]
    match_id = data_from_frontend["ticket_info"]["match_id"]
    category = data_from_frontend["ticket_info"]["ticket_category"]
    quantity = data_from_frontend["ticket_info"]["quantity"]
    ticket_ids = data_from_frontend["ticket_info"]["ticket_ids"]
    email = data_from_frontend["email"]

    user_service_url = f"http://kong:8000/api/v1/user/{user_id}/tickets/match/{match_id}"

    response = requests.get(user_service_url)
    print(response.json())
    payment_intent = response.json()["data"]["payment_intent"]

    # 2. call billing service for refund
    billing_service_refund_url = "http://kong:8000/api/v1/billing/refund"
    data_for_sending = {
        "user_id": user_id,
        "match_id": match_id,
        "category": category,
        "quantity": quantity,
        "ticket_ids": ticket_ids, 
        "payment_intent": payment_intent,
        "email": email,
    }
    response = requests.post(billing_service_refund_url, json=data_for_sending)
    print(response.json()["data"])

    # 3. receive a status from billing service about the refund, success/failure
    if response.json()["data"]["status"] == "failed":
        return jsonify({"message": "Failed to initiate refund"}), 500
    if response.json()["data"]["status"] == "succeeded":
        # 4. if success, send ticket information to RabbitMQ to update db
        publish_to_amqp(response.json()["data"])
        print("Messages sent to refund queues")
        return jsonify({"message": "Refund initiated successfully"}), 200
    else:
        return jsonify({"message": "Failed to initiate refund"}), 500

def retrive_match_from_match_service(match_id):
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

def publish_to_amqp(data):
    rabbitmq_url = "amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/"
    parameters = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()  

    user_id = data["metadata"]["user_id"]
    match_id = data["metadata"]["match_id"]
    payment_intent = data["payment_intent"]
    category = data["metadata"]["category"]
    quantity = data["metadata"]["quantity"]
    ticket_ids = data["metadata"]["ticket_ids"]
    email = data["metadata"]["email"]


    # Publish to user to remove ticket from user account
    user_message = {"user_id":user_id, "match_id":match_id, "payment_intent":payment_intent, "category":category, "quantity":quantity} 
    channel.basic_publish(
        exchange="refunds",
        routing_key="refunds.user",
        body=json.dumps(user_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to match to update available tickets
    match_message = {"match_id":match_id, "quantity":quantity} 
    channel.basic_publish(
        exchange="refunds",
        routing_key="refunds.match",
        body=json.dumps(match_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to seat to remove the seat from tickets  
    seat_message = {"ticket_ids": ticket_ids} 
    channel.basic_publish(
        exchange="refunds",
        routing_key="refunds.seat",
        body=json.dumps(seat_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to notification to send email to user
    notification_message = {
                                "user_id": user_id, 
                                "match": retrive_match_from_match_service(match_id), 
                                "category": category, 
                                "quantity": quantity, 
                                "payment_intent": payment_intent,
                                "email": email
                            }
    channel.basic_publish(
        exchange="refunds",
        routing_key="refunds.notification",
        body=json.dumps(notification_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    connection.close()

if __name__ == '__main__':
    app.run(port=9103, debug=True, host="0.0.0.0")
