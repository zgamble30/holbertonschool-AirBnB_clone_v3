#!/usr/bin/python3
"""
Index view for API
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
    Returns a JSON object with the status of the API
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """
    Retrieves the number of each objects by type
    """
    classes = {
        "Amenity": storage.count("Amenity"),
        "City": storage.count("City"),
        "Place": storage.count("Place"),
        "Review": storage.count("Review"),
        "State": storage.count("State"),
        "User": storage.count("User")
    }
    return jsonify(classes)
