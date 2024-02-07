from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)

# Database connection setup
# we replace localhost here with mongodb because our services are configured to run within docker.
app.config["MONGO_URI"] = "mongodb://mongodb:27017/events_db"
mongo = PyMongo(app)

# MongoDB collection
events_collection = mongo.db.events


# Helper function to convert ObjectId to string
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


# Route handlers
@app.route("/events/", methods=["POST"])
def create_event():
    data = request.json
    new_event = {
        "name": data["name"],
        "description": data["description"],
        "date": data["date"],
        "location": data["location"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    event_id = events_collection.insert_one(new_event).inserted_id
    created_event = events_collection.find_one({"_id": event_id})
    return jsonify(serialize_doc(created_event))


@app.route("/events/", methods=["GET"])
def read_events():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)
    events = events_collection.find().skip(skip).limit(limit)
    return jsonify([serialize_doc(event) for event in events])


@app.route("/events/<string:event_id>", methods=["GET"])
def read_event(event_id):
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(serialize_doc(event))


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
