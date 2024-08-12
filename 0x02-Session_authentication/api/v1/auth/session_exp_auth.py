#!/usr/bin/env python3
"""Adds expiration date to a session
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """Add expiration handling to SessionAuth
    """
    def __init__(self):
        """Initialize SessionExpAuth class
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session with an expiration time.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_data = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user ID associated with the session ID if not expired
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        if self.session_duration <= 0:
            return session_data.get('user_id')

        created_at = session_data.get('created_at')
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return session_data.get('user_id')
