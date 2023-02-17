#!/usr/bin/python3
"""
Handles all default RESTFul API actions for the User object
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['Get', 'POST'], strict_slashes=False)
def users():
    """
    Creates User view to handle default RestFul API actions for the object
    """
    if request.method == 'GET':
        all_users = []
        users = storage.all('User').values()
        for user in users:
            all_users.append(user.to_json())
        return jsonify(all_users)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('email') is None:
            return jsonify({'error': 'Missing email'}), 400
        elif post.get('password') is None:
            return jsonify({'error': 'Missing password'}), 400
        new_user = User(**post)
        new_user.save()
        new_user = user.to_json()
        return jsonify(new_user), 201

@app_views.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves User object with specific id
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user = user.to_json()
    return jsonify(user)

@app_views.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User with given id
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users/<string:user_id>', methods=['PUT'])
def new_user(user_id):
    """
    Adds new User object
    """
    new_user = storage.get('User', user_id)
    if new_user is None:
        abort(404)
    data = request.get_json()
    if data is None or type(data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(new_user, key, value)
        new_user.save()
        return jsonify(new_user.to_dict()), 200
