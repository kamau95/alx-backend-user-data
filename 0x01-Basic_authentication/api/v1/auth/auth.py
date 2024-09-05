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
        Determines whether a given path requires authentication or not
        Args:
            - path(str): Url path to be checked
            - excluded_paths(List of str): List of paths that do not require
              authentication
        Return:
            - True if path is not in excluded_paths, else False
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
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
