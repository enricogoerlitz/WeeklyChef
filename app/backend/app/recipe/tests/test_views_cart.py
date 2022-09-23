"""
Test cart models api endpoints
"""
from django.test import TestCase

from rest_framework.test import APIClient

from djdevted.test import (  # noqa
    check_is_auth_required,
    get_payload_data,
    id_url,
)

# DayTime, RecipeCart, RecipeCartIngredient

URL_DAY_TIME = "/api/v1/day-time/"
URL_RECIPE_CART = "/api/v1/recipe-cart/"
URL_RECIPE_CART_ING = "/api/v1/recipe-cart-ingredient/"


class PublicCartAuthRequired(TestCase):
    """Test endpoints require an authorization token"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_day_time(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_DAY_TIME
            )
        )

    def test_auth_required_recipe_cart(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_RECIPE_CART
            )
        )

    def test_auth_required_recipe_cart_ingredient(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_RECIPE_CART_ING
            )
        )
