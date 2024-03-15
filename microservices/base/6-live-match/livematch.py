from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send
from datetime import datetime
import websockets
import asyncio
import threading

app = Flask(__name__)
socketio = SocketIO(app)
data_collection = []

async def receive_data(): #establish ws connection and recv data
    async with websockets.connect('ws://statservice:9901') as ws:
        while True:
            data = await ws.recv()
            data_collection.append(data)
            await asyncio.sleep(5)

def start_loop(loop): #runs the receive_data() func in a loopt to retrieve data from ws server
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receive_data())

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route('/') #test app endpoint
def index():
    return "live match Service.. alive"




@app.route('/retrievedata', methods=["GET"])
def retrieve_data():
    return jsonify({'data': data_collection})

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_loop, args=(loop,))
    t.start()
    app.run(port=9006, debug=True, host="0.0.0.0")
