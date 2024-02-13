import pika
import requests
from flask import Flask, request

# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_QUEUE = "notifications"

# AWS SES API endpoint
SES_API_URL = "https://email.us-west-2.amazonaws.com"

app = Flask(__name__)


@app.route("/notifications", methods=["POST"])
def send_notification():
    data = request.get_json()
    recipient = data.get("recipient")
    message = data.get("message")

    # Maybe add sms here?
    send_email(message)

    return "Notification sent successfully"


def consume_notifications():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    def callback(ch, method, properties, body):
        send_email(body)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()


def send_email(body):
    response = requests.post(SES_API_URL, data=body)
    if response.status_code == 200:
        print("Email sent successfully")
    else:
        print("Failed to send email")


if __name__ == "__main__":
    # Start consuming notifications from RabbitMQ
    consume_notifications()

