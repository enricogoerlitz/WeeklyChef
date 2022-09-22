"""
Test user model api endpoints
"""
from django.test import TestCase # noqa

from rest_framework.test import APIClient

from app_auth import auth_service
from core.models import User
from core.tests.test_model_user import create_user


def setup_login(
    client: APIClient,
    is_staff: bool = False,
    username="teddy_auth"
) -> User:
    user = create_user(username, is_staff=is_staff)
    tokens = auth_service._create_access_refresh_token(
        user.id,
        user.is_staff
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['token']}")
    return user

# /api/v1/user/me/                      # return me as object
# /api/v1/user/me/watchlists/           # list of user watchlists
# /api/v1/user/me/favorite-recipes/     # list of user recipe favorites
# /api/v1/user/me/favorite-foodshop/    # specific foodshop
# /api/v1/user/me/cart/                 # cart of the user [full joined]
# /api/v1/user/me/cart/count/
