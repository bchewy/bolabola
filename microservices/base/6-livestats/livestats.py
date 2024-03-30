from flask import Flask
# import pika
import requests
from prometheus_flask_exporter import PrometheusMetrics
import graphene
from flask_socketio import SocketIO, emit
import json
import redis

app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")
redis_client = redis.Redis(host='redis', port=6379, db=0, password="verys3ruec")
responseData = ""

with open("mock_stats.json") as f:
    init_data = json.load(f)
    data = {}
    for item in init_data:
        timestamp = item['timestamp_seconds']
        del item['timestamp_seconds']
        data[timestamp] = json.dumps(item)
    # print(data)

@app.route("/")
def index():
    return "Match Streaming Service.. alive"

@socketio.on('connect')
def handle_connect(*args):
    print("Client connected")
    # Cache in redis
    BASE_URL = "https://api.twelvelabs.io/v1.2"
    api_key = "tlk_0W18KV92FYPK3S2NY8RQZ2EWFC3R"
    query = {
        "video_id": "6607ccef66995fbd9fd65fbc",
        "type": "summary",
        "prompt": "return only a json object list called \"highlights\" of highlights including:\n\ntimestamp\nplayer\nteam\nevent\ndescription\n\nthe timestamp should follow the video's timing in seconds as an int,\nexample of event can be \"SHOT\", \"CROSS\", \"VAR\", \"PASS\"\nbe as specific as possible, at least 10 events",
        "index_id": "6607ccc7a8753bd44500e816"
    }
# Send request
    response = requests.post(f"{BASE_URL}/summarize", json=query, headers={"x-api-key": api_key})
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")
    responseData = response.json()
    summaryData = json.loads(responseData['summary'])
    summaryDict = {item['timestamp']: json.dumps(item) for item in summaryData['highlights']}
    # print("summaryJson:",summaryJson)
    # print("data",data)
    if not redis_client.exists('stats'):
        # redis_client.hset('stats', mapping=data)
        redis_client.hset('stats', mapping=summaryDict)
    emit('connected', {'message': 'Connected to match streaming service'})
    
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
    # Remove redis cache
    redis_client.delete('stats')
    emit('disconnected', {'message': 'Disconnected from match streaming service'})

@socketio.on('stream')
def handle_stream_match(timestamp):
    data = redis_client.hget('stats', timestamp)
    try:
        print(f"Received timestamp from client: {timestamp}")
        if redis_client.hexists('stats', timestamp):
            data = redis_client.hget('stats', timestamp)
            data = json.loads(data)
            print("Data found in timestamp")
            emit('stream', {'data': {
                'timestamp': timestamp,
                'player': data['player'],
                'team': data['team'],
                'event': data['event'],
                'description':data['description'],
            }})
    except Exception as e:
        print(e)
        emit('error', {'message': 'Error retrieving data'})
if __name__ == "__main__":
    socketio.run(app, port=9006, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)