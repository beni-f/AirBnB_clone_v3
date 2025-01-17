#!/usr/bin/python3
"""
    Create a new view for State objects
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, abort, request, jsonify, make_response

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
        Retrieves the list of all State objects
    """
    states = storage.all(State).values()
    list_states = []
    for state in states:
            list_states.append(state.to_dict())
    return jsonify(list_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """
        Retrieves a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())
                         
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
        Deletes a State object
    """
    state = storage.get(State, state_id)

    if not state:
         abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """
        Creates a State
    """
    data = request.get_json()
    if not data:
         abort(400, description="Not a JSON")
    if 'name' not in data:
         abort(400, description="Missing name")
        
    state = State(**data)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
        Updates a State object
    """
    state = storage.get(State, state_id)
    data = request.get_json()

    if not state:
        abort(404)
    if not data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
