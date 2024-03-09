from flask import Flask, request, jsonify
import pika
import requests

app = Flask(__name__)

@app.route('/api/v1/refund/initiate-refund', methods=['POST'])
def refund():
    """
    1. receives ticket information from frontend
    2. calls billing service for refund
    3. receives a status from billing service, success/failure
    4. if success, send ticket information to RabbitMQ to update db
    """
    # 1. receive ticket information from frontend
    ticket = request.json
    # end of 1

    # 2. call billing service for refund
    billing_service_url = "http://billing:9003/api/v1/billing/refund"

    response = requests.post(billing_service_url, json=ticket)
    status = response.json()['status']
    # end of 2

    # 3. receive a status from billing service, success/failure
    if status == "succeeded":
        # 4. if success, send ticket information to RabbitMQ to update db
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='refund')

        channel.basic_publish(exchange='', routing_key='refund', body=jsonify(ticket))
        connection.close()
        return jsonify({"message": "Refund initiated successfully"}), 200
    else:
        return jsonify({"message": "Refund failed"}), 500

if __name__ == '__main__':
    app.run(port=9103)
