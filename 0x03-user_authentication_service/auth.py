#!/usr/bin/env python3
"""
thi si the auth module
"""
from typing import Union, TypeVar
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """
    generates a uuid id and returns its str representation
    """
    id = str(uuid.uuid4())
    return id


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
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        validates a user login
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if user and bcrypt.checkpw(
            password.encode('utf-8'), user.hashed_password
        ):
            return True
        return False

    def create_session(self, email: str) -> str:
        """
        Create a session_id for an existing user and update the user's
        session_id attribute
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        retrievs a user by using session_id
        """
        if session_id is None:
            return None
        user = self._db.find_user_by(session_id=session_id)
        if user is not None:
            return user
        return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user's session by setting session_id to None.
        """
        user = self._db.find_user_by(user_id=user_id)
        if user is None:
            return
        user.session_id = None
        # save change to database
        self._db.commit()
