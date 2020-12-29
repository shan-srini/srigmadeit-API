from flask import request, jsonify, Blueprint
from app.util.validators import validate_json, validate_query_params, validate_authorization
from app.db.categories import Category

categories_api = Blueprint('categories_api', __name__)

@categories_api.route('/events/<string:event_id>/categories', methods=['POST'])
@validate_authorization
@validate_json({
    'type': 'object',
    'properties': {
        'order': {'type' : 'number', 'minimum': 0, 'maximum': 10},
        'name': {'type': 'string', 'minLength': 3}
    },
    'required': ['order', 'name']
})
def create(event_id: str):
    body = request.get_json()
    category = body.get('name')
    order = body.get('order')
    ret = Category.save(event_id = event_id, category_name = category, order = order)
    return jsonify({'success': True, 'category_id': ret}), 200

@categories_api.route('/events/<string:event_id>/categories', methods=['GET'])
def get_by_event(event_id: str):
    categories = Category.get(event_id=event_id)
    return jsonify({'success': True, 'categories': categories}), 200

@categories_api.route('/events/<string:event_id>/categories/<string:category_id>', methods=['PUT'])
@categories_api.route('/categories/<string:category_id>', methods=['PUT'])
@validate_authorization
@validate_json({
    'type': 'object',
    'properties': {
        'order': {'type' : 'number', 'minimum': 0, 'maximum': 10},
        'name': {'type': 'string'}
    },
})
def edit(event_id: str, category_id: str):
    body = request.get_json()
    ret = Catgory.update_meta(category_id=category_id, request_update=body)
    return jsonify({'success': ret})