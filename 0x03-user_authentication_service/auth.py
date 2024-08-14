#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Takes in a password string arguments and returns bytes
    """
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    """Return a string representantion of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new_user with the given email and password arguments
           and return a User object.
        Raise:
            ValueError: If a user already exist with the passed email
            NoResultFound:
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")

        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Verifies user's credentials and return True if it matches,
           Otherwise False

           Parameters
           ----------
           password: The plaintext password to be verified.
           email: email to relocate the user
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Takes an email string argument and returns the session ID
           as a string.
           Finds the user corresponding to the email and generates a new UUID,
           stores it in the db as the user's session_id.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None
