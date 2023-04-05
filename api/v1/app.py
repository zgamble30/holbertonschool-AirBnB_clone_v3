#!/usr/bin/python3
"""Flask App"""
import os
from flask import Flask, jsonify
from api.v1.views import app_views


# create an instance of Flask
app = Flask(__name__)
app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port)
