# Collection photos operations
from app.util import mongo as mongo_util
import uuid

collection_name = "photos"

def create(mongo_db):
    ''' Create collection '''
    colletion = mongo_db[collection_name]
    collection.create_index([('category', 1)], sparse=True)
    print('--- {} collection lazily created'.format(collection_name))

def get_collection(mongo_db = mongo_util.get_db()):
    return mongo_db[collection_name]

class Photo:
    ''' Class to interact with photos collection '''
    keys = {
        'id': '_id',
        'category': 'category',
        'event': 'event'
    }

    def save(event:str, category: str) -> str:
        ''' Saves a document under a specified event/category and returns the assigned id '''
        collection = get_collection()
        try:
            _id = str(uuid.uuid4())
            res = collection.insert_one({'_id': _id, 'event': event, 'category': category})
            return str(res.inserted_id)
        except:
            raise Exception

    def get(category: str, size = 25, start = 0) -> list:
        ''' Only access pattern is to get an x number of documents under a certain category '''
        collection = get_collection()
        photos = collection.find({"category": category}, skip=start, limit=size)
        return list(photos)

    def delete(photo_id: str):
        # Need to decide if I should let UI delete from COS or do it on API side?
        # Probably gonna do it on UI side for consistency, though I'm not a fan of it :/
        return True