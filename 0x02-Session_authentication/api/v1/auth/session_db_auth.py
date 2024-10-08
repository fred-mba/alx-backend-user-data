#!/usr/bin/env python3
"""Sessions in database
"""
from flask import request
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth stores session info in the db
    """
    def create_session(self, user_id=None):
        """Create and store session in the db.
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id
            }
            user_session = UserSession(**kwargs)
            user_session.save()

            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user_id based on the session ID stored in the db.
        """
        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(user_session) <= 0:
            return None

        current_time = datetime.now()
        time_stamp = timedelta(seconds=self.session_duration)
        exp_time = user_session[0].created_at + time_stamp
        if exp_time < current_time:
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroy user_session from the db based on the session ID.
        """
        session_id = self.session_cookie(request)
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if len(user_session) <= 0:
            return False
        user_session[0].remove()
        return True
