from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
from redis import Redis
import os
import sys

"""
Ticket reservation microservice accepts HTTP POST request from booking microservice
params
    available_tickets: list of ticket IDs that are available in the ticket DB

It will iterate through the list of tickets and reserve the first one that is not locked in Redis, with an expiry (TTL) of 10 minutes.

TODO: Seat optimizer to allow bookings for multiple tickets to sit together
"""

app = Flask(__name__)
CORS(app)
redis = Redis(host='redis-cluster', port=6379, decode_responses=True)
TTL_SECONDS = 600

@app.route('/')
def hello():
    redis.ping()
    return "Redis server is running"

@app.route('/api/reservation/<string:ticket>', methods=['DELETE'])
def remove_reserved_seat(ticket):
    try:
        if redis.exists(ticket):
            redis.delete(ticket)
            return jsonify({
                "code": 200,
                "message": f"Ticket {ticket} has been removed"
            }), 200
        return jsonify({
            "code": 400,
            "message": f"Ticket {ticket} is currently not reserved"
        }), 400
    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "Internal server error: " + ex_str
        }), 500
        

@app.route('/api/reservation', methods=['POST'])
def reserve_seat():
    if request.is_json:
        try:
            params = request.get_json()
            available = params['available_tickets']
            
            shortest_ttl = TTL_SECONDS
            
            for ticket in available:
                if not redis.exists(ticket):
                    redis.set(ticket, "locked", ex=TTL_SECONDS)
                    return jsonify({
                        "code": 200,
                        "ticket": ticket,
                        "message": f"Ticket {ticket} has been reserved with TTL of 10 minutes"
                    }), 200
                shortest_ttl = min(shortest_ttl, redis.ttl(ticket))
                
            return jsonify({
                "code": 409,
                "message": f"All tickets are reserved, check back in {shortest_ttl} seconds"
            }), 409
            
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Internal server error: " + ex_str
            }), 500
    
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def consume_message(channel, method, properties, body):
    # Process the consumed message here
    print("Received message:", body.decode())

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')
    channel.basic_consume(queue='my_queue', on_message_callback=consume_message, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
