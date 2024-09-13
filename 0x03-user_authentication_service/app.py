#!/usr/bin/env python3
"""
the factory for my flask app
"""
from flask import redirect, url_for, make_response
from flask import Flask, jsonify, request, abort
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Handles GET requests to the root route.
    Returns:
        jsonify: A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    Handles POST requests to the /users route for user registration.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    auth = Auth()
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        response = make_response(
            jsonify({'email': email, 'message': 'logged in'})
        )
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logout by deleting the session.
    Retrieves the session ID from
    the request's cookies and destroys the session.
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        auth = Auth()
        user = auth.find_user_by(session_id=session_id)
        if user:
            auth.destroy_session(user.id)
            return redirect(url_for('index'))
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Respond to GET profile request.
    """
    session_id = request.cookies.get('session_id')
    auth = Auth()

    try:
        user = auth._db.find_user_by(session_id=session_id)
    except NoResultFound:
        abort(403)  # User not found, return a 403 Forbidden error

    if user and session_id:
        response = make_response(jsonify({"email": user.email}), 200)
        return response

    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
