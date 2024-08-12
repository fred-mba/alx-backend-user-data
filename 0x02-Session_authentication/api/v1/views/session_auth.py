#!/usr/bin/env python3
"""
New view session authentication module
"""
import os
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """Handle login process using session authentication. If email/password
       is not provided, abort
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(getattr(user, 'id'))

    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
