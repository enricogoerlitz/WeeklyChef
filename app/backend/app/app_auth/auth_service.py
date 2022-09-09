from datetime import datetime, timezone, timedelta

from app import settings
from core import models

import jwt


def register_user() -> models.User:
    # das einfach über POST in ViewSet abwickeln? -> NEIN -> brauchen JWT!
    pass


def login_user() -> tuple[models.User, dict]:
    """
    Fetch the user from the db and generates an jwt access and refresh token
    Returns the user and the both tokes as dict as tuple
    """
    pass


def _get_access_refresh_token(data: dict) -> dict:
    """Generates and returns an access and refresh jwt token"""
    return {
        "token": _create_access_token(data),
        "refresh_token": _create_refresh_token(data)
    }


def _create_access_token(data: dict) -> str:
    """Generates and returns an access jwt token"""
    return _create_token(data, True)


def _create_refresh_token(data: dict) -> str:
    """Generates and returns an refresh jwt token"""
    return _create_token(data | {"is_refresh_token": True}, False)


def _create_token(data: dict, do_exp: bool = True) -> str:
    exp = datetime.now(tz=timezone.utc) + timedelta(days=30)
    issuer = settings.JWT_ISSUER
    jwt_token_settings = {"exp": exp, "iss": issuer} if do_exp else {"iss": issuer}
    payload = data | jwt_token_settings

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def _decode_token(token: str) -> dict:
    """
    Validate an given jwt token
    Raises jwt.ExpiredSignatureError
    Raises jwt.InvalidSignatureError
    """
    token_data = jwt.decode(token, settings.JWT_SECRET_KEY, issuer=settings.JWT_ISSUER, algorithms=["HS256"])
    return token_data
