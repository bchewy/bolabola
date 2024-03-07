from flask import Flask, request, jsonify
import redis
import requests

app = Flask(__name__)

# Redis connection setup
app.config["REDIS_URL"] = "redis://redis:6379/0"  # Adjust as necessary
redis_client = redis.StrictRedis.from_url(app.config["REDIS_URL"])

# Match CRUD Service Base URL
MATCH_CRUD_SERVICE_URL = "http://match"  # Adjust with actual service URL

# Health Check
@app.route("/health/", methods=["GET"])
def health_check():
    return jsonify({"status": "alive"}), 200

# Reserve a seat
@app.route("/reserve/", methods=["POST"])
def reserve_seat():
    data = request.json
    userid = data["userid"]
    matchid = data["matchid"]
    ticketcat = data["ticketcat"]
    ticketid = data["ticketid"]

    # Create a ticket hold in Redis
    if redis_client.set(f"ticket_hold:{ticketid}", userid, ex=300, nx=True):
        # Send HTTP request to Match CRUD Service to decrease seatqty
        response = requests.post(
            f"{MATCH_CRUD_SERVICE_URL}/decrease_seatqty/", json={"matchid": matchid}
        )
        if response.status_code == 200:
            return (
                jsonify(
                    {
                        "message": "Seat reserved and match seat quantity updated.",
                        "status": "success",
                    }
                ),
                200,
            )
        else:
            # Rollback the Redis hold in case of failure to update match service
            redis_client.delete(f"ticket_hold:{ticketid}")
            return (
                jsonify(
                    {
                        "error": "Failed to update seat quantity in match service.",
                        "status": "failure",
                    }
                ),
                response.status_code,
            )
    else:
        return jsonify({"error": "Failed to reserve seat", "status": "failure"}), 400


# Release a seat if not purchased (called when Redis key expires)
@app.route("/release/", methods=["POST"])
def release_seat():
    data = request.json
    ticketid = data["ticketid"]

    # Send HTTP request to Match CRUD Service to increase seatqty
    response = requests.post(
        f"{MATCH_CRUD_SERVICE_URL}/increase_seatqty/", json={"ticketid": ticketid}
    )
    if response.status_code == 200:
        return (
            jsonify(
                {
                    "message": "Seat released and match seat quantity updated.",
                    "status": "success",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "error": "Failed to update seat quantity in match service.",
                    "status": "failure",
                }
            ),
            response.status_code,
        )


# Add any additional endpoints needed for communication with match CRUD service here

if __name__ == "__main__":
    app.run(port=9009, debug=True, host="0.0.0.0")
