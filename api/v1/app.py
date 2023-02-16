#!/usr/bin/python3
"""
Entry point to the API to return the status
"""
from os import getenv
from flask import Flask, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)
CORS(app_views)


@app.teardown_appcontext
def close_db_session(error):
    """
    closses current database session
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """
    Custom 404 error handler in JSON format
    """
    return({'error': 'Not found!'}), 404


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True, debug=True)
