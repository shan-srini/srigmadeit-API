from flask import request, jsonify, Blueprint
from app.util.validators import validate_json, validate_query_params, validate_authorization
from app.db.media import Media

media_api = Blueprint('media_api', __name__)

@media_api.route('/categories/<string:category>/media', methods=['POST'])
@validate_authorization
@validate_json({
    'type': 'object',
    'properties': {
        'source': {'type': 'string', 'enum': ['b2', 'youtube']},
        'count': {'type': 'number', 'minimum': 1}
    },
    'required': ['source']
})
def create(category: str):
    ''' Will create a Media instance under this event/category and return uuid '''
    body = request.get_json()
    count = int(body.get('count')) if 'count' in body else 1
    media_ids = Media.save(category_id=category, count=count)
    return jsonify({'success': True, 'media_ids': media_ids})

@media_api.route('/categories/<string:category>/media', methods=['GET'])
def get_media(category_id: str):
    size = int(request.args.get('size')) if 'size' in request.args else 25
    start = int(request.args.get('page')) * size if 'page' in request.args else 0
    media = Media.get(category = category, start = start, size = size)
    return jsonify({'success': True, 'media_ids': media}), 200