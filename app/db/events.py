# Collection events operations
from app.util import mongo as mongo_util
import uuid

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
            _id = str(uuid.uuid4()) # pretty much using uuid cause bson String = cooler than ObjectID type :p
            event = {
                '_id': _id,
                Event.keys['name']: name,
                Event.keys['timestamp']: timestamp
            }
            res = collection.insert_one(event)
            return str(res.inserted_id)
        except:
            # handle not unique event name
            raise Exception

    def get(start = 0, size = 25):
        ''' Gets some events '''
        collection = get_collection()
        events = collection.find({}, skip = start, limit = size).sort("$natural", -1)
        return events # NOTICE RETURNS CURSOR

    def delete(event_id):
        # Going to need to delete all categories, and all nested pictures, then return 
        # a list of deleted picture ids to cleanup the COS
        return True
