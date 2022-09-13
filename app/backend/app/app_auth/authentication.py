"""
Module for custom jwt authentication classes
"""
from rest_framework.authentication import BaseAuthentication

from app_auth import auth_service


class JWTAuthUser:
    """JWT Auth user in request object"""

    def __init__(self, id: int, is_staff: bool) -> None:
        self.id = id
        self.is_staff = is_staff
        self.is_authenticated = True if id else False
    
    def __str__(self) -> str:
        return f"{self.id} | {self.is_staff} | {self.is_authenticated}"
    

class JWTAuthentication(BaseAuthentication):
    """Class for set needed data to the request object"""

    def authenticate(self, request):
        BEARER_PREFIX = "bearer "
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
