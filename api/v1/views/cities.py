#!/usr/bin/python3
"""
Handles all default RESTFul API actions for the State object
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                methods=['Get', 'POST'], strict_slashes=False)
def cities(state_id):
    """
    Creates City view to handle default RestFul API actions for the object
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
                    [val.to_dict() for val in state.cities])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        new_city = City(state_id=state_id, **post)
        new_city.save()
        return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<string:city_id>',
                methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object with specific id
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        city = storage.get('City', city_id)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(pu) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
                storage.save()
        return jsonify(city.to_dict()), 200
