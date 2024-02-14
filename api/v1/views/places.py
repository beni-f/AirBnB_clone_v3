#!/usr/bin/python3
"""
    Creates a new view for the Place objects
"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
        Retrieves the list of all Place objects
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
      Retrieves a Place object  
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
        Creates a Place
    """
    city = storage.get(City, city_id)
    data = request.get_json()

    if not city:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    
    place = Place(**data)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
        Updates a Place object
    """
    place = storage.get(Place, place_id)
    data = request.get_json()

    if not place:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    return make_response(jsonify(place.to_dict()), 200)