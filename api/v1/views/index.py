#!/usr/bin/python3
"""
Index module to create routes on app_views objects.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Return OK status"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats_route():
    """
    Retrieve number of each objects by the type
    """
    count_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(count_dict)
