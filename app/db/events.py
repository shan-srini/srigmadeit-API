# Collection events operations
from app.util import mongo as mongo_util
from datetime import datetime, timedelta
import re

collection_name = "events"

def create(mongo_db):
    ''' Create collection '''
    collection = mongo_db[collection_name]
    collection.create_index([('name', 1), ('timestamp', -1)], sparse=True, unique=True)
    print('--- {} collection lazily created'.format(collection_name))

def get_collection(mongo_db = mongo_util.get_db()):
    return mongo_db[collection_name]

class Event:
    keys = {
        'name': 'name',
        'timestamp': 'timestamp',
    }

    def save(name: str, timestamp: int) -> str:
        ''' Accepts an event name, epoch int timestamp -> ObjectId '''
        collection = get_collection()
        try:
            _id = name + (datetime.fromtimestamp(timestamp) + timedelta(days=1)).strftime("%m-%d-%y") # timestamp(april 21, 2000) -> 04-21-2000
            event = {
                '_id': _id,
                Event.keys['name']: name,
                Event.keys['timestamp']: timestamp
            }
            res = collection.insert_one(event)
            print(res)
            return str(res.inserted_id)
        except:
            # handle not unique event name
            return False

    def get(start = 0, size = 25, search_name = None):
        ''' Gets some events '''
        collection = get_collection()
        query: dict = {}
        if search_name:
            query.update({Event.keys['name']: re.compile(search_name, re.IGNORECASE)})
        events = collection.find(query, skip = start, limit = size).sort("timestamp", -1)
        return events # NOTICE RETURNS CURSOR
    
    def get_meta(event_id: str):
        collection = get_collection()
        return collection.find_one({'_id': event_id})


    def delete(event_id: str) -> bool:
        collection = get_collection()
        result = collection.delete_one({'_id': event_id})
        return result.deleted_count == 1
