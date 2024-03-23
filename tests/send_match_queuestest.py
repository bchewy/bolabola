import pika
import json

# RabbitMQ credentials
credentials = pika.PlainCredentials("ticketboost", "veryS3ecureP@ssword")

# RabbitMQ connection parameters
parameters = pika.ConnectionParameters("localhost", 5672, "/", credentials)


def test_rabbitmq_queue():
    # Create a connection to RabbitMQ
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue
    queue_name = "match"
    channel.queue_declare(queue=queue_name, durable=True)

    # Send a test message to the queue
    test_message = {"match_id": "65fe5781ed0d4ff9ea64c8d1", "qty": "1"}
    channel.basic_publish(
        exchange="match-booking-exchange",
        routing_key="match.#",
        body=json.dumps(test_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make the message persistent
        ),
    )
    print(f"Test message sent to the '{queue_name}' queue")

    connection.close()


if __name__ == "__main__":
    test_rabbitmq_queue()   
