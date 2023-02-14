#!/usr/bin/python3
"""
Entry point to the API to return the status
"""
from os import getenv
from flask import Flask, jsonify, Blueprint
from models import storage
from api.vi.views import app_views

app = Flask(__name__)
app.register_blueprint(app.views)


@app.teardown_appcontext
def close_db_session(error):
    """
    closses current database session
    """
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
