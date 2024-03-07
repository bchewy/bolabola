from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)

# Database connection setup
# we replace localhost here with mongodb because our services are configured to run within docker.
app.config["MONGO_URI"] = "mongodb://mongodb:27017/matchs_db"
mongo = PyMongo(app)

# MongoDB collection
match_collection = mongo.db.matchs


# Helper function to convert ObjectId to string
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


# Route handlers
@app.route("/match/", methods=["POST"])
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
    match_id = match_collection.insert_one(new_event).inserted_id
    created_event = match_collection.find_one({"_id": match_id})
    return jsonify(serialize_doc(created_event))


@app.route("/match/", methods=["GET"])
def read_events():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)
    events = match_collection.find().skip(skip).limit(limit)
    return jsonify([serialize_doc(event) for event in events])


@app.route("/matches/<string:match>", methods=["GET"])
def read_event(match_id):
    event = match_collection.find_one({"_id": ObjectId(match_id)})
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(serialize_doc(event))


if __name__ == "__main__":
    app.run(port=9001, debug=True, host="0.0.0.0")
