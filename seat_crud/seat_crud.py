from flask import Flask, request, jsonify
from flask_cors import CORS
from redis import StrictRedis
import os
import sys
import uuid


app = Flask(__name__)
CORS(app)
redis = StrictRedis(host='redis-cluster', port=6379, decode_responses=True)
TTL_SECONDS = 600

@app.route('/')
def hello():
    redis.ping()
    return "Redis server is running"


@app.route('/api/reservation', methods=['POST'])
def acquire_seat_lock():
    if request.is_json:
        try:
            params = request.get_json()
            tickets = params['tickets']
            identifier = str(uuid.uuid4())
            
            booked_conflicts = []
            reserved_conflicts = []
            
            for ticket in tickets:
                if redis.exists(f"{ticket}_booked"):
                    booked_conflicts.append(ticket)
                    
                elif redis.exists(f"{ticket}_reserved"):
                    reserved_conflicts.append(ticket)
                
            if len(booked_conflicts) > 0 or len(reserved_conflicts) > 0:
                return jsonify({
                    "code": 409,
                    "booked_conflicts": booked_conflicts,
                    "reserved_conflicts": reserved_conflicts,
                    "message": "There are booking or reservation conflicts"
                }), 409
            else:
                identifiers = {}
                
                for ticket in tickets:
                    redis.set(ticket, identifier, nx=True, px=TTL_SECONDS)
                    identifiers[identifier] = ticket
                    
                #TODO: Send request to billing microservice
                
                return jsonify({
                    "code": 200,
                    "lock_identifier": identifiers,
                    "message": f"Ticket(s) {", ".join(tickets)} succesfully reserved for {TTL_SECONDS} seconds"
                }), 200
                    
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


@app.route('/api/reservation/<string:ticket>', methods=['DELETE'])
def release_seat_lock(ticket):
    try:
        if redis.delete(ticket):
            return jsonify({
                "code": 200,
                "message": f"Ticket {ticket} lock has been released"
            }), 200
        
        else:
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
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)