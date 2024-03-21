from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId
from threading import Thread
import pika, json
import requests
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Database connection setup
# we replace localhost here with mongodb because our services are configured to run within docker.
app.config["MONGO_URI"] = "mongodb://mongodb:27017/matches"
mongo = PyMongo(app)

# MongoDB collection
match_collection = mongo.db.matches

def start_rabbitmq_consumer():
    match_id = match_collection.id
    def callback(ch, method, properties, body):
        read_events(match_id)
    credentials = pika.PlainCredentials("ticketboost", "veryS3ecureP@ssword")
    parameters = pika.ConnectionParameters("rabbitmq", 5672, "/", credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_consume(queue="match", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def run_consumer_thread():
    consumer_thread = Thread(target=start_rabbitmq_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()


# Helper function to convert ObjectId to string
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


# Make a call to video asset to place the _id of the match in the videoasset table!
# This is the function that will be called when a new match is created.
# We will use the match id to create a new video asset in the videoasset table.
@app.route("/match-video-url", methods=["POST"])
def create_video_asset():
    # This is the URL of the videoasset service
    # get matchid from json body of the requests
    video_id = request.json.get("id")
    url = f"http://kong:8000/api/v1/videoasset/video?id={video_id}"
    response = requests.post(url, json={"id": video_id})
    if response.status_code == 200:
        video_url = response.json()
        print("exiting retrieve_video_url")
        return video_url
    else:
        print("exiting retrieve_video_url but found nothing")
        return "Error"


# Route handlers
# Match Create
@app.route("/create/", methods=["POST"])
def create_event():
    data = request.json
    new_event = {
        "name": data["name"],
        "description": data["description"],
        "date": data["date"],
        "venue": data["venue"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    match_id = match_collection.insert_one(new_event).inserted_id
    created_event = match_collection.find_one({"_id": match_id})
    return jsonify(serialize_doc(created_event))


# Match Read All
@app.route("/", methods=["GET"])
def read_events():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)
    events = match_collection.find().skip(skip).limit(limit)
    return jsonify([serialize_doc(event) for event in events])


# Match Read 1
@app.route("/<string:match_id>", methods=["GET"])
def read_event(match_id):
    event = match_collection.find_one({"_id": ObjectId(match_id)})
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(serialize_doc(event))


# Match Update
@app.route("/<string:match_id>", methods=["PUT"])
def update_event(match_id):
    data = request.json
    result = match_collection.update_one(
        {"_id": ObjectId(match_id)},
        {"$set": data, "$currentDate": {"updated_at": True}},
    )
    if result.matched_count == 0:
        return jsonify({"error": "Event not found"}), 404
    updated_event = match_collection.find_one({"_id": ObjectId(match_id)})
    return jsonify(serialize_doc(updated_event))


# Match Delete
@app.route("/<string:match_id>", methods=["DELETE"])
def delete_event(match_id):
    result = match_collection.delete_one({"_id": ObjectId(match_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({"message": "Event deleted successfully"}), 200


if __name__ == "__main__":
    run_consumer_thread()
    app.run(port=9001, debug=True, host="0.0.0.0")
