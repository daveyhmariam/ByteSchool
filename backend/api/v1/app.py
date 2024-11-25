#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.basic_auth import BasicAuth
import os
from flasgger import Swagger


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
swagger = Swagger(app)
auth = BasicAuth()



@app_views.route('/docs', methods=['GET'], strict_slashes=False)
def documentation():
    """Get Swagger UI documentation.
    Returns:
        Swagger UI for the API.
    """
    return swagger.ui() 

app.register_blueprint(app_views)




@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def authenticate():
    """
    Authentication
    """
    if auth:
        excluded = [
            '/byteschool/users/register',
            '/docs',
            '/flasgger_static/*',
            '/apidocs/*',
            '/apidocs',
            '/apispec_1.json'
        ]
        require_auth = auth.require_auth(request.path, excluded)
        if require_auth:
            if not auth.authorization_header(request):
                abort(401)
            if not auth.current_user(request):
                abort(403)
        request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    with app.app_context():
        print(app.url_map)

    app.run(host=host, port=port, debug=True)
