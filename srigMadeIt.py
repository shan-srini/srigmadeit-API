import sys
from flask import Flask, jsonify
from flask_cors import CORS
from app.db.create_mongo import create_db

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:1234"])

from app.routes.events_api import events_api
from app.routes.categories_api import categories_api
from app.routes.photos_api import photos_api
app.register_blueprint(events_api, url_prefix="/api")
app.register_blueprint(categories_api, url_prefix="/api")
app.register_blueprint(photos_api, url_prefix="/api")

@app.route('/', methods=['GET'])
def hello():
    return 'bonjour', 200

if __name__ == '__main__':
    # if len(sys.argv) == 2 and sys.argv[1] == 'create_db':
    #     create_db()
    app.run()