# Collection categories operations

# Categories are sections within an event
# An event has one or many categories

from app.util import mongo as mongo_util

collection_name = "categories"

def create(mongo_db):
    ''' Create collection '''
    collection = mongo_db[collection_name]
    collection.create_index([('event', 1), ('priority', 1)], sparse=True)
    print('--- {} collection lazily created'.format(collection_name))

def get_collection(mongo_db = mongo_util.get_db()):
    return mongo_db[collection_name]

class Category:
    keys = {
        'id': '_id',
        'name': 'category',
        'priority': 'priority',
        'event_id': 'event'
    }

    def save(event_id: str, category_name: str, priority: int) -> str:
        ''' Saves a document under a specified event and returns the assigned id '''
        collection = get_collection()
        try:
            to_insert = {
                Category.keys['name']: category_name,
                Category.keys['event']: event_id,
                Category.keys['priority']: priority
            }
            res = collection.insert_one(to_insert)
            return str(res.inserted_id)
        except BaseException as e:
            raise str(e)

    def get(event_id: str) -> list:
        ''' The only access pattern is to get all categories by the given event ''' 
        collection = get_collection()
        results = collection.find({Category.keys['event_id']: event})
        return list(results)

    def delete(category: str):
        # Delete and also call delete in photos collection for all photos under this category
        # Might also need to return a list of all photo ids to delete to the UI so it can delete from COS
        return True