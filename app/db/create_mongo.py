import os
from app.db import categories
from app.db import events
from app.db import media
import app.util.mongo as mongo_util


def create_db():
    db_name = os.environ.get('DB_NAME')
    client = mongo_util.get_client()
    # Drop and create db if needed
    if db_name in client.list_database_names():
        confirm_drop = ''
        while confirm_drop not in ['y', 'n']:
            confirm_drop = input('{} database exists. Confirm whether or not to drop database\ny to drop, n to retain\n')
            if confirm_drop == 'y':
                client.drop_database(db_name)
                print("- {} database dropped".format(db_name))
                # Lazily create database and collections
                db = client[db_name]
                categories.create(db)
                events.create(db)
                media.create(db)
    print('---- success')