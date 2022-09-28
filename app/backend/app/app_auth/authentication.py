"""
Module for custom jwt authentication classes
"""
from typing import Union

from rest_framework.authentication import BaseAuthentication

from djdevted.request import IRequest

from app_auth import auth_service


class JWTAuthUser:
    """JWT Auth user in request object"""

    def __init__(
        self, id: Union[None, int],
        is_staff: Union[None, bool]
    ) -> None:
        self.id = id
        self.is_staff = is_staff
        self.is_authenticated = True if id else False

    def __str__(self) -> str:
        return f"{self.id} | {self.is_staff} | {self.is_authenticated}"


class JWTAuthentication(BaseAuthentication):
    """Class for set needed data to the request object"""

    def authenticate(self, request: IRequest):
        BEARER_PREFIX = "Bearer "
        try:
            token: str = request.META["HTTP_AUTHORIZATION"]
            token = token.replace(BEARER_PREFIX, "")
            decoded_token = auth_service.decode_token(token)
            user = JWTAuthUser(
                decoded_token["user_id"],
                decoded_token["is_staff"]
            )
            return (user, None)
        except Exception:
            user = JWTAuthUser(None, None)
            return (user, None)
