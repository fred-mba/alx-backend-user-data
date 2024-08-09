#!/usr/bin/env python3
"""
Module to manage all authetication system.
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Manage authentication system.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return boolean value
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Return None
           request: Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return None
           request: Flask request oject
        """
        return None
