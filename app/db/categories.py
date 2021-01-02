# Collection categories operations

# Categories are sections within an event
# An event has one or many categories

from app.util import mongo as mongo_util
import uuid

collection_name = "categories"

def create(mongo_db):
    ''' Create collection '''
    collection = mongo_db[collection_name]
    collection.create_index([('name', 1), ('order', 1)], sparse=True)
    print('--- {} collection lazily created'.format(collection_name))

def get_collection(mongo_db = mongo_util.get_db()):
    return mongo_db[collection_name]

class Category:
    keys = {
        'id': '_id',
        'name': 'name',
        'order': 'order',
        'event': 'event'
    }

    def save(event_id: str, category_name: str, order: int = 0) -> str:
        ''' Saves a document under a specified event and returns the assigned id '''
        collection = get_collection()
        try:
            to_insert = {
                Category.keys['id']: str(uuid.uuid4()),
                Category.keys['name']: category_name,
                Category.keys['event']: event_id,
                Category.keys['order']: order
            }
            res = collection.insert_one(to_insert)
            return str(res.inserted_id)
        except BaseException as e:
            raise str(e)

    def get(event_id: str) -> list:
        ''' The only access pattern is to get all categories by the given event ''' 
        collection = get_collection()
        results = collection.find({Category.keys['event']: event_id}, {Category.keys['event']: 0}).sort(Category.keys['order'])
        return list(results)

    def update_meta(category_id: str, request_update: dict) -> bool:
        ''' Updates a single category, returns True if a category was updated '''
        collection = get_collection()
        update_body = {}
        if Category.keys['name'] in request_update:
            update_body[Category.keys['name']] = request_update.get(Category.keys['name'])
        if Category.keys['order'] in request_update:
            update_body[Category.keys['order']] = request_update.get(Category.keys['order'])
        ret = collection.update_one({Category.keys['id']: category_id}, update_body)
        return ret.modified_count == 1

    def delete(event_id: str = None, category_id: str = None):
        collection = get_collection()
        delete_query = {}
        if (event_id):
            delete_query[Category.keys['event']] = event_id
        result = collection.delete_many(delete_query)
        return result.deleted_count > 0