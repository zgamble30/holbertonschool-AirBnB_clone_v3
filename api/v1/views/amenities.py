#!/usr/bin/python3
"""
Module that creates view for Amenity objects handling default
RESTful API actions
"""
# Imports app_views blueprint
from api.v1.views import app_views
# Import necessary Flask modules
from flask import jsonify, abort, request, make_response
# Imports storage engine and Amenity model from models module
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/", methods=["GET"],
                 strict_slashes=False)
# Defines a function that handles GET requests to /Amenities/
def amenities_get():
    """
    Retrieves list of all Amenity objects.
    """
    all_amenities = storage.all(Amenity)
    amenity_list = []
    for amenity in all_amenities.values():
        amenity_list.append(amenity.to_dict())
    return make_response(jsonify(amenity_list), 200)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_id_get(amenity_id):
    """
    Retrieves an amenity with a given id
    Raise 404 error if id not linked to any Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_id_delete(amenity_id):
    """
    Deletes an Amenity object with a given id
    Raise 404 error if id not linked to any Amenity object
    Returns and empty dictionary with status code 200
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities/", methods=["POST"],
                 strict_slashes=False)
def amenity_post():
    """
    Creates an Amenity via POST
    If the HTTP body request is not valid JSON, raise 400 error, Not a JSON
    If the dictionary doesn't contain the key name, raise a 400 error with
    message Missing name
    Returns new Amenity with status code 201
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_put(id):
    """
    Updates an Amenity object via PUT
    If the amenity_id is not linked to any Amenity object, raise 404 error
    If the HTTP body request is not valid JSON, raise a 400 error, Not JSON
    Update Amenity object with all key-value pairs of the dictionary
    Ignore keys: id, created_at, updated_at
    """
    print("i am here")
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        amenity = storage.get(Amenity, id)
        if amenity is None:
            abort(404)
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in req_dict.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
