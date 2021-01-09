import jwt
import os
from datetime import datetime, timedelta

secret=os.environ.get('JWT_RANDOM_SECRET')

def produce_jwt() -> str:
    """
    Produces jwt as a utf-8 str for the given username.
    JWT expires in 2 hours!
    All auth handled through this API so Symmetric encryption HS256 fine for now.
    """
    return jwt.encode({'exp': datetime.utcnow() + timedelta(hours=2)}, secret, algorithm='HS256').decode('utf-8')

def is_jwt_valid(token: str) -> bool:
    """ Checks if a JWT is valid """
    try:
        jwt.decode(token.encode('utf-8'), secret, algorithms=['HS256'])
        return True
    except (jwt.InvalidTokenError, jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        print(e)
        return False
