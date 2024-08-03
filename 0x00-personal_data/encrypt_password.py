#!/usr/bin/env python3
"""
An imeplementation of encrypting password using bcypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt
    Returns
    -------
    bytes: the salted, hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
