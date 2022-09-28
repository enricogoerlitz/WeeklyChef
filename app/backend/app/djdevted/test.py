"""
Module for test API-Endpoints
"""
from typing import Callable, Union, TypeVar

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.serializers import ModelSerializer


def check_is_auth_required(
    client: APIClient,
    endpoint: str
) -> bool:
    res = client.get(endpoint)
    if res.status_code == status.HTTP_301_MOVED_PERMANENTLY:
        print("Status: 301 -> CHECK YOUR ROUTE (/)!")
    return res.status_code == status.HTTP_403_FORBIDDEN


def id_url(url: str, id: int) -> str:
    return f"{url}{id}/"


def detail_url(url: str) -> tuple[str, str]:
    url1 = f"{url}?detail=1"
    url2 = f"{url}?detail=1"
    return url1, url2


def get_payload_data(
    Serializer_class: Callable,
    payload: Union[list, dict],
    many=False
) -> dict:
    serializer: ModelSerializer = Serializer_class(many=many, data=payload)
    serializer.is_valid()
    return serializer.data


class HttpResponseObj:
    """Compare two HTTP Responses"""
    HttpResponseObjClass = TypeVar(
        "HttpResponseObjClass",
        bound="HttpResponseObj"
    )

    def __init__(self) -> None:
        pass

    def compare(obj: Union[HttpResponseObjClass, dict, Response]):
        """
        Compares the given object with this object
        Raises NotEqualException
        """
        pass
