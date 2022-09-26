from django.test import TestCase

from core import models
from core.tests.test_model_food_shop import create_food_shop
from core.tests.test_model_user import setup_user


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
    date: str = "2022-03-01"
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


class DayTimeModelTests(TestCase):
    """Test day time model"""

    def test_create_day_time(self):
        """Test creating day time"""
        day_time_name = "Nachmittag"
        day_time = create_day_time(day_time_name)

        self.assertEqual(day_time.day_time_name, day_time_name)


class RecipeCartModelTests(TestCase):
    """Test recipe cart model"""

    def test_create_recipe_cart(self):
        """Test recipe cart"""
        user1 = setup_user("teddy1")
        user2 = setup_user("teddy2")
        day_time1 = create_day_time("vormittag")
        day_time2 = create_day_time("nachmittag")
        date1 = "2020-05-01"
        date2 = "2021-05-02"
        food_shop1 = create_food_shop("shop1")
        food_shop2 = create_food_shop("shop2")
        recipe_name1 = "recipe1"
        recipe_name2 = "recipe2"

        rc1 = create_recipe_cart(
            user1,
            food_shop1,
            day_time1,
            recipe_name1,
            date1
        )
        rc2 = create_recipe_cart(
            user1,
            food_shop2,
            day_time1,
            recipe_name2,
            date2
        )
        rc3 = create_recipe_cart(
            user1,
            food_shop1,
            day_time2,
            recipe_name1,
            date1
        )
        rc4 = create_recipe_cart(
            user1,
            food_shop1,
            day_time1,
            recipe_name2,
            date1
        )
        rc5 = create_recipe_cart(
            user2,
            food_shop1,
            day_time1,
            recipe_name1,
            date1
        )

        self.assertEqual(rc1.user.id, user1.id)
        self.assertEqual(rc1.food_shop.id, food_shop1.id)
        self.assertEqual(rc1.day_time.id, day_time1.id)
        self.assertEqual(rc1.recipe_name, recipe_name1)

        self.assertEqual(rc2.food_shop.id, food_shop2.id)
        self.assertEqual(rc3.day_time.id, day_time2.id)
        self.assertEqual(rc4.recipe_name, recipe_name2)
        self.assertEqual(rc5.user.id, user2.id)
