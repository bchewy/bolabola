from flask import Flask
import pika
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

# AMQP consumer
def consume_message(channel, method, properties, body):
    # Process the consumed message here
    print("Received message:", body.decode())

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')
    channel.basic_consume(queue='my_queue', on_message_callback=consume_message, auto_ack=True)
    channel.start_consuming()

def retrieve_match(id):
    url = f"http://localhost:8000/matches/{id}"
    response = requests.get(url)
    if response.status_code == 200:
        match = response.json()
        return match
    else:
        return None

if __name__ == '__main__':
    app.run(port=9102)
