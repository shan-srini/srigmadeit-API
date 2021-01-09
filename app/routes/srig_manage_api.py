# Routes for managing photos, login, etc.
import os
from flask import request, jsonify, Blueprint
from app.util.validators import validate_json, validate_query_params, validate_authorization
from app.util import general
import app.util.jwt as jwt_util

srig_manage_api = Blueprint('srig_manage_api', __name__)

@srig_manage_api.route('/login', methods=['POST'])
@validate_json({
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
})
def login():
    body = request.get_json()
    user = body.get('username')
    password = body.get('password')
    secret_user = os.environ['SRIG_USER']
    secret_password = os.environ['SRIG_PASS']
    if user == secret_user and password == secret_password:
        res = jsonify({'success': True, 'cosConfig': general.get_cos_creds()})
        token = jwt_util.produce_jwt()
        res.set_cookie("AUTH_TOKEN", token, httponly=True, samesite="lax")
        return res, 200
    else:
        return jsonify({'success': False}), 403

@srig_manage_api.route('/validate', methods=['POST'])
@validate_authorization
def validate():
    # validate_authorization will return 401 if not authorized
    return jsonify({'success': True}), 200