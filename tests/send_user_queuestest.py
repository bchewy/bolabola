import requests
import json
import requests
import json
import pika
import json

connection_params = pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('ticketboost', 'veryS3ecureP@ssword'))
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Define the queue name
queue_name = 'user_queue'

# Define the message data
message_data = {"match_id": "1", "ticket_category": "A", "serial_no": "100"}

# Convert the message data to JSON
message_json = json.dumps(message_data)

# Publish the message to the queue
channel.basic_publish(exchange='', routing_key=queue_name, body=message_json)

# Close the connection
connection.close()