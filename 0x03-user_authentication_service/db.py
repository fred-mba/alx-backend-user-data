#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

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
           Used to add new user and commit the transaction.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves the user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Takes in arbitrary keyword arguments and returns the first row
           found in the users table.

           Raises:
              NoResultFound: If no user is found with the provided ID.
              InvalidRequestError: If an invalid field is provided.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user

        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """Takes as argument a required user_id integer and arbitrary
           keyword arguments, and returns None
        """
        user = self._session.query(User).filter_by(id=user_id).one()

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
