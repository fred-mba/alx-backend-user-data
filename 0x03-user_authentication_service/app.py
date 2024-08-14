#!/usr/bin/env python3
"""Basic flask app module
"""
from user import User
from flask import Flask, request, jsonify, make_response, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def basic_flask():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """An end-point to register a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify(
            {"email": "{new_user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Logs in the user by validating credentials before creating a session
       for the user, and store session ID as a cookie with key "session_id"
       on the response and a JSON payload form.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    if not AUTH.valid_login(email=email, password=password):
        abort(401)
    session_id = AUTH.create_session(email=email)
    if not session_id:
        abort(401)

    response = make_response(
        jsonify({"email": "{email}", "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.rout('/sessions', methods=['DELETE'])
def logout():
    """Find the user with the requested session ID. If the user exists destroy
       the session and redirect the user to GET /. Otherwise respond with a 403
       HTTP status.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)

    # Create a redirection response to home page
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
