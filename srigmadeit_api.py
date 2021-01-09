import sys
import os
import re
from flask import Flask, jsonify
from flask_cors import CORS
from app.db.create_mongo import create_db
from flask_compress import Compress

app = Flask(__name__)
Compress(app)
CORS(app, supports_credentials=True, origins=[re.compile("https://(www.)?srigmadeit.com"), "http://192.168.1.202:1234"])

from app.routes.events_api import events_api
from app.routes.categories_api import categories_api
from app.routes.media_api import media_api
from app.routes.srig_manage_api import srig_manage_api
app.register_blueprint(events_api)
app.register_blueprint(categories_api)
app.register_blueprint(media_api)
app.register_blueprint(srig_manage_api)

@app.route('/', methods=['GET'])
def hello():
    return 'bonjour', 200

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'create_db':
        create_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    # app.run(port=5000, debug=True)