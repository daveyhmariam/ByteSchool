#!/usr/bin/env python3
"""
Auth class definition
"""

from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """
    Authentication class
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

        Args:
            request (_type_, optional): Defaults to None.

        Returns:
            str:
        """
        if request is None or "Authorization" not in request.headers.keys():
            return None
        else:
            return (request.headers["Authorization"])

    def current_user(self, request=None) -> TypeVar('User'):
        """

        Returns:
            User:
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Gets the value of the cookie named SESSION_NAME.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
