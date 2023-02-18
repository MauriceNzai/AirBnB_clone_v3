#!/usr/bin/python3
"""
Handles all default RESTFul API actions for the Place object
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<string:city_id>/places',
                 methods=['Get', 'POST'], strict_slashes=False)
def places(city_id):
    """
    Creates Place view to handle default RestFul API actions for the object
    """
    city = storage.get('City', city_id)
    print(city)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in city.places])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        elif post.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif storage.get('User', post.get('user_id')) is None:
            abort(404)
        new_place = Place(city_id=city_id, **post)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a city object with a specific id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place = storage.get('Place', place_id)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'city_id', 'user_id']:
                setattr(place, key, value)
                storage.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of
    the JSON in the body of the request
    """
    body_r = request.get_json()
    if body_r is None:
        abort(400, "Not a JSON")

    if not body_r or (
            not body_r.get('states') and
            not body_r.get('cities') and
            not body_r.get('amenities')
    ):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []

    if body_r.get('states'):
        states = [storage.get("State", id) for id in body_r.get('states')]

        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if body_r.get('cities'):
        cities = [storage.get("City", id) for id in body_r.get('cities')]

        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if body_r.get('amenities'):
        ams = [storage.get("Amenity", id) for id in body_r.get('amenities')]
        i = 0
        limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
        while i < limit:
            place = places[i]
            url = first_url + '{}/amenities'
            req = url.format(place.id)
            response = requests.get(req)
            am_d = json.loads(response.text)
            amenities = [storage.get("Amenity", o['id']) for o in am_d]
            for amenity in ams:
                if amenity not in amenities:
                    places.pop(i)
                    i -= 1
                    limit -= 1
                    break
            i += 1
    return jsonify([place.to_dict() for place in places])
