import boto3
import json
import pika


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

    queue_email = "notification"
    queue_telegram = "telegram"

    # Bind the queue to the exchange
    channel.queue_bind(
        exchange="booking", queue=queue_email, routing_key="booking.notification"
    )
    channel.queue_bind(
        exchange="booking", queue=queue_telegram, routing_key="booking.telegram"
    )

    def send_telegram_message(chat_id, message):
        # Placeholder for sending a message via Telegram
        # This should be replaced with actual code to send a message via Telegram API

        print(f"Sending Telegram message to {chat_id}: {message}")

    def telegram_callback(ch, method, properties, body):
        # Parse the message
        message = json.loads(body)

        # Send the telegram message
        send_telegram_message(message["chat_id"], message["message"])

        # Log the notification
        print(f"Sent Telegram message to {message['chat_id']}")

    channel.basic_consume(
        queue=queue_telegram, on_message_callback=telegram_callback, auto_ack=True
    )

    # SES ========================

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

    channel.basic_consume(
        queue=queue_email, on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()


if __name__ == "__main__":
    # Start consuming notifications from RabbitMQ
    consume_notifications()
