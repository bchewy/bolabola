from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for events
events = []

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(events)

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    for event in events:
        if event['id'] == event_id:
            return jsonify(event)
    return jsonify({'error': 'Event not found'}), 404

@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    event = {
        'id': len(events) + 1,
        'name': data['name'],
        'date': data['date'],
        'location': data['location']
    }
    events.append(event)
    return jsonify(event), 201

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    for event in events:
        if event['id'] == event_id:
            event['name'] = data['name']
            event['date'] = data['date']
            event['location'] = data['location']
            return jsonify(event)
    return jsonify({'error': 'Event not found'}), 404

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    for event in events:
        if event['id'] == event_id:
            events.remove(event)
            return jsonify({'message': 'Event deleted'})
    return jsonify({'error': 'Event not found'}), 404

if __name__ == '__main__':
    app.run()
