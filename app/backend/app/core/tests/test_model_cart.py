from django.test import TestCase

from core import models


def create_day_time(
    day_time_name: str = "vormittag"
) -> models.DayTime:
    return models.DayTime.objects.create(
        day_time_name=day_time_name
    )


def create_recipe_cart(
    user: models.User,
    food_shop: models.FoodShop,
    day_time: models.DayTime,
    recipe_name: str = "Spagetti Carbonara",
    date: str = "08.09.2022"
) -> models.RecipeCart:
    return models.RecipeCart.objects.create(
        user=user,
        date=date,
        day_time=day_time,
        recipe_name=recipe_name,
        food_shop=food_shop
    )


def create_recipe_cart_ingredient(
    shopping_cart_recipe: models.RecipeCart,
    ingredient: models.Ingredient,
    buy_unit_quantity: int = 2,
    is_done: bool = False
) -> models.RecipeCartIngredient:
    return models.RecipeCartIngredient.objects.create(
        shopping_cart_recipe=shopping_cart_recipe,
        ingredient=ingredient,
        buy_unit_quantity=buy_unit_quantity,
        is_done=is_done
    )


class CartModelTests(TestCase):
    """Test cart model"""

    def setUp(self):
        self.user = models.User.objects.create_user(
            username="cart_teddy",
            email="teddy@email.com",
            password="pasiueefrrhfiuho83r"
        )
