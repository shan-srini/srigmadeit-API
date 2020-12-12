# Collection photos operations
from app.util import mongo as mongo_util
import uuid

collection_name = "media"

def create(mongo_db):
    ''' Create collection '''
    collection = mongo_db[collection_name]
    collection.create_index([('category', 1)], sparse=True)
    print('--- {} collection lazily created'.format(collection_name))

def get_collection(mongo_db = mongo_util.get_db()):
    return mongo_db[collection_name]

class Media:
    ''' Class to interact with media collection '''
    keys = {
        'id': '_id',
        'category_id': 'category',
    }

    def save(category_id: str, count: int) -> str:
        ''' Saves a document under a specified category_id and returns the assigned id '''
        collection = get_collection()
        try:
            to_insert = [{'_id': str(uuid.uuid4()), 'category': category} for ii in range(count)]
            res = collection.insert_many(to_insert)
            return res.inserted_ids
        except:
            raise Exception

    def get(category_id: str, size = 25, start = 0) -> list:
        ''' Only access pattern is to get an x number of documents under a certain category '''
        collection = get_collection()
        media = collection.find({"category": category_id}, skip=start, limit=size)
        return list(media)

    def delete(media_id: str):
        # Need to decide if I should let UI delete from COS or do it on API side?
        # Probably gonna do it on UI side for consistency, though I'm not a fan of it :/
        return True