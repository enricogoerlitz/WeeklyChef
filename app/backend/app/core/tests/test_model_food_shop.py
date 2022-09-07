from django.test import TestCase

from core import models


def create_food_shop(
    shop_name: str,
    address: str = "Street1",
    zip_code: str = "F28193",
    city: str = "Berlin",
    shop_comment: str = None
) -> models.FoodShop:
    return models.FoodShop.objects.create(
        shop_name=shop_name,
        address=address,
        zip_code=zip_code,
        city=city,
        shop_comment=shop_comment,
    )


def create_food_shop_area(
    area_name: str,
    food_shop: models.FoodShop,
    area_order_number: int = 1
) -> models.FoodShopArea:
    return models.FoodShopArea.objects.create(
        area_name=area_name,
        food_shop=food_shop,
        area_order_number=area_order_number
    )


def create_food_shop_area_part(

) -> models.FoodShopAreaPart:
    pass


def create_food_shop_area_part_ingredient(

) -> models.FoodShopAreaPartIngredient:
    pass


def create_preferred_user_food_shop(

) -> models.PreferredUserFoodShop:
    pass


class FoodShopModelTests(TestCase):
    """Test food_shop model"""

    def setUp(self):
        self.user = models.User.objects.create_user(
            username="food_shop_teddy",
            email="teddy@email.com",
            password="pasiueefrrhfiuho83r"
        )
