import os

def get_cos_creds():
    return {
        'photos': {
            'accessKeyId': os.environ['B2_COS_ACCESS_KEY_ID'],
            'secretAccessKey': os.environ['B2_COS_SECRET_ACCESS_KEY'],
            'endpoint': os.environ['B2_COS_ENDPOINT']
        },
        'videos': {
            'accessKeyId': os.environ['ORACLE_COS_ACCESS_KEY_ID'],
            'secretAccessKey': os.environ['ORACLE_COS_SECRET_ACCESS_KEY'],
            'endpoint': os.environ['ORACLE_COS_ENDPOINT'],
            's3ForcePathStyle': True,
            'signatureVersion': 'v4',
            'region': 'us-ashburn-1'
        }
    }