"""
Module for handling django HttpRequest helper methods
"""
from rest_framework.request import Request


class IRequest(Request):
    """Dummy request interface for typing intellisense"""
    path: str
    META: dict
    method: str

    def __init__(self) -> None:
        raise TypeError(
            "Don't create an instance of the object. \
            This is just an dummy object for a typing intellisense"
        )
