#!/usr/bin/python3
"""
    Create a new view for Amenity objects
"""
from models import storage
from models.amenity import Amenity
from flask import make_response, abort, request, jsonify
from api.v1.views import app_views

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenitites():
    """
        Retrieves the list of all Amenity objects
    """
    amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """
        Retrieves an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
        Deletes an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """
        Creates an Amenity
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
        Update an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if not amenity:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in amenity.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)