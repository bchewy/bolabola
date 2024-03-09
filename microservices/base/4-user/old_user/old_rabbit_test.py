import pika
import json
import requests

# Replace these variables with your actual RabbitMQ connection parameters
rabbitmq_host = "localhost"  # Use 'rabbitmq' if running inside Docker and linked to RabbitMQ service
rabbitmq_port = 5672
rabbitmq_user = "ticketboost"
rabbitmq_password = "veryS3ecureP@ssword"
queue_name = "ticket_user_queue"

# Setup RabbitMQ connection
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=queue_name)

# Define URL of Flask application where the add_ticket_to_user method is implemented
#"/api/v1/user/<int:user_id>/tickets/add"
def callback_add_ticket(ch, method, properties, body):
    # Convert the message body from bytes to string
    message = body.decode("utf-8")
    print("Received message:", message)

    # Extract user_id, match_id, ticket_category, and ticket_id from the message
    user_id, match_id, ticket_category, ticket_id = message.split(',')

    # Send a POST request to your Flask route to add the ticket to the user
    response = requests.post(user_tickets_url.format(user_id), json={"match_id": match_id, "ticket_category": ticket_category, "ticket_id": ticket_id})

    if response.status_code == 200:
        print("Ticket added successfully")
    else:
        print("Failed to add ticket")

# Start consuming messages for adding tickets to users
channel.basic_consume(queue=queue_name, on_message_callback=callback_add_ticket, auto_ack=True)

# Define URL of Flask application where the view_user_tickets method is implemented
#"/api/v1/user/<int:user_id>/tickets"
def callback_view_tickets(ch, method, properties, body):
    # Convert the message body from bytes to string
    message = body.decode("utf-8")
    print("Received message:", message)

    # Extract user_id from the message
    user_id = message

    # Send a GET request to your Flask route to view all tickets owned by the user
    response = requests.get(f"http://localhost:8015/api/v1/user/{user_id}/tickets")

    if response.status_code == 200:
        print("User tickets:", response.json())
    else:
        print("Failed to view tickets")

# Start consuming messages for viewing tickets owned by users
channel.basic_consume(queue=queue_name, on_message_callback=callback_view_tickets, auto_ack=True)

print("Waiting for messages. To exit press CTRL+C")

channel.start_consuming()
