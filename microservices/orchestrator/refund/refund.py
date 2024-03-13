from flask import Flask, request, jsonify
import pika
import requests
import json

app = Flask(__name__)

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

@app.route('/initiate-refund', methods=['POST'])
def refund():
    """
    1. receives ticket and user information from frontend
    2. calls billing service for refund
    3. receives a status from billing service, success/failure
    4. if success, send ticket information to RabbitMQ to update db
    """
    # 1. receive ticket and user information from frontend
    data = request.json

    # 2. call billing service for refund
    billing_service_url = "http://kong:8000/api/v1/billing/refund"

    response = requests.post(billing_service_url, json=data)
    status = response.json()['status']

    # 3. receive a status from billing service, success/failure
    if status == "succeeded":
        try: 
            # 4. if success, send ticket information to RabbitMQ to update db
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()

            channel.exchange_declare(exchange='refund', exchange_type='direct', durable=True)

            channel.queue_declare(queue='user', durable=True) # for the user service

            channel.queue_declare(queue='match', durable=True) # for the match service

            # Set up the message to be sent
            msg = json.dumps(data)  # convert the data to a string to send as message

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
    else:
        return jsonify({"message": "Refund failed"}), 500

if __name__ == '__main__':
    app.run(port=9103)
