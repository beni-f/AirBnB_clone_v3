#!/usr/bin/python3
"""
    Creates a new view for the Place objects
"""
from models import storage
from models.place import Place
from models.city import City
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

@app_views.route
