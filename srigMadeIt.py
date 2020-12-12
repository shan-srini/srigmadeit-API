import sys
from flask import Flask, jsonify
from flask_cors import CORS
from app.db.create_mongo import create_db

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://192.168.1.202:1234"])

from app.routes.events_api import events_api
from app.routes.categories_api import categories_api
from app.routes.media_api import media_api
from app.routes.srig_manage_api import srig_manage_api
app.register_blueprint(events_api, url_prefix="/api")
app.register_blueprint(categories_api, url_prefix="/api")
app.register_blueprint(media_api, url_prefix="/api")
app.register_blueprint(srig_manage_api, url_prefix="/api")

@app.route('/', methods=['GET'])
def hello():
    return 'bonjour', 200

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'create_db':
        create_db()
    app.run(host='0.0.0.0', port=5000, debug=True)