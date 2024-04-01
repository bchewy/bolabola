from flask import Flask

# import pika
import requests
from prometheus_flask_exporter import PrometheusMetrics
import graphene
from flask_socketio import SocketIO, emit
import json
import redis
from flask import request

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")
redis_client = redis.Redis(host="redis", port=6379, db=0, password="verys3ruec")
responseData = ""

with open("mock_stats.json") as f:
    init_data = json.load(f)
    data = {}
    for item in init_data:
        timestamp = item["timestamp_seconds"]
        del item["timestamp_seconds"]
        data[timestamp] = json.dumps(item)
    # print(data)


@app.route("/")
def index():
    return "Match Streaming Service.. alive"


@socketio.on("connect")
def handle_connect(*args):
    print("Client connected")
    emit("connected", {"message": "Connected to match streaming service"})


@socketio.on("start")
def start_things(*args):
    print("======================================================================")
    print("Client connected")
    # Cache in redis
    BASE_URL = "https://api.twelvelabs.io/v1.2"
    api_key = "tlk_0W18KV92FYPK3S2NY8RQZ2EWFC3R"
    print("Socket iniital connection ===============")
    print("Request args: ", args)
    match_id = args[0]["match_id"]
    # match_id = data.get("match_id")
    print("MATCH ID IS : ", match_id)
    video_id = fetch_match_video(match_id)

    query = {
        "video_id": video_id,
        "type": "summary",
        "prompt": 'return only a json object list called "highlights" of highlights including:\n\ntimestamp\nplayer\nteam\nevent\ndescription\n\nthe timestamp should follow the video\'s timing in seconds as an int,\nexample of event can be "SHOT", "CROSS", "VAR", "PASS"\nbe as specific as possible, at least 10 events',
        # "index_id": "6607ccc7a8753bd44500e816", #matt's 12lab index
        "index_id": "660a6bbf2ae59d128f13369f", #brian's 
    }

    # Send request
    response = requests.post(
        f"{BASE_URL}/summarize", json=query, headers={"x-api-key": api_key}
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")
    responseData = response.json()
    summaryData = json.loads(responseData["summary"])
    summaryDict = {
        item["timestamp"]: json.dumps(item) for item in summaryData["highlights"]
    }
    # print("summaryJson:",summaryJson)
    # print("data",data)
    if not redis_client.exists("stats"):
        # redis_client.hset('stats', mapping=data)
        redis_client.hset("stats", mapping=summaryDict)
    emit("connected", {"message": "Connected to match streaming service"})


# HELPER FUNCTION TO FETCH 12LABS VIDEO ID
def fetch_match_video(match_id):
    url = f"http://localhost:8000/api/v1/videoasset/video/{match_id}"
    response = requests.get(url)
    if response.status_code == 200:
        print("VIDEO Data from within livestats: ", response.json())
        video_data = response.json()
        video_id_12labs = video_data.get("video_id_12labs")
        return video_id_12labs
    else:
        print(
            f"Failed to fetch video for match {match_id}, status code: {response.status_code}"
        )


# Example usage
# fetch_match_video("6608c540d2581f223537c270")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    # Remove redis cache
    redis_client.delete("stats")
    emit("disconnected", {"message": "Disconnected from match streaming service"})


@socketio.on("stream")
def handle_stream_match(timestamp):
    data = redis_client.hget("stats", timestamp)
    try:
        print(f"Received timestamp from client: {timestamp}")
        if redis_client.hexists("stats", timestamp):
            data = redis_client.hget("stats", timestamp)
            data = json.loads(data)
            print("Data found in timestamp")
            emit(
                "stream",
                {
                    "data": {
                        "timestamp": timestamp,
                        "player": data["player"],
                        "team": data["team"],
                        "event": data["event"],
                        "description": data["description"],
                    }
                },
            )
    except Exception as e:
        print(e)
        emit("error", {"message": "Error retrieving data"})


if __name__ == "__main__":
    socketio.run(app, port=9006, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)
