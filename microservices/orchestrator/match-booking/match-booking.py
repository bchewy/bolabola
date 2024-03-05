from flask import Flask
import pika

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

def consume_message(channel, method, properties, body):
    # Process the consumed message here
    print("Received message:", body.decode())

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')
    channel.basic_consume(queue='my_queue', on_message_callback=consume_message, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    app.run(port=9101)
