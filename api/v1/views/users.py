#!/usr/bin/python3
"""
    Creates a new view for the User objects
"""
from models import storage
from models.user import User
from flask import jsonify, make_response, abort, request
from api.v1.app import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
        Retrieves the list of all User objects
    """
    user = storage.all(User).values()
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
        Retrieves a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
        Deletes a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
        Creates a User
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")

    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
        Updates a User object
    """
    data = request.get_json()
    user = storage.get(User, user_id)

    if not user:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
