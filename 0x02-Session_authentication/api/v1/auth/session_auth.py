#!/usr/bin/env python3
"""
Session Authentication Module
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Session Authentication Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates session ID and stores in user_id_by_session_id class
        attribute.
        Returns generated session ID string or None if user_id is None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Returns a User instance based on a cookie value
           Parameter
           --------
           request: Will contain the session_cookie ID. It will use this
           to identify the user.
           Steps:
           1. Request the session_id from the cookie
           2. Retrieve the user_id from the session_id
           3. Retrieve thr user instance from the db using user_id
        """
        session_id = self.session_cookie(request)

        user_id = self.user_id_for_session_id(session_id)

        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Delete the user session (logs out the user)
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if session_id is None or user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            # return self.user_id_by_session_id.pop(session_id, True)
            del self.user_id_by_session_id[session_id]
        return True
