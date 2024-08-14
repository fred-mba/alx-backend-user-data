#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Takes in a password string arguments and returns bytes
        """
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_pwd

    def register_user(self, email: str, password: str) -> User:
        """Registers a new_user with the given email and password arguments
           and return a User object.
        Raise:
            ValueError: If a user already exist with the passed email
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = self._hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_pwd)
            return new_user
