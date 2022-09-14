"""
Module for handling django HttpRequest helper methods
"""
from rest_framework.request import Request


class IRequest(Request):
    """Dummy request interface for typing intellisense"""

    def __init__(self):
        self.path: str
        self.META: dict
        self.method: str

        raise TypeError(
            "Don't create an instance of the object. \
            This is just an dummy object for a typing intellisense"
        )
