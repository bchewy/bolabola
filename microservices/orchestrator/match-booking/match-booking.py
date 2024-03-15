from flask import Flask
import pika
from threading import Thread


####### RabbitMQ  #######
def start_rabbitmq_consumer():
    def callback(ch, method, properties, body):
        pass

    credentials = pika.PlainCredentials("ticketboost", "veryS3ecureP@ssword")
    parameters = pika.ConnectionParameters("rabbitmq", 5672, "/", credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue="match", durable=True)
    channel.basic_consume(queue="match", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def run_consumer_thread():
    consumer_thread = Thread(target=start_rabbitmq_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()


app = Flask(__name__)


#### Helper Functions #####
def publish_to_amqp():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    # Publish to user to update match booking
    channel.queue_declare(queue="user")
    channel.basic_publish(
        exchange="",
        routing_key="user",
        body="User has purchased ticket for match with id {123} !",
    )

    # Publish to Match Queue to update ticket availablity
    channel.queue_declare(queue="match")
    channel.basic_publish(
        exchange="", routing_key="match", body="Match with id {123} has been booked!"
    )

    # Publish to seat reservation to remove ticket lock
    channel.queue_declare(queue="seat")
    channel.basic_publish(
        exchange="", routing_key="seat", body="Seat with id {123} has been booked!"
    )

    # Publish to notification
    channel.queue_declare(queue="notification")
    channel.basic_publish(
        exchange="",
        routing_key="notification",
        body="Notification for match with id {123} has been sent!",
    )

    connection.close()


@app.route("/")
def hello():
    return "Match Booking orcha is alive!"


# def consume_message(channel, method, properties, body):
#     # Process the consumed message here
#     print("Received message:", body.decode())

# def start_consuming():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()
#     channel.queue_declare(queue='my_queue')
#     channel.basic_consume(queue='my_queue', on_message_callback=consume_message, auto_ack=True)
#     channel.start_consuming()

if __name__ == "__main__":
    app.run(port=9101)
