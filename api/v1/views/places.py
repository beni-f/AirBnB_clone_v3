#!/usr/bin/python3
"""
    Creates a new view for the Place objects
"""
from models import storage
from models.place import Place
from flask import jsonify, make_response, request, abort
from api.v1.app import app_views