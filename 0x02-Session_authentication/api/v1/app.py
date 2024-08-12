#!/usr/bin/env python3
"""
Route module for the API
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

auth_type = getenv('AUTH_TYPE')

# If  auth type is session_auth, import SessionAuth and create instance of it
if auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

# If auth type is basic_auth, import BasicAuth and create instance of it
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

# Otherwise, follow the previous mechanism by creating instance of `Auth`
elif auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request_func():
    """Execute this function before any request is made
    """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/',
        '/api/v1/auth_session/login/']

    if not auth.require_auth(request.path, excluded_paths):
        return

    user = auth.current_user(request)

    if auth.authorization_header(request) is None and \
            auth.session_cookie(request) is None:
        abort(401)

    if user is None:
        abort(403)
    request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Error handler: Unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Error handler: Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
