import jsonschema
from functools import wraps
from flask import jsonify, request

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