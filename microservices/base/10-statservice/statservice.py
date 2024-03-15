from flask import Flask, request, jsonify
from datetime import datetime
from flask_socketio import SocketIO, send
import asyncio
import websockets
import random 
import json
# Sample data
sport_stats = [
    {"timestamp": 234, "highlight": "Goal by Player 1", "score": "Team A 1 - Team B 0"},
    {"timestamp": 300, "highlight": "Red card for Player 2", "score": "Team A 1 - Team B 0"},
    {"timestamp": 350, "highlight": "Substitution: Player 3 in, Player 4 out", "score": "Team A 1 - Team B 0"},
] 

async def send_data(websocket, path):
        for stat in sport_stats:
        # i = random.randint(1,1000)
            print(stat)
            await websocket.send(json.dumps(stat))
            await asyncio.sleep(10)  # Wait for 1 second before sending next data

async def main():
    async with websockets.serve(send_data, '0.0.0.0', 9901):
        await asyncio.Future()  # Keep running indefinitely

if __name__ == "__main__":
    asyncio.run(main()) 