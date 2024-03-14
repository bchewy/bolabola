from flask import Flask
import pika
import requests
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

@app.route('/')
def index():
    return "Match Streaming Service.. alive"

# Flow of orchestrator for streaming:
# 1. Retrieve match from match service
# 2. Find video URL for match
# 3. Get S3 filepath for match;
# 4. Somehow need to stream it back to the UI.

def retrieve_video_url(match_id):
    print('entering retrieve_video_url')
    url = f"http://kong:8000/videoasset/video?id={match_id}" # Currently videoasset only has ids ,1,23,4,5,6... not the objectids from Mongo.
    response = requests.get(url)
    if response.status_code == 200:
        video_url = response.json()
        print('exiting retrieve_video_url')
        return video_url
    else:
        print('exiting retrieve_video_url but found nothing')
        return None


@app.route('/<string:id>')
def retrieve_match(id):
    print('entering retrieve_match')
    url = f"http://kong:8000/match/{id}"
    response = requests.get(url)
    if response.status_code == 200:
        match = response.json()
        print(match)
        print('exiting retrieve_match')
        video_url = retrieve_video_url(id)
        return [match, video_url]
    else:
        print('exiting retrieve_match but found nothing')
        return None
    



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



if __name__ == '__main__':
    app.run(port=9102, debug=False, host='0.0.0.0')
