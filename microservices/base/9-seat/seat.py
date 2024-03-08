from flask import Flask, request, jsonify
import redis
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
mongo_client = MongoClient("mongodb://mongodb:27017/")
mongo_db = mongo_client["ticket_db"]
tickets_collection = mongo_db["tickets"]

# Redis connection setup
app.config["REDIS_URL"] = "redis://redis:6379/0"  # Adjust as necessary
redis_client = redis.StrictRedis.from_url(app.config["REDIS_URL"])


# Reserve a seat
# Sample Request Body
# {
#     "user_id": "123456789",
#     "match_id": "987654321",
#     "ticket_category": "A"
# }
# Do take note that the and match_id and ticket categoryshould be valid and existing
@app.route("/reserve/", methods=["POST"])
def reserve_seat():
    data = request.json
    user_id = data["user_id"]
    match_id = data["match_id"]
    ticket_category = data["ticket_category"]

    # Find an available ticket
    ticket = tickets_collection.find_one(
        {
            "match_id": match_id,
            "ticket_category": ticket_category,
            "user_id": {"$exists": False},
        }
    )

    if ticket:
        serial_no = ticket["serial_no"]
        # Create a ticket hold in Redis with TTL
        if redis_client.set(f"ticket_hold:{serial_no}", user_id, ex=300, nx=True):
            # Update ticket with user_id to lock it temporarily
            tickets_collection.update_one(
                {"serial_no": serial_no}, {"$set": {"user_id": user_id}}
            )
            return jsonify({"message": "Seat reserved", "serial_no": serial_no}), 200
        else:
            return jsonify({"error": "Seat is currently on hold"}), 409
    else:
        return jsonify({"error": "No available seats"}), 404


# Release a seat - only if the need arises.
# Sample Request Body
# {
#     "serial_no": "12345"
# }
@app.route("/release/", methods=["POST"])
def release_seat():
    data = request.json
    serial_no = data["serial_no"]

    # Remove the ticket hold from Redis
    redis_client.delete(f"ticket_hold:{serial_no}")

    # Set the user_id to None in MongoDB to make the seat available again
    tickets_collection.update_one({"serial_no": serial_no}, {"$unset": {"user_id": ""}})
    return jsonify({"message": "Seat released", "serial_no": serial_no}), 200


@app.route("/validate_reservation/", methods=["POST"])
def validate_reservation():
    data = request.json
    serial_no = data["serial_no"]

    # Check in MongoDB if the seat has a user_id assigned
    ticket = tickets_collection.find_one({"serial_no": serial_no})

    if ticket and "user_id" in ticket:
        # Check if the ticket hold still exists in Redis
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
@app.route("/health/", methods=["GET"])
def health_check():
    return jsonify({"status": "alive"}), 200


if __name__ == "__main__":
    app.run(port=9009, debug=True, host="0.0.0.0")
