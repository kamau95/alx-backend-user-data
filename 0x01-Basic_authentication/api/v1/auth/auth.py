#!/usr/bin/env python3
"""
This module holds Auth class which is responsible for handling
api authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    this class manages api authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        this method checks if authentication is needed for a url
        """
        if path is None:
            return True

        if excluded_paths is None:
            return True

        # make sure path ends with a slash
        if not path.endswith('/'):
            path += '/'

        # Check if the path is in excluded paths
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        this method gets authorization header from the request
        """
        if request is None:
            return None

        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        this method retrives current user from the request
        """
        return None
