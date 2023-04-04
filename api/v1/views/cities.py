#!/usr/bin/python3
"""
This script defines API endpoints for managing City objects. 
It includes routes for getting a list of cities in a state,
getting a specific city by its ID, creating a new city in a state,
updating an existing city, and deleting a city.

The following routes are implemented:
- GET /states/<state_id>/cities:
    Returns a list of City objects associated with a state.
- GET /cities/<city_id>:
    Returns a specific City object by its ID.
- DELETE /cities/<city_id>:
    Deletes a City object by its ID.
- POST /states/<state_id>/cities:
    Creates a new City object associated with a state.
- PUT /cities/<city_id>:
    Updates a City object with the provided JSON data.

Each route has error handling for cases like non-existent state or city IDs, 
missing or incorrect JSON data in the request, and attempts to modify read-only attributes.

The script uses the Flask web framework, and the City and State objects are managed by a storage system.
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<string:state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities_in_state(state_id):
    """
    Returns list of cities with given state_id in JSON format
    if state_id doesn't exist, endpoint returns 404 error
    """
    state = storage.get(State, state_id)
    city_list = []
    if state is None:
        abort(404)
    for city in state.cities:
        city_list.append(city.to_dict())
    return make_response(jsonify(city_list))


@app_views.route("/cities/<string:city_id>", methods=["GET"],
                 strict_slashes=False)
def city_id_get(city_id):
    """
    Returns City info w/ given city_id in JSON format
    if city_id doesn't exits, endpoint returns 404 error
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return make_response(jsonify(city.to_dict()))


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_id_delete(city_id):
    """
    Deletes a City object w/ given city_id & returns empty JSON object
    w/ status code 200
    if city_id doesn't exits, endpoint returns 404 error
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<string:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_post(state_id):
    """
    Creates new city object w/ given state_id & returns new city's
    data as a JSON object.
    """
    state = storage.get(State, state_id)
    # Extract JSON data sent in HTTP POST request and convert
    # to a python dict, & store it in city_data variable
    city_data = request.get_json()
    if state is None:
        abort(404)
    if not city_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in city_data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    # Create new city object using data from city_data dict
    # Using '**' to unpack the dict and pass its key-value pairs as
    # keyword args to City constructor
    new_city = City(**city_data)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=["PUT"],
                 strict_slashes=False)
def city_put(city_id):
    """
    Updates City w/ given city_id using provided JSON data
    Returns updated city's data as JSON object.
    If city_id doesn't exit, return 404 error
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    # Ignore these keyes when updating the City object
    # These attributes should not be modified: id, created_at, updated_at
    ignore_keys = ["id", "created_at", "updated_at"]
    # Iterate over key/val pairs  of JSON data sent in PUT request
    for key, value in request.get_json().items():
        # If current key not in ignore_keys list, set corresponding
        # attribute of city object to value provided in JSON data.
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
