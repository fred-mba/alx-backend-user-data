#!/usr/bin/env python3
"""
Basic auth module
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic auth class that inherits from Auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header for a
        Basic Authentication.

        Parameters
        ----------
        authorization_header(str): The authorization header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 a UTF-8 string, None if
           decoding fails

           Parameteres
           -----------
           base64_authorization_header(str): The base64 auth header to decode
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_string = base64.b64decode(base64_authorization_header)
            return decoded_string.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
