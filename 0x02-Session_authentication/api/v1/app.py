#!/usr/bin/env python3
"""
Route module for the API
This module sets up the Flask application, configures CORS, and
handles authentication for the API routes.
It also includes error handling for common HTTP errors such as 404
(Not Found), 401 (Unauthorized), and 403 (Forbidden).
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def before_req():
    """
    This function is executed before each
    request to handle authentication.
    If authentication is required for the
    requested path and the user is not authenticated,
    the appropriate error response
    is returned (401 Unauthorized or 403 Forbidden).
    """
    if auth is None:
        pass
    else:
        setattr(request, 'current_user', auth.current_user(request))
        excluded = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
            ]
        if auth.require_auth(request.path, excluded):
            cookie = auth.session_cookie(request)
            if auth.authorization_header(request) is None and cookie is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handler for 404 Not Found errors.
    Returns a JSON response with an error message.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(e) -> str:
    """
    Handler for 401 Unauthorized errors.
    Returns a JSON response with an error message.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(e) -> str:
    """
    Handler for 403 Forbidden errors.
    Returns a JSON response with an error message.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
