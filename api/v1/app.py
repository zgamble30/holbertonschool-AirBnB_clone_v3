#!/usr/bin/python3
"""
    Entry point for the API
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exception):
    """Calls storage close"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Returns JSON 404 status"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True)
