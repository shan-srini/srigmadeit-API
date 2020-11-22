from flask import request, jsonify, Blueprint
from app.util.validators import validate_json, validate_query_params
from app.db.categories import Category

categories_api = Blueprint('categories_api', __name__)

@categories_api.route('/events/<string:event>/categories', methods=['POST'])
@validate_json({
    'type': 'object',
    'properties': {
        'priority': {'type' : 'number', 'minimum': 0, 'maximum': 10},
        'event': {'type': 'string'},
        'category': {'type': 'string'}
    },
    'required': ['priority', 'event', 'category']
})
def create(event: str):
    body = request.get_json()
    event = body.get('event')
    category = body.get('category')
    priority = body.get('priority')
    return Category.save(event = event, category = category, priority = priority), 200

@categories_api.route('/events/<string:event>/categories', methods=['GET'])
def get_by_event(event: str):
    categories = Category.get(event=event)
    return jsonify({'categories': categories}), 200


# size = int(request.args.get('size')) if 'size' in request.args else 25
# start = int(request.args.get('page')) * size if 'page' in request.args else 0