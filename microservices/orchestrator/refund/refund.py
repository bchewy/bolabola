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
    1. receives ticket and user information from frontend
    2. calls billing service for refund
    3. receives a status from billing service, success/failure
    4. if success, send ticket information to RabbitMQ to update db

    Sends the following JSON payload to the billing service:
    {
        "user_id": "1234",
        "match_id": "5678",
        "payment_intent": "pi_1NirD82eZvKYlo2CIvbtLWuY"
    }

    Receives the following JSON payload from the billing service:
    {
        "status": "succeeded",
        "message": "Refund successful",
        "data": {
            "user_id": "1234",
            "match_id": "5678",
            "payment_intent": "pi_1NirD82eZvKYlo2CIvbtLWuY"
        }
    }

    Sends the following JSON payload to the RabbitMQ:
    {
        "user_id": "1234",
        "match_id": "5678",
        "payment_intent": "pi_1NirD82eZvKYlo2CIvbtLWuY"
    }
    """
    # 1. receive ticket and user information from frontend
    data = request.json

    # 2. call billing service for refund
    billing_service_url = "http://kong:8000/api/v1/billing/refund"
    response = requests.post(billing_service_url, json=data)

    # 3. receive a status from billing service, success/failure
    if response.status_code != 200:
        return jsonify({"message": "Failed to initiate refund"}), 500
    
    try: 
        # 4. if success, send refund information to RabbitMQ to update db
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        channel.exchange_declare(exchange='refund', exchange_type='direct', durable=True)

        channel.queue_declare(queue='user', durable=True) # for the user service

        channel.queue_declare(queue='match', durable=True) # for the match service

        # Set up the refund information to be sent
        msg = json.dumps(response.json())

        channel.basic_publish(
            exchange='refund',
            routing_key='refund.user',
            body=msg,
            properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
        )

        connection.close()
        return jsonify({"message": "Refund initiated successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to initiate refund"}), 500

if __name__ == '__main__':
    app.run(port=9103, debug=True, host="0.0.0.0")
