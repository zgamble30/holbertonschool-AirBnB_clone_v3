#!/usr/bin/python3
"""
Index route for API V1
"""
from api.v1.views import *
from flask import Flask, jsonify

app_views = Flask(__name__)
app_views.url_map.strict_slashes = False


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns status: OK """
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns number of each endpoint in storage"""
    from models import storage
    cls_dict = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    return_dict = {}
    for key, value in cls_dict.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)

if __name__ == "__main__":
    pass
