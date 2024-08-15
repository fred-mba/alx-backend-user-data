#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Take in a password string arguments and return bytes
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
        """Register a new_user with the given email and password arguments
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
        """Validate the user's credentials and return True if it matches,
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
        """Take an email string argument and return the session ID
           as a string.
           Find the user corresponding to the email and generates a new UUID,
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

    def get_user_from_session_id(self, session_id: str) -> User:
        """Find user by session_id. If the session ID is None or no user is
           found, return None. Otherwise return the corresponding user.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Delete a session based on user_id by setting session_id to None.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token by finding the user corresponding
           to the email. If the user exist, generate a UUID and update the
           user's reset_token db field
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            user.reset_token = reset_token
            self._db._session.commit()

            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password by taking the reset_token and password argument
           If it does not exist, raise a ValueError exception.Otherwise,
           hash the password and update the user’s hashed_password field
           with the new hashed password and the reset_token field to None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        user.hashed_password = hashed_password
        user.reset_token = None

        self.db_session.commit()
