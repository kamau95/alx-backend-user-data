#!/usr/bin/env python3
"""
this module will contain the class
BasicAuth
"""
from .auth import Auth
import base64


class BasicAuth(Auth):
    """
    BasicAuth class inherits from the Auth class
    Implements Basic Authorization protocol methods
    """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        this method validates and decodes base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            res = base64.b64decode(base64_authorization_header)
            return res.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        this method extracts user credentials password and username
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        parts = decoded_base64_authorization_header.split(':', 1)
        if len(parts) != 2:
            return None, None
        email, password = parts
        return email, password
