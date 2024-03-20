from flask import Flask, request, jsonify
import redis
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)
mongo_client = MongoClient("mongodb://mongodb:27017/")
mongo_db = mongo_client["tickets"]
tickets_collection = mongo_db["tickets"]
app.config["REDIS_URL"] = "redis://redis:6379/0"
redis_client = redis.StrictRedis.from_url(app.config["REDIS_URL"])


@app.route("/reserve", methods=["POST"])
def reserve_seat():
    print("Reserve seat called")
    data = request.json
    user_id = data["user_id"]
    match_id = data["match_id"]
    ticket_category = data["ticket_category"]

    # Check if user_id already has a seat reserved for this match
    existing_ticket = tickets_collection.find_one(
        {"match_id": match_id, "user_id": user_id}
    )
    if existing_ticket:
        return (
            jsonify({"error": "User already has a seat reserved for this match"}),
            409,
        )

    # Find an available ticket for the given match and category
    ticket = tickets_collection.find_one_and_update(
        {
            "match_id": match_id,
            "ticket_category": ticket_category,
            "user_id": None,
        },
        {"$set": {"user_id": user_id}},
        return_document=ReturnDocument.AFTER,
    )

    if ticket:
        if redis_client.set(
            f"ticket_hold:{match_id}:{ticket_category}:{ticket['_id']}",
            user_id,
            ex=300,
            nx=True,
        ):
            return (
                jsonify(
                    {
                        "message": "Seat reserved",
                        "match_id": match_id,
                        "ticket_category": ticket_category,
                        "ticket_id": str(ticket["_id"]),
                    }
                ),
                200,
            )
        else:
            tickets_collection.update_one(
                {"_id": ticket["_id"]}, {"$unset": {"user_id": ""}}
            )
            return jsonify({"error": "Seat is currently on hold"}), 409
    else:
        return (
            jsonify({"error": "No available tickets for this match and category"}),
            400,
        )


@app.route("/release", methods=["POST"])
def release_seat():
    data = request.json
    serial_no = data["serial_no"]
    redis_client.delete(f"ticket_hold:{serial_no}")
    tickets_collection.update_one({"serial_no": serial_no}, {"$unset": {"user_id": ""}})
    return jsonify({"message": "Seat released", "serial_no": serial_no}), 200


@app.route("/validate_reservation/", methods=["POST"])
def validate_reservation():
    data = request.json
    serial_no = data["serial_no"]
    ticket = tickets_collection.find_one({"serial_no": serial_no})
    if ticket and "user_id" in ticket:
        is_held = redis_client.exists(f"ticket_hold:{serial_no}")
        if is_held:
            return (
                jsonify(
                    {
                        "status": "reserved",
                        "message": "This seat is currently on hold.",
                        "user_id": ticket["user_id"],
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "status": "confirmed",
                        "message": "This seat has been confirmed by a user.",
                        "user_id": ticket["user_id"],
                    }
                ),
                200,
            )
    elif ticket:
        return (
            jsonify({"status": "available", "message": "This seat is available."}),
            200,
        )
    else:
        return jsonify({"error": "Seat not found"}), 404


# Health Check
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "alive"}), 200


if __name__ == "__main__":
    app.run(port=9009, debug=True, host="0.0.0.0")
