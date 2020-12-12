import jsonschema
from functools import wraps
from flask import jsonify, request
from app.util.jwt import is_jwt_valid

def validate_json(expected: dict):
    """ Validates mimetype is json (), then uses jsonschema to try to validate the request body """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):     
            try:
                request_body = request.get_json()
                jsonschema.validate(instance=request_body, schema=expected)
            except jsonschema.exceptions.ValidationError as e:
                return jsonify({"success": False, "log": e.message}), 400
            except:
                return jsonify({"success": False, "log": "Expected json"}), 400
            return f(*args, **kwds)
        return wrapper
    return decorator

def validate_query_params(*expected):
    """ Validates that the request has the specified query param args """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            for field in expected:
                if field not in request.args:
                    return jsonify({"success": False, "log": "%s not found in request query params" % (field)}), 400
            return f(*args, **kwds)
        return wrapper
    return decorator

def validate_authorization(f):
    """ Checks if the client's JWT is valid for auth purposes. Also may attempt to renew token, if it is set to expire soon. """
    @wraps(f)
    def wrapper(*args, **kwds):
        if ("AUTH_TOKEN" in request.cookies and is_jwt_valid(request.cookies.get("AUTH_TOKEN"))):
            returned = f(*args, **kwds) # toReturn may be a tuple of Flask return instance, and a HTTP return code
            if type(returned) is tuple:
                response = returned[0]
                http_code = returned[1]
            else:
                response = returned
                http_code = returned.status_code
            # check_and_renew(response, request.cookies.get("AUTH_TOKEN"))
            return response, http_code
        else:
            return jsonify({"success": False, "log": "UNAUTHORIZED"}), 401
    return wrapper