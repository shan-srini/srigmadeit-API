# Collection photos operations
from app.util import mongo as mongo_util
import uuid

collection_name = "media"

def create(mongo_db):
    ''' Create collection '''
    collection = mongo_db[collection_name]
    collection.create_index([('category', 1), ('event', 1)], sparse=True)
    print('--- {} collection lazily created'.format(collection_name))

def get_collection(mongo_db = mongo_util.get_db()):
    return mongo_db[collection_name]

class Media:
    ''' Class to interact with media collection '''
    keys = {
        'id': '_id',
        'event_id': 'event',
        'category_id': 'category',
        'source': 'source'
    }

    def save(event_id: str, category_id: str, count: int, source: str, request_id: str = None) -> str:
        ''' Saves a document under a specified category_id and returns the assigned id '''
        collection = get_collection()
        # try:
        to_insert_id = str(request_id if request_id else str(uuid.uuid4())) # Videos have pre created unique ids, photos require id creation
        to_insert = [{'_id': to_insert_id, Media.keys['event_id']: event_id, Media.keys['category_id']: category_id, Media.keys['source']: source} for ii in range(count)]
        res = collection.insert_many(to_insert)
        return res.inserted_ids
        # except:
        #     raise Exception

    def get(category_id: str = None, event_id = None, size = 25, start = 0, reverse = False):
        collection = get_collection()
        query = {}
        if category_id:
            query[Media.keys['category_id']] = category_id
        elif event_id:
            query[Media.keys['event_id']] = event_id
        media = collection.find(query, skip=start, limit=size)
        if reverse:
            media.sort([('$natural', -1)])
        return media # NOTICE RETURNS CURSOR

    def delete(media_id: str = None, event_id: str = None) -> dict:
        ''' deletes media and returns the ids of the media deleted '''
        collection = get_collection()
        delete_query = {}
        if (event_id):
            delete_query[Media.keys['event_id']] = event_id
        removed = collection.find(delete_query)
        delete_result = collection.delete_many(delete_query)
        return removed