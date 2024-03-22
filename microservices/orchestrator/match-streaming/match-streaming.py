from flask import Flask
import pika
import requests
from prometheus_flask_exporter import PrometheusMetrics
import graphene

app = Flask(__name__)

metrics = PrometheusMetrics(app)


@app.route("/")
def index():
    return "Match Streaming Service.. alive"


videoasset_url = "http://kong:8000/api/v1/videoasset/"
match_url = "http://kong:8000/api/v1/match/"

# Flow of orchestrator for streaming:
# 1. Retrieve match from match service
# 2. Find video URL for match
# 3. Get S3 filepath for match;
# 4. Somehow need to stream it back to the UI.


# class Match(graphene.ObjectType):
#     id = graphene.String()
#     name = graphene.String()
    # Add more fields as needed


# class Query(graphene.ObjectType):
#     match = graphene.Field(Match, id=graphene.String())

#     def resolve_match(self, info, id):
#         url = f"http://kong:8000/api/v1/match/{id}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             match_data = response.json()
#             match = Match(
#                 id=match_data["id"],
#                 name=match_data["name"],
#                 # Add more fields as needed
#             )
#             return match
#         else:
#             return None


def retrieve_video_url(match_id):
    print("entering retrieve_video_url")
    url = videoasset_url + "video?id=" + match_id
    response = requests.post(url)
    if response.status_code == 200:
        print("response received from video asset ms")
        video_url = response.json()
        return video_url
    else:
        create_video_url = requests.post(
            match_url + "match-video-url", json={"id": match_id}
        )
        if create_video_url.status_code == 200:
            video_url = create_video_url.json()
            return video_url
        else:
            return "Video URL not found or invalid."


@app.route("/<string:id>")
def retrieve_match(id):
    # Retrieve match from match service using GraphQL
    query = '''
    {
        match_details(_id: "%s") {
            _id
            name
            description
            venue
            home_team
            away_team
            home_score
            away_score
            date
            seats
        }
    }
    ''' % id

    url = match_url + ""
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
            match_data = response.json()
            return match_data['data']['match_details']
    else:
            return "Match not found"


# AMQP consumer
def consume_message(channel, method, properties, body):
    # Process the consumed message here
    print("Received message:", body.decode())


def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="my_queue")
    channel.basic_consume(
        queue="my_queue", on_message_callback=consume_message, auto_ack=True
    )
    channel.start_consuming()


if __name__ == "__main__":
    app.run(port=9102, debug=True, host="0.0.0.0")
