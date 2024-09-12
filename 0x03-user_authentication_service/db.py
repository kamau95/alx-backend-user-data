#!/usr/bin/env python3
"""DB module all management of db
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add a new user to database and return user object
        """
        # create a user object
        user = User(email=email, hashed_password=hashed_password)
        # add user to the session and commit
        session = self._session
        session.add(user)
        session.commit()

        # Return the user object
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        find user who becomes the first to match the criteria
        given by kwargs
        """
        # query for a user table
        query = self._session.query(User)
        # Apply filters based on keyword arguments
        for key, value in kwargs.items():
            if hasattr(User, key):
                column = getattr(User, key)
                query = query.filter(column == value)
            else:
                raise InvalidRequestError
        user = query.first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        returns None,
        - updates the user’s attributes as passed in the method’s
        arguments then commit changes to the database.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueEror
            setattr(user, key, value)
            self._session.commit()
