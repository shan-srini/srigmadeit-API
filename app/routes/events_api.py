from flask import request, jsonify, Blueprint
from app.util.validators import validate_json, validate_query_params
from app.db.events import Event

events_api = Blueprint('events_api', __name__)

@events_api.route('/events', methods=['POST'])
@validate_json({
    'type': 'object',
    'properties': {
        'event': {'type': 'string'},
        'timestamp': {'type' : 'number'},
    },
    'required': ['event', 'timestamp']
})
def create():
    body = request.get_json()
    event = body.get('event')
    timestamp = body.get('timestamp')
    return Event.save(name = event, timestamp = timestamp), 200

@events_api.route('/events', methods=['GET'])
def get_events():
    size = int(request.args.get('size')) if 'size' in request.args else 25
    start = int(request.args.get('page')) * size if 'page' in request.args else 0
    events = Event.get(start = start, size = size)
    return jsonify({'events': events}), 200
