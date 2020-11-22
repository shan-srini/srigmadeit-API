# Collection events operations
from app.util import mongo as mongo_util

collection_name = "events"

def create(mongo_db):
    ''' Create collection '''
    collection = mongo_db[collection_name]
    collection.create_index([('name', 1)], sparse=True, unique=True)
    print('--- {} collection lazily created'.format(collection_name))

def get_collection(mongo_db = mongo_util.get_db()):
    return mongo_db[collection_name]

class Event:
    keys = {
        'name': 'name',
        'timestamp': 'timestamp',
        'profile': 'profile'
    }

    def save(name: str, timestamp: int) -> str:
        ''' Accepts an event name, epoch int timestamp -> ObjectId '''
        collection = get_collection()
        try:
            event = {
                Event.keys['name']: name,
                Event.keys['timestamp']: timestamp
            }
            res = collection.insert_one(event)
            return str(res.inserted_id)
        except:
            raise Exception

    def get(start = 0, size = 25):
        ''' Gets some events '''
        collection = get_collection()
        events = collection.find({}, {'_id': 0}, skip = start, limit = size)
        return list(events)

    def delete(event_id):
        # Going to need to delete all categories, and all nested pictures, then return 
        # a list of deleted picture ids to cleanup the COS
        return True
