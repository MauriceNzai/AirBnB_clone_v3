#!/usr/bin/python3
"""
index page of the API
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint
from models.state import State
from models import stroage

@app_views.route('/status', method=['GET'], strict_slashes=False)
def get_status():
    """
    Returns the status of the API
    """
    return jsonify({'status': 'OK'})

