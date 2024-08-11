#!/usr/bin/env python3
"""
Module to manage all authetication system.
"""
import os
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Manage authentication system.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if auth is required for the give path.

           Parameters
           ----------
           path(str): Path to check.
           excluded_paths(List[str]): A list of paths that do ot require auth

           Return True if authentication is required, else False
        """
        if path is None:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True

        # Ensure the path is slash-tolerant
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                base_path = excluded_path[:-1]

                if path.startswith(base_path):
                    return False

            if excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Parameters
           ----------
           request: Flask request object
           Returns the value of the authorization header, or None if it does
           not contain the header.
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """Return None
           request: Flask request object
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Returns a cookie value from a request
        """
        cookie_name = os.getenv('SESSION_NAME')

        if request is None:
            return None
        return request.cookies.get(cookie_name)
