from django.db import models

from core.models import Ingredient, User


class FoodShop(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop_name = models.CharField(unique=True, max_length=100)
    address = models.CharField(max_length=75)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    shop_comment = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'food_shop'

    def __str__(self) -> str:
        return f"{self.id} | {self.shop_name} | {self.address}"


class FoodShopArea(models.Model):
    id = models.BigAutoField(primary_key=True)
    food_shop = models.ForeignKey(
        FoodShop,
        models.CASCADE
    )
    area_name = models.CharField(max_length=100)
    area_order_number = models.IntegerField()

    class Meta:
        db_table = 'food_shop_area'
        unique_together = (
            ('food_shop', 'area_order_number'),
            ('food_shop', 'area_name'),
        )

    def __str__(self) -> str:
        return f"{self.id} | {self.area_name} | {self.area_order_number}"


class FoodShopAreaPart(models.Model):
    id = models.BigAutoField(primary_key=True)
    area = models.ForeignKey(FoodShopArea, models.CASCADE)
    area_part_name = models.CharField(max_length=100)
    area_part_order_number = models.IntegerField()

    class Meta:
        db_table = 'food_shop_area_part'
        unique_together = (
            ('area', 'area_part_order_number'),
            ('area', 'area_part_name'),
        )

    def __str__(self) -> str:
        return f"{self.id} | {self.area_part_name} | \
                 {self.area_part_order_number}"


class FoodShopAreaPartIngredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    ingredient = models.ForeignKey(Ingredient, models.CASCADE)
    area_part = models.ForeignKey(FoodShopAreaPart, models.CASCADE)
    ingredient_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'food_shop_area_part_ingredient'
        unique_together = (('ingredient', 'area_part'),)

    def __str__(self) -> str:
        return f"{self.id}"


class PreferredUserFoodShop(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, models.CASCADE)
    food_shop = models.ForeignKey(
        FoodShop,
        models.SET_NULL,
        blank=False,
        null=True
    )

    class Meta:
        db_table = 'preferred_user_food_shop'
        unique_together = (('user', 'food_shop'),)

    def __str__(self) -> str:
        return f"{self.id}"
