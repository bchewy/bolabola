from flask import Flask, request, jsonify
import pika
import stripe
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_API_KEY')

# Initialize RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='my_queue')

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    amount = data['amount']
    currency = data['currency']
    description = data['description']
    token = data['token']

    charge = stripe.Charge.create(
        amount=amount,
        currency=currency,
        description=description,
        source=token
    )

    # Send a message to the queue
    channel.basic_publish(exchange='', routing_key='my_queue', body=charge['id'])

    return jsonify(charge)

if __name__ == '__main__':
    app.run()

# def consume_message(channel, method, properties, body):
#     # Process the consumed message here
#     print("Received message:", body.decode())

# def start_consuming():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()
#     channel.queue_declare(queue='my_queue')
#     channel.basic_consume(queue='my_queue', on_message_callback=consume_message, auto_ack=True)
#     channel.start_consuming()

# if __name__ == '__main__':
#     app.run()

