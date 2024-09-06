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
        """Checks if a path requires authentication.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
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
