"""
Module for test API-Endpoints
"""
from typing import Callable, Union

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.serializers import ModelSerializer


def check_is_auth_required(client: APIClient, endpoint: str):
    res = client.get(endpoint)
    if res.status_code == status.HTTP_301_MOVED_PERMANENTLY:
        print("Status: 301 -> CHECK YOUR ROUTE (/)!")
    return res.status_code == status.HTTP_403_FORBIDDEN


def id_url(url: str, id: int):
    return f"{url}{id}/"


def get_payload_data(
    Serializer_class: Callable,
    payload: Union[list, dict],
    many=False
) -> dict:
    serializer: ModelSerializer = Serializer_class(many=many, data=payload)
    serializer.is_valid()
    return serializer.data
