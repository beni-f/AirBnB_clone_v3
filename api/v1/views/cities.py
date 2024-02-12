#!/usr/bin/python3
"""
    Create a new view for City objects
"""
from models import storage
from models.state import State
from models.city import City
from flask import make_response, abort, jsonify, request
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
        Retrieves the list of all CIty objects of a State
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
        Retrieves a City object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
        Deletes a City object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
        Creates a City
    """
    data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    city = City(**data)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
        Updates a City object
    """
    data = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)