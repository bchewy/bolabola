import pika
import json

# Replace these variables with your actual RabbitMQ connection parameters
rabbitmq_host = "localhost"  # Use 'rabbitmq' if running inside Docker and linked to RabbitMQ service
rabbitmq_port = 5672
rabbitmq_user = "ticketboost"
rabbitmq_password = "veryS3ecureP@ssword"
exchange_name = "notifications"
routing_key = "notification.test"
test_message = {
    "email": "brian@bchewy.com",
    "subject": "Test Message",
    "body": "This is a test message from RabbitMQ!",
}

# Setup RabbitMQ connection
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
parameters = pika.ConnectionParameters(
    host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Publish a message
channel.basic_publish(
    exchange=exchange_name, routing_key=routing_key, body=json.dumps(test_message)
)
print(
    " [x] Sent test message to exchange:",
    exchange_name,
    "with routing key:",
    routing_key,
)

# Close the connection
connection.close()
