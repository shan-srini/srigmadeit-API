import os

def get_cos_creds():
    return {
        'accessKeyId': os.environ['COS_ACCESS_KEY_ID'],
        'secretAccessKey': os.environ['COS_SECRET_ACCESS_KEY'],
        'endpoint': os.environ['COS_ENDPOINT']
    }