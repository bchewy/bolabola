from flask import Flask, request, jsonify
import pika
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
            "serial_no": "123456"
            }
    }

    Sends the following JSON payload to the billing service:
    {
        "user_id": "1234",
        "match_id": "5678",
        "category": "A",
        "quantity": 2,
        "payment_intent": "pi_1NirD82eZvKYlo2CIvbtLWuY"
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
            "serial_no": "123456"
        }
    }
    """
    # 1.1. receive ticket and user information from frontend
    data_from_frontend = request.json

    # 1.2. call the user service to get the payment_intent
    user_id = data_from_frontend["user_id"]
    match_id = data_from_frontend["ticket_info"]["match_id"]
    category = data_from_frontend["ticket_info"]["ticket_category"]
    quantity = data_from_frontend["ticket_info"]["quantity"]
    serial_no = data_from_frontend["ticket_info"]["serial_no"]

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
        "serial_no": serial_no, 
        "payment_intent": payment_intent
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

def publish_to_amqp(data):
    rabbitmq_url = "amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/"
    parameters = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()  

    # NOT TESTED: Extract the necessary data from the response
    user_id = data["metadata"]["user_id"]
    match_id = data["metadata"]["match_id"]
    payment_intent = data["payment_intent"]
    category = data["metadata"]["category"]
    quantity = data["metadata"]["quantity"]
    serial_no = data["metadata"]["serial_no"]

    # Publish to user to remove ticket from user account
    user_message = {"user_id":user_id, "match_id":match_id, "payment_intent":payment_intent, "category":category, "quantity":quantity} # doing this half awake so need to verify thanks
    channel.basic_publish(
        exchange="refunds",
        routing_key="refunds.user",
        body=json.dumps(user_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to match to update available tickets
    match_message = {"match_id":match_id, "quantity":quantity} # doing this half awake so need to verify thanks
    channel.basic_publish(
        exchange="refunds",
        routing_key="refunds.match",
        body=json.dumps(match_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    # Publish to seat to remove the seat from tickets  
    seat_message = {"serial_no": serial_no} # doing this half awake so need to verify thanks
    channel.basic_publish(
        exchange="refunds",
        routing_key="refunds.seat",
        body=json.dumps(seat_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )

    connection.close()

if __name__ == '__main__':
    app.run(port=9103, debug=True, host="0.0.0.0")
