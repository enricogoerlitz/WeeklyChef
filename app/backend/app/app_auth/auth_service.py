from datetime import datetime, timezone, timedelta
from typing import Union

from app import settings
from core import models

import jwt


EXP_DURATION = {"days": 30}


def register_user() -> models.User:
    # das einfach über POST in ViewSet abwickeln? -> NEIN -> brauchen JWT!
    pass


def login_user() -> tuple[models.User, dict]:
    """
    Fetch the user from the db and generates an jwt access and refresh token
    Returns the user and the both tokes as dict as tuple
    """
    pass


def _create_access_refresh_token(data: dict) -> dict:
    """Generates and returns an access and refresh jwt token"""
    return {
        "token": _create_access_token(data),
        "refresh_token": _create_refresh_token(data)
    }


def _create_access_token(data: dict) -> str:
    """Generates and returns an access jwt token"""
    payload = data | {"is_refresh_token": False}
    return _create_token(payload, exp_duration=EXP_DURATION)


def _create_refresh_token(data: dict) -> str:
    """Generates and returns an refresh jwt token"""
    payload = data | {"is_refresh_token": True}
    return _create_token(payload, exp_duration=None)


def _create_token(
    data: dict,
    exp_duration: Union[dict, None] = EXP_DURATION
) -> str:
    """Create a jwt token"""
    creation_date = datetime.now(tz=timezone.utc)
    issuer = settings.JWT_ISSUER
    jwt_token_settings = {"iss": issuer, "creation_date": creation_date}
    if exp_duration:
        exp = creation_date + timedelta(**exp_duration)
        jwt_token_settings = {"exp": exp} | jwt_token_settings
    payload = data | jwt_token_settings

    return jwt.encode(payload, key=settings.JWT_SECRET_KEY, algorithm="HS256")


def _decode_token(token: str) -> dict:
    """
    Validate an given jwt token
    Raises jwt.ExpiredSignatureError
    Raises jwt.InvalidSignatureError
    Returns decoded token data
    """
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        issuer=settings.JWT_ISSUER,
        algorithms=["HS256"]
    )
