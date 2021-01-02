from flask import request, jsonify, Blueprint
from app.util.validators import validate_json, validate_query_params, validate_authorization
from app.db.events import Event
from app.db.categories import Category

events_api = Blueprint('events_api', __name__)

@events_api.route('/events', methods=['POST'])
@validate_authorization
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
    try:
        saved_id: str = Event.save(name = event, timestamp = timestamp)
        return jsonify({'success': True, 'event_id': saved_id})
    except BaseException as e:
        print(e)
        return jsonify({'success':False, 'log': "Most likely duplicate event id"}), 400

@events_api.route('/events', methods=['GET'])
def get_events():
    
    size = int(request.args.get('size')) if 'size' in request.args else 25
    start = int(request.args.get('page')) * size if 'page' in request.args else 0
    events = Event.get(start = start, size = size, search_name = request.args.get('name'))
    return jsonify({'success': True, 'events': list(events), 'count': events.count()}), 200

@events_api.route('/events/<string:event_id>', methods=['GET'])
def get_event(event_id: str):
    event_meta = Event.get_meta(event_id = event_id)
    if event_meta is None:
        return jsonify({'success': False, 'log': "Event not found"}), 404
    categories = Category.get(event_id = event_id)
    return jsonify({'success': True, 'event_meta': event_meta, 'categories': categories}), 200

@events_api.route('/events/<string:event_id>', methods=['GET'])
@validate_authorization
def delete_event(event_id: str):
    if Event.delete(event_id=event_id):
        Category.delete(event_id=event_id)
        deleted_media_ids = Media.delete(event_id=event_id)
        deleted_media_ids.append(event_id)
        return jsonify({'success': True, 'deleted_media': deleted_media_ids})
    else:
        return jsonify({'success': False}), 404