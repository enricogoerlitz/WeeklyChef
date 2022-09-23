from django.test import TestCase

from core import models
from core.tests.test_model_user import setup_user
from core.tests.test_model_recipe import (
    create_ingredient,
    create_unit,
)


address: str = "Street1"
zip_code: str = "F28193"
city: str = "Berlin"
shop_comment: str = ""


def create_food_shop(
    shop_name: str,
    address: str = address,
    zip_code: str = zip_code,
    city: str = city,
    shop_comment: str = shop_comment
) -> models.FoodShop:
    return models.FoodShop.objects.create(
        shop_name=shop_name,
        address=address,
        zip_code=zip_code,
        city=city,
        shop_comment=shop_comment,
    )


area_order_number: int = 1


def create_food_shop_area(
    food_shop: models.FoodShop,
    area_name: str,
    area_order_number: int = area_order_number
) -> models.FoodShopArea:
    return models.FoodShopArea.objects.create(
        area_name=area_name,
        food_shop=food_shop,
        area_order_number=area_order_number
    )


area_part_name: str = "Eingangsbereich"
area_part_order_number: int = 1


def create_food_shop_area_part(
    area: models.FoodShopArea,
    area_part_name: str = area_part_name,
    area_part_order_number: int = area_part_order_number
) -> models.FoodShopAreaPart:
    return models.FoodShopAreaPart.objects.create(
        area=area,
        area_part_name=area_part_name,
        area_part_order_number=area_part_order_number
    )


ingredient_price: float = 1.99


def create_food_shop_area_part_ingredient(
    area_part: models.FoodShopAreaPart,
    ingredient: models.Ingredient,
    ingredient_price: float = ingredient_price
) -> models.FoodShopAreaPartIngredient:
    return models.FoodShopAreaPartIngredient.objects.create(
        ingredient=ingredient,
        area_part=area_part,
        ingredient_price=ingredient_price
    )


def create_preferred_user_food_shop(
    user: models.User,
    food_shop: models.FoodShop
) -> models.PreferredUserFoodShop:
    return models.PreferredUserFoodShop.objects.create(
        user=user,
        food_shop=food_shop
    )


class FoodShopModelTests(TestCase):
    """Test food_shop model"""

    def setUp(self):
        self.user = setup_user()

    def test_create_food_shop(self):
        """Test creating food shop"""
        shop_name = "shop1"
        food_shop = create_food_shop(shop_name)

        self.assertEqual(food_shop.shop_name, shop_name)
        self.assertEqual(food_shop.address, address)
        self.assertEqual(food_shop.zip_code, zip_code)
        self.assertEqual(food_shop.city, city)
        self.assertEqual(food_shop.shop_comment, shop_comment)


class FoodShopAreaModelTests(TestCase):
    """Test food shop area model"""

    def test_creating_food_shop_area(self):
        """Test creating food shop area"""
        food_shop1 = create_food_shop("shop1")
        food_shop2 = create_food_shop("shop2")
        area_name1 = "area_name1"
        area_name2 = "area_name2"
        area_name3 = "area_name3"
        order1 = 1
        order2 = 2
        order3 = 3

        fsa1 = create_food_shop_area(food_shop1, area_name1, order1)
        fsa2 = create_food_shop_area(food_shop1, area_name2, order2)
        fsa3 = create_food_shop_area(food_shop1, area_name3, order3)
        fsa4 = create_food_shop_area(food_shop2, area_name1, order1)
        fsa5 = create_food_shop_area(food_shop2, area_name2, order2)
        fsa6 = create_food_shop_area(food_shop2, area_name3, order3)

        self.assertEqual(fsa1.food_shop.id, food_shop1.id)
        self.assertEqual(fsa1.area_name, area_name1)
        self.assertEqual(fsa1.area_order_number, order1)

        self.assertEqual(fsa2.food_shop.id, food_shop1.id)
        self.assertEqual(fsa2.area_name, area_name2)
        self.assertEqual(fsa2.area_order_number, order2)

        self.assertEqual(fsa3.food_shop.id, food_shop1.id)
        self.assertEqual(fsa3.area_name, area_name3)
        self.assertEqual(fsa3.area_order_number, order3)

        self.assertEqual(fsa4.food_shop.id, food_shop2.id)
        self.assertEqual(fsa4.area_name, area_name1)
        self.assertEqual(fsa4.area_order_number, order1)

        self.assertEqual(fsa5.food_shop.id, food_shop2.id)
        self.assertEqual(fsa5.area_name, area_name2)
        self.assertEqual(fsa5.area_order_number, order2)

        self.assertEqual(fsa6.food_shop.id, food_shop2.id)
        self.assertEqual(fsa6.area_name, area_name3)
        self.assertEqual(fsa6.area_order_number, order3)


class FoodShopAreaPartModelTests(TestCase):
    """Test food shop area part model"""

    def setUp(self):
        self.shop = create_food_shop("shop1")

    def test_create_food_shop_area_part(self):
        """Test creating a food shop area part"""
        area1 = create_food_shop_area(
            self.shop,
            "area1",
            1
        )
        area2 = create_food_shop_area(
            self.shop,
            "area2",
            2
        )
        a_part_name1 = "part1"
        a_part_name2 = "part2"
        a_part_name3 = "part3"
        order1 = 1
        order2 = 2
        order3 = 3

        fsap1 = create_food_shop_area_part(area1, a_part_name1, order1)
        fsap2 = create_food_shop_area_part(area1, a_part_name2, order2)
        fsap3 = create_food_shop_area_part(area1, a_part_name3, order3)
        fsap4 = create_food_shop_area_part(area2, a_part_name1, order1)
        fsap5 = create_food_shop_area_part(area2, a_part_name2, order2)
        fsap6 = create_food_shop_area_part(area2, a_part_name3, order3)

        self.assertEqual(fsap1.area.id, area1.id)
        self.assertEqual(fsap1.area_part_name, a_part_name1)
        self.assertEqual(fsap1.area_part_order_number, order1)

        self.assertEqual(fsap2.area.id, area1.id)
        self.assertEqual(fsap2.area_part_name, a_part_name2)
        self.assertEqual(fsap2.area_part_order_number, order2)

        self.assertEqual(fsap3.area.id, area1.id)
        self.assertEqual(fsap3.area_part_name, a_part_name3)
        self.assertEqual(fsap3.area_part_order_number, order3)

        self.assertEqual(fsap4.area.id, area2.id)
        self.assertEqual(fsap4.area_part_name, a_part_name1)
        self.assertEqual(fsap4.area_part_order_number, order1)

        self.assertEqual(fsap5.area.id, area2.id)
        self.assertEqual(fsap5.area_part_name, a_part_name2)
        self.assertEqual(fsap5.area_part_order_number, order2)

        self.assertEqual(fsap6.area.id, area2.id)
        self.assertEqual(fsap6.area_part_name, a_part_name3)
        self.assertEqual(fsap6.area_part_order_number, order3)


class FoodShopAreaPartIngredientModelTests(TestCase):
    """Test food shop area part ingredient model"""

    def setUp(self):
        self.unit = create_unit("kg")
        self.food_shop = create_food_shop("shop1")

    def test_create_food_shop_area_part_ingredient(self):
        """Test creating food shop area part ingredient"""
        ingredient1 = create_ingredient("ingedient1", "ingredient", self.unit)
        ingredient2 = create_ingredient("ingedient2", "ingredient", self.unit)
        ingredient3 = create_ingredient("ingedient3", "ingredient", self.unit)
        area_part1 = create_food_shop_area_part(
            create_food_shop_area(self.food_shop, "area1", 1),
            "area_part1",
            1
        )
        area_part2 = create_food_shop_area_part(
            create_food_shop_area(self.food_shop, "area2", 2),
            "area_part2",
            1
        )
        price1 = 2.49
        price2 = 1.39
        price3 = None

        area_part_ing1 = create_food_shop_area_part_ingredient(
            area_part1,
            ingredient1,
            price1
        )
        area_part_ing2 = create_food_shop_area_part_ingredient(
            area_part1,
            ingredient2,
            price2
        )
        area_part_ing3 = create_food_shop_area_part_ingredient(
            area_part1,
            ingredient3,
            price3
        )
        area_part_ing4 = create_food_shop_area_part_ingredient(
            area_part2,
            ingredient3,
            price3
        )

        self.assertEqual(area_part_ing1.area_part.id, area_part1.id)
        self.assertEqual(area_part_ing1.ingredient.id, ingredient1.id)
        self.assertEqual(area_part_ing1.ingredient_price, price1)

        self.assertEqual(area_part_ing2.area_part.id, area_part1.id)
        self.assertEqual(area_part_ing2.ingredient.id, ingredient2.id)
        self.assertEqual(area_part_ing2.ingredient_price, price2)

        self.assertEqual(area_part_ing3.area_part.id, area_part1.id)
        self.assertEqual(area_part_ing3.ingredient.id, ingredient3.id)
        self.assertEqual(area_part_ing3.ingredient_price, price3)

        self.assertEqual(area_part_ing4.area_part.id, area_part2.id)
        self.assertEqual(area_part_ing4.ingredient.id, ingredient3.id)
        self.assertEqual(area_part_ing4.ingredient_price, price3)


class PreferredUserFoodShopModelTests(TestCase):
    """Test preferred user food shop model"""

    def setUp(self):
        self.user = setup_user()
        self.food_shop = create_food_shop("shop1")

    def test_create_preferred_user_food_shop(self):
        """Test creating preferred user food shop"""
        pref_u_shop = create_preferred_user_food_shop(
            self.user,
            self.food_shop
        )

        self.assertEqual(pref_u_shop.user.id, self.user.id)
        self.assertEqual(pref_u_shop.food_shop.id, self.food_shop.id)
