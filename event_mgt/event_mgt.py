import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/event_mgt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app) 

class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def json(self):
        return {"event_id": self.event_id, 
                "name": self.name, 
                "description": self.description, 
                "location": self.location, 
                "created_at": self.created_at, 
                "updated_at": self.updated_at}
    

@app.route("/events",methods=['GET'])
def get_all():
    events = Event.query
    name = request.args.get('name')
    location = request.args.get('location')
    if name:
        events = events.filter_by(name=name)
    if location:
        events = events.filter_by(location=location)
    events = events.all()
    if(events):
        return jsonify({"body": [event.json() for event in events]})
    return jsonify({"message": "There are no events."}), 404


@app.route("/events/<int:event_id>",methods=['GET'])
def get_event(event_id):
        event = Event.query.get(event_id)
        if(event):
            return jsonify(event.json())
        return jsonify({"message": "Event not found."}), 404

if __name__ == "__main__":
    app.run(port='5000',debug=True)


