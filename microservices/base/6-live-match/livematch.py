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





if __name__ == "__main__":
    app.run(port=9006, debug=True, host="0.0.0.0")
