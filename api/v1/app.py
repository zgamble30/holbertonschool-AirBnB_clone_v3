#!/usr/bin/python3
""" app.py: Main Flask application file """
from flask import Flask, jsonify
from os import environ
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
# app_views is a Flask blueprint used to group & organize the
# different routes & views of your application.
# This registers the blueprint w/ Flask app instance 'app'.
# This tells Flask to include routes & views defined in app_views
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception=None):
    """
    Close the storage connection.
    This function is called when the app context is torn down.
    It ensures that the storage connection is properly closed.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handle 404 errors, returning a JSON-formatted response. """
    return jsonify({"error": "Not Found"}), 404


if __name__ == '__main__':
    """
    Run the Flask server w/ specified host, port, & threaded option.
    The host and port are retrieved from environment variables if available,
    otherwise, default values are used.
    """
    # These 2 lines retrieve the value of the environment variables & assign
    # it to host/port variables. If env var not defined,
    # default to 0.0.0.0/5000.
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = environ.get("HBNB_API_PORT", 5000)
    # This line runs Flask server w/ host/port values from env vars or default
    # Enables multi-threading, allowing handling of
    # multiple requests concurrently.
    app.run(host=host, port=port, threaded=True)
