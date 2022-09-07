from django.test import TestCase

from core import models


def create_day_time(

) -> models.DayTime:
    pass


def create_recipe_cart(

) -> models.RecipeCart:
    pass


def create_recipe_cart_ingredient(

) -> models.RecipeCartIngredient:
    pass


class CartModelTests(TestCase):
    """Test cart model"""

    def setUp(self):
        self.user = models.User.objects.create_user(
            username="cart_teddy",
            email="teddy@email.com",
            password="pasiueefrrhfiuho83r"
        )
