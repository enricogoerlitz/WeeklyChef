from datetime import datetime, timezone, timedelta
from typing import Union

from django.core.exceptions import ObjectDoesNotExist

from djdevted.request import IRequest

from app import settings
from recipe.serializers import UserPostSerializer
from core.models import User

import jwt  # type: ignore


EXP_DURATION = {"days": 30}


def register_user(request: IRequest) -> dict:
    """
    Handle register user
    Raises Value error if serializing failed
    """
    serializer = UserPostSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValueError(serializer.errors)

    created_user: User = User.objects.create_user(
        **serializer.data,
        password=request.data.get("password")
    )

    return _create_access_refresh_token(created_user.id, created_user.is_staff)


def login_user(request: IRequest) -> dict:
    """
    Handle user login
    Raises ValueError
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not username:
        raise ValueError("The username field is required.")

    if not password:
        raise ValueError("The password field is required.")

    user: User = User.objects.get(username=username)
    if not user.check_password(password):
        raise ObjectDoesNotExist()

    return _create_access_refresh_token(user.id, user.is_staff)


def refresh_token(request: IRequest) -> dict:
    """Handle refreshing token"""
    refresh_token = request.data.get("refresh_token")
    if not refresh_token:
        raise ValueError("No refresh token in request body.")

    decoded_token = decode_token(refresh_token)

    if not decoded_token.get("is_refresh_token"):
        raise ValueError("The passed token is no refresh token.")

    user_id = decoded_token.get("user_id")
    user: User = User.objects.get(id=user_id)

    return _create_access_refresh_token(user.id, user.is_staff)


def _create_access_refresh_token(user_id: int, is_staff: bool) -> dict:
    """Generates and returns an access and refresh jwt token"""
    refresh_token_data = {"user_id": user_id}
    access_token_data = refresh_token_data | {"is_staff": is_staff}
    return {
        "token": _create_access_token(access_token_data),
        "refresh_token": _create_refresh_token(refresh_token_data)
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
    jwt_token_settings: dict = {
        "iss": issuer,
        "creation_date": str(creation_date)
    }
    if exp_duration:
        exp = creation_date + timedelta(**exp_duration)
        jwt_token_settings = {"exp": exp} | jwt_token_settings
    payload = data | jwt_token_settings

    return jwt.encode(payload, key=settings.JWT_SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> dict:
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
