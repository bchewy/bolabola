import boto3
import json
import pika
import os


def consume_notifications():
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

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    print(
        f"Attempting to connect to RabbitMQ at {rabbitmq_host} with user '{rabbitmq_user}'"
    )

    # Declare the exchange
    channel.exchange_declare(exchange="", exchange_type="direct")

    # Declare the queue
    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the exchange
    channel.queue_bind(
        exchange="", queue=queue_name, routing_key="notification"
    )

    # Set up AWS SES client with explicit region
    ses = boto3.client("ses", region_name="ap-southeast-1")  # AWS SES region

    def send_email(recipient, subject, body):
        ses.send_email(
            Source="brian@bchewy.com",  # Verified SES email address
            Destination={
                "ToAddresses": [
                    recipient,
                ],
            },
            Message={
                "Subject": {
                    "Data": subject,
                },
                "Body": {
                    "Text": {
                        "Data": body,
                    },
                },
            },
        )

    def callback(ch, method, properties, body):
        # Parse the message
        message = json.loads(body)

        # Send the email
        send_email(message["email"], message["subject"], message["body"])

        # Log the notification
        print(f"Sent notification to {message['email']}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Waiting for notifications. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    # Start consuming notifications from RabbitMQ
    consume_notifications()
