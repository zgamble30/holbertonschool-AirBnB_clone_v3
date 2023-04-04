#!/usr/bin/python3
"""
This script defines API endpoints for managing Place objects,
which are linked to City and User objects.
It includes routes for getting a list of places in a city,
getting a specific place by its ID, creating a new place in a city,
updating an existing place, and deleting a place.

The following routes are implemented:
- GET /cities/<city_id>/places:
    Retrieves a list of all Place objects linked to a
    City with the given city_id.
- GET /places/<place_id>:
    Retrieves a Place object with the given place_id.
- DELETE /places/<place_id>:
    Deletes a Place object with the given place_id and returns
    an empty dictionary with a status code of 200.
- POST /cities/<city_id>/places:
    Creates a new Place object linked to a City with the given city_id,
    and returns the new Place object with a status code of 201.
- PUT /places/<place_id>:
    Updates an existing Place object with the given place_id and
    returns the updated Place object with a status code of 200.

Each route has error handling for cases like non-existent city or place IDs,
missing or incorrect JSON data in the request, and attempts to modify
read-only attributes.

The script uses the Flask web framework, and the City and Place
objects are managed by a storage system.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<string:city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_get(city_id):
    """
    Retrieves list of all Place objects linked to a City.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        place_list = []
        # Iterate through Place objects associated w/ city obj
        for place in city.places:
            # Append dict representation of each Place obj to place_list
            place_list.append(place.to_dict())
        return jsonify(place_list)


@app_views.route("/places/<string:place_id>", methods=["GET"],
                 strict_slashes=False)
def place_id_get(place_id):
    """
    Retrieves an place with a given id
    Raise 404 error if id not linked to any Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def place_id_delete(place_id):
    """
    Deletes an Place object with a given id
    Raise 404 error if id not linked to any Place object
    Returns and empty dictionary with status code 200
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<string:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_post(city_id):
    """
    Creates an Place via POST
    If the HTTP body request is not valid JSON, raise 400 error: Not a JSON
    If the dictionary doesn't contain the key name, raise a 400 error with
    message Missing name
    Returns new Place with status code 201
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    # Retrieve JSON data sent in HTTP request body and store it as
    # a Python dictionary
    place_data = request.get_json()
    if place_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in place_data.keys():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if "name" not in place_data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    user = storage.get(User, place_data["user_id"])
    if user is None:
        abort(404)
    else:
        # If both city and user are found, a new Place obj is created
        # using Place(**place_data), which initializes the new Place obj w/
        # the key:value pairs from the place_data dict
        new_place = Place(**place_data)
        storage.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    Updates an Place object via PUT
    If the place_id is not linked to any Place object, raise 404 error
    If the HTTP body request is not valid JSON, raise a 400 error, Not a JSON
    Update the Place object with all key-value pairs of the dictionary
    Ignore keys: id, created_at, updated_at
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    # Check if HTTP request body contains valid JSON data
    # If not, error message: Not a JSON
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    # define ignore_keys to contain keys that should
    # not be updated in Place obj
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    # Iterate through key:value pairs in JSON data sent in HTTP request body
    for key, value in request.get_json().items():
        # Check if current key is not in ignore_keys list
        # If key is not in list, update corresponding attribute of Place obj
        # w/ new values: place, key, value
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
