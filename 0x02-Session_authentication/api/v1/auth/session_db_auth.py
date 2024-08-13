#!/usr/bin/env python3
"""Sessions in database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth stores session info in the db
    """
    def create_session(self, user_id=None):
        """Create and store session in the db.
        """
        sesssion_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(**kwargs)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user_id based on the session ID stored in the db.
        """
        if session_id is None:
            return None

        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy user_session from the db based on the session ID.
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_session = UserSession.search("session_id": session_id)
        if not user_session:
            return False

        user_session.remove()
        return True
