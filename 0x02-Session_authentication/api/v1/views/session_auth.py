#!/usr/bin/env python3
"""
this module will handle all authentication routes
"""
from flask import jsonify, request
import os
from api.v1.views import app_views
from models.user import User


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False
)
def session_auth():
    """
    handle user authentication
    returns dictionary representation of the user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            respon = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            respon.set_cookie(session_name, session_id)
            return respon
        return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def logout_handler():
    """
    deletes a session, finish log out
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
