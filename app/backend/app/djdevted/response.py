"""
Module for handling django HttpResponse helper methods
"""

from typing import Union

from rest_framework import status
from rest_framework.response import Response


def success(obj: dict) -> Response:
    """Returns an HTTP-200-OK Response with passed data."""
    return Response(obj, status=status.HTTP_200_OK)

def created(created_obj: dict) -> Response:
    """Returns an HTTP-201-CREATED Response with passed data."""
    return Response(created_obj, status=status.HTTP_201_CREATED)

def updated(updated_obj: dict) -> Response:
    """Returns an HTTP-202-ACCEPTED Response with passed data."""
    return Response(updated_obj, status=status.HTTP_202_ACCEPTED)

def error_400_bad_request(exp: Union[Exception, str, dict]) -> Response:
    """Returns an HTTP-400-BAD-REQUEST Response with passed data."""
    if isinstance(exp, dict):
        Response(exp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": str(exp)}, status=status.HTTP_400_BAD_REQUEST)

def error_401_unauthorized(exp: Union[Exception, str, dict]) -> Response:
    """Returns an HTTP-401-UNAUTHORIZED Response with passed data."""
    if isinstance(exp, dict):
        Response(exp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": str(exp)}, status=status.HTTP_401_UNAUTHORIZED)

def error_403_forbidden(exp: Union[Exception, str, dict]) -> Response:
    """Returns an HTTP-403-FORBIDDEN Response with passed data."""
    if isinstance(exp, dict):
        Response(exp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": str(exp)}, status=status.HTTP_403_FORBIDDEN)

def error_500_internal_server_error(exp: Union[Exception, str, dict]) -> Response:
    """Returns an HTTP-500-SERVER-ERROR Response with passed data."""
    if isinstance(exp, dict):
        Response(exp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error": str(exp)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)