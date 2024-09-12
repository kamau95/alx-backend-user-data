#!/usr/bin/env python3
"""
thi si the auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """
    hash password using bcrypt and return bytes
    """
    salt = bcrypt.gensalt()
    pass_bytes = password.encode('utf-8')
    hashed_pass = bcrypt.hashpw(pass_bytes, salt)
    return hashed_pass


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        checks whether an email exists in which it prints and error
        if email doesnt exist hash the password and then add the user
        """
        try:
            existing_usr = self._db.find_user_by(email=email)
            if existing_usr:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            new_pass = _hash_password(password)
            user = self._db.add_user(email, new_pass)
            return user
