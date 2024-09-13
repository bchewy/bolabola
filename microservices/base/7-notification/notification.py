import boto3
import json
import pika


def consume_notifications():
    # Hardcoded credentials and connection details for RabbitMQ
    print("Now consuming messages")
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

    # declare and find queues for 'booking'
    exchangeBooking = channel.exchange_declare(
        exchange="booking", exchange_type="direct", durable=True
    )
    queueBooking = channel.queue_declare(queue="booking_notification", durable=True)
    channel.queue_bind(
        exchange="booking", queue="booking_notification", routing_key="booking.notification"
    )

    # declare and find queues for 'refunds'
    exchangeRefunds = channel.exchange_declare(
        exchange="refunds", exchange_type="direct", durable=True
    )
    queueRefunds = channel.queue_declare(queue="refunds_notification", durable=True)
    channel.queue_bind(
        exchange="refunds", queue="refunds_notification", routing_key="refunds.notification"
    )

    print(
        f"Attempting to connect to RabbitMQ at {rabbitmq_host} with user '{rabbitmq_user}'"
    )

    def callbackRefund(ch, method, properties, body):
        # Parse the message
        message = json.loads(body)
        print("Received a message into the notification service: ", message)
        email = message["email"]
        subject = "Refund Confirmation!"
        match = message["match"]
        bodyme = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Refund Confirmation</title>
            <style>
                body {{font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}}
                .container {{max-width: 600px; margin: auto; background: #f7f7f7; padding: 20px; border-radius: 8px;}}
                h2 {{color: #007BFF;}}
                p {{line-height: 1.6;}}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Refund Confirmation</h2>
                <p>Dear User,</p>
                <p>Your refund has been successfully processed. You have been refunded for the following match:</p>
                <ul>
                    <li>Match: {match['name']}</li>
                    <li>Date: {match['date']}</li>
                    <li>Teams: {match['home_team']} vs {match['away_team']}</li>
                </ul>
                <p>If you have any questions, feel free to contact our support team.</p>
                <p>Best Regards,<br>Bolabola Team</p>
            </div>
        </body>
        </html>
        """

        # Send the email
        send_email(email, subject, bodyme)

        # Log the notification
        print(f"Sent notification to {message['email']}")

    def callbackBooking(ch, method, properties, body):
        # Parse the message
        message = json.loads(body)
        print("Received a message into the notification service: ", message)
        try:
            email = message["email"]
            subject = "Booking Confirmation!"
            match = message["match"]
            quantity = message["quantity"]
            bodyme = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Booking Confirmation</title>
                <style>
                    body {{font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}}
                    .container {{max-width: 600px; margin: auto; background: #f7f7f7; padding: 20px; border-radius: 8px;}}
                    h2 {{color: #007BFF;}}
                    p {{line-height: 1.6;}}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Booking Confirmation</h2>
                    <p>Dear User,</p>
                    <p>Thank you for your booking. You have successfully booked {quantity} tickets for the match:</p>
                    <ul>
                        <li>Match: {match['name']}</li>
                        <li>Date: {match['date']}</li>
                        <li>Teams: {match['home_team']} vs {match['away_team']}</li>
                    </ul>
                    <p>If you have any questions, feel free to contact our support team.</p>
                    <p>Best Regards,<br>Bolabola Team</p>
                </div>
            </body>
            </html>
            """
        except KeyError:
            email = message["email"]
            subject= "Booking Failed!"
            bodyme = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Booking Failed</title>
                <style>
                    body {{font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}}
                    .container {{max-width: 600px; margin: auto; background: #f7f7f7; padding: 20px; border-radius: 8px;}}
                    h2 {{color: #007BFF;}}
                    p {{line-height: 1.6;}}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Booking Failed</h2>
                    <p>Dear User,</p>
                    <p>Unfortunately, your booking has failed. Please try again later.</p>
                    <p>If you have any questions, feel free to contact our support team.</p>
                    <p>Best Regards,<br>Bolabola Team</p>
                </div>
            </body>
            </html>
            """

        # Send the email
        send_email(email, subject, bodyme)

        # Log the notification
        print(f"Sent notification to {message['email']}")
    
    channel.basic_consume(
        queue=queueRefunds.method.queue, on_message_callback=callbackRefund, auto_ack=True
    )
    channel.basic_consume(
        queue=queueBooking.method.queue, on_message_callback=callbackBooking, auto_ack=True
    )


    # queue_email = "notification"
    # queue_telegram = "telegram"

    # # Bind the queue to the exchange
    # channel.queue_bind(
    #     exchange="booking", queue=queue_email, routing_key="booking.notification",
    # )

    # channel.queue_bind(
    #     exchange="refunds", queue=queue_email, routing_key="refunds.notification",
    # )

    # channel.basic_consume(
    #     queue=queue_email, on_message_callback=callbackRefund, auto_ack=True
    # )

    # channel.queue_bind(
    #     exchange="booking", queue=queue_telegram, routing_key="booking.telegram"
    # )

    # def send_telegram_message(chat_id, message):
    #     # Placeholder for sending a message via Telegram
    #     # This should be replaced with actual code to send a message via Telegram API

    #     print(f"Sending Telegram message to {chat_id}: {message}")

    # def telegram_callback(ch, method, properties, body):
    #     # Parse the message
    #     message = json.loads(body)

    #     # Send the telegram message
    #     send_telegram_message(message["chat_id"], message["message"])

    #     # Log the notification
    #     print(f"Sent Telegram message to {message['chat_id']}")

    # channel.basic_consume(
    #     queue=queue_telegram, on_message_callback=telegram_callback, auto_ack=True
    # )

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
                    "Html": {
                        "Data": body,
                    },
                },
            },
        )

    # channel.basic_consume(
    #     queue=queue_email, on_message_callback=callbackBooking, auto_ack=True
    # )
    channel.start_consuming()


if __name__ == "__main__":
    # Start consuming notifications from RabbitMQ
    consume_notifications()
