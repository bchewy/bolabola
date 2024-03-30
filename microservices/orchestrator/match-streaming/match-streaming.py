from flask import Flask
# import pika
import requests
from prometheus_flask_exporter import PrometheusMetrics
import graphene
from flask_socketio import SocketIO, emit
import asyncio

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")

# metrics = PrometheusMetrics(app)

@app.route("/")
def index():
    return "Match Streaming Service.. alive"


VIDEOASS_URL = "http://kong:8000/api/v1/videoasset/"
MATCH_URL = "http://kong:8000/api/v1/match/"

# Flow of orchestrator for streaming:
# 1. Retrieve match from match service
# 2. Find video URL for match
# 3. Get S3 filepath for match;
# 4. Somehow need to stream it back to the UI.


def retrieve_video_url(match_id):
    print("entering retrieve_video_url")
    url = VIDEOASS_URL + "video?id=" + match_id
    response = requests.post(url)
    if response.status_code == 200:
        print("response received from video asset ms")
        video_url = response.json()
        return video_url
    else:
        # TODO: In match microservice, add an endpoint to update the match_id with a default video URL, if it did not previously exist.
        create_video_url = requests.post(
            MATCH_URL + "match-video-url", json={"id": match_id}
        )
        if create_video_url.status_code == 200:
            video_url = create_video_url.json()
            return video_url
        else:
            return "Video URL not found or invalid."


@app.route("/retrieve/<string:id>")
def retrieve_match(id):
    # Retrieve match from match service using GraphQL
    query = """
        query getMatchDetails($id: String) {
            match_details(_id: $id) {
                _id
                name
                description
                venue
                home_team
                away_team
                home_score
                away_score
                date
            }
        }
    """

    variables = {
        "id": id,
    }

    try:
        response = requests.post(
            MATCH_URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            match_data = response.json()
            print("Match data response: ", match_data)
            return match_data
            # if match_data["data"]["match_details"]:
            #     return match_data["data"]["match_details"]
            # else:
            #     return "Match not found", 404
        else:
            return f"Error retrieving match: {response.status_code}", 500
    except requests.exceptions.RequestException as e:
        return f"Error retrieving match: {str(e)}", 500
    
def retrieve_stats():
    return
    

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('connected', {'message': 'Connected to match streaming service'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
    emit('disconnected', {'message': 'Disconnected from match streaming service'})
    
@socketio.on('stream')
def handle_stream_match(timestamp):
    print(f"Received timestamp from client: {timestamp}")
    if timestamp in data:
        print("Data found in timestamp")
        emit('stream', {'data': {
            'timestamp': timestamp,
            'player': data[timestamp]['player'],
            'team': data[timestamp]['team'],
            'event': data[timestamp]['event']
        }})

# AMQP consumer
# def consume_message(channel, method, properties, body):
#     # Process the consumed message here
#     print("Received message:", body.decode())


# def start_consuming():
#     connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
#     channel = connection.channel()
#     channel.queue_declare(queue="my_queue")
#     channel.basic_consume(
#         queue="my_queue", on_message_callback=consume_message, auto_ack=True
#     )
#     channel.start_consuming()

if __name__ == "__main__":
    # app.run(port=9102, debug=True, host="0.0.0.0")
    socketio.run(app, port=9102, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)
    