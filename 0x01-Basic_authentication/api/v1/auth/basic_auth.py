#!/usr/bin/env python3
"""
Basic auth module
"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Returns a tuple containing the user email and password from the
           Base64 decoded value else, (None, None) if extraction fails.

           Parameters
           ----------
           decoded_base64_authorization_header(str): The decoded Base64 string
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password if
        successfull, None if it fails
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                user = User.search({'email': user_email})

            except Exception:
                return None

            if not user:
                return None

            if user[0].is_valid_password(user_pwd):
                return user[0]

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request
           1. Gets the authorization header
           2. Exctract the Base64 section from the auth header
           3. Decode the Base64 to get the user credentials
           4. Exctract the user email and password from the decoded string
           5. Get the current user object based on the extracted email and pwd

           Parameters
           ----------
           request: Request object that contains the authorization header.

           Returns the user is the auth is successfull, None if it fails
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        email, password = self.extract_user_credentials(decoded_header)
        if email is None or password is None:
            return None

        user = self.user_object_from_credentials(email, password)
        return user
