#!/usr/bin/python3
"""
Index view for API
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """
    Return a JSON-formatted status response
    """
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    """
    Return a JSON-formatted stats response
    """
    from models import storage
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
