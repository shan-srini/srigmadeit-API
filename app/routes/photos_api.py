from flask import request, jsonify, Blueprint
from app.util.validators import validate_json, validate_query_params
from app.db.photos import Photo

photos_api = Blueprint('photos_api', __name__)

@photos_api.route('/events/<string:event>/categories/<string:category>/photos', methods=['POST'])
def create(event: str, category: str):
    ''' Will create a photo instance under this event/category and return uuid '''
    photo_id = Photo.save(event=event, category=category)
    return jsonify({'photo_id': photo_id})

@events_api.route('/events/<string:event>/categories/<string:category>/photos', methods=['GET'])
def get_events(event: str, category: str):
    size = int(request.args.get('size')) if 'size' in request.args else 25
    start = int(request.args.get('page')) * size if 'page' in request.args else 0
    photos = Photo.get(category = category, start = start, size = size)
    return jsonify({'photos': photos}), 200