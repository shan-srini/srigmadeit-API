from flask import request, jsonify, Blueprint
from app.util.validators import validate_json, validate_query_params, validate_authorization
from app.db.media import Media

media_api = Blueprint('media_api', __name__)

@media_api.route('/events/<string:event_id>/categories/<string:category_id>/media', methods=['POST'])
@validate_authorization
@validate_json({
    'type': 'object',
    'properties': {
        'source': {'type': 'string', 'enum': ['b2', 'gd']}, # backblaze b2 or Google Drive (videos)
        'count': {'type': 'number', 'minimum': 1},
        'request_id': {'type': 'string'}
    },
    'required': ['source']
})
def create(event_id:str, category_id: str):
    ''' Will create a Media instance under this event/category and return uuid '''
    body = request.get_json()
    source = body.get('source')
    count = int(body.get('count')) if 'count' in body else 1
    request_id = body.get('request_id') # Totally okay if this is None. Only use case is for videos, where id is precreated
    if request_id and count > 1:
        return jsonify({'success': False, 'log': "Single id provided, but multiple media creation requested."})
    media_ids = Media.save(event_id = event_id, category_id=category_id, count=count, source=source, request_id=request_id)
    return jsonify({'success': True, 'media_ids': media_ids})

@media_api.route('/media', methods=['GET'])
def get_media():
    category_id = request.args.get('categoryId')
    event_id = request.args.get('eventId') # NOTE AND/OR IS CURRENTLY NOT SUPPORTED, CATEGORY TAKES PRECEDENCE, one or the other.
    size = int(request.args.get('size')) if 'size' in request.args else 25
    start = int(request.args.get('page')) * size if 'page' in request.args else 0
    reverse = bool(request.args.get('reverse')) if 'reverse' in request.args else False
    if category_id is None and event_id is None:
        return jsonify({success: False, 'log': 'provide searchParam categoryId or eventId'}), 400
    media = Media.get(category_id = category_id, event_id = event_id, start = start, size = size, reverse = reverse)
    return jsonify({'success': True, 'media_ids': list(media), 'count': media.count()}), 200