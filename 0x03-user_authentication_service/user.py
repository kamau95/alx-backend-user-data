#!/usr/bin/env python3
"""
Declare a SQLAlchemy model named 'User' corresponding to a
database table named "users"
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Initialize the declarative base class for SQLAlchemy models
Base = declarative_base()

class User(Base):
    """
    User model representing a user entity in the database.
    
    Attributes:
        id (int): The primary key, unique identifier for each user.
        email (str): The user's email address, must be unique and not null.
        hashed_password (str): The user's password, stored as a hashed value.
        session_id (str, optional): The current session ID of the user for session management.
        reset_token (str, optional): Token used for password reset purposes.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(255), nullable=True)
