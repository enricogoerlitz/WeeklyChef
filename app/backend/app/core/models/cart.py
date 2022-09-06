from django.db import models

from core.models import User, Ingredient
from core.models.food_shop import FoodShop


class DayTime(models.Model):
    id = models.BigAutoField(primary_key=True)
    day_time_name = models.CharField(
        unique=True,
        max_length=10,
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'day_time'

    def __str__(self) -> str:
        return f"{self.id} | {self.day_time_name}"


class RecipeCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        blank=False,
        null=False
    )
    date = models.DateField(blank=False, null=False)
    day_time = models.ForeignKey(
        DayTime,
        models.SET_NULL,
        blank=True,
        null=True
    )
    recipe_name = models.CharField(max_length=75)
    food_shop = models.ForeignKey(
        FoodShop,
        models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'recipe_cart'

    def __str__(self) -> str:
        return f"{self.id} | {self.user} | {self.recipe_name}"


class RecipeCartIngredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopping_cart_recipe = models.ForeignKey(
        RecipeCart,
        models.CASCADE,
        blank=False,
        null=False
    )
    ingredient = models.ForeignKey(
        Ingredient,
        models.CASCADE,
        blank=False,
        null=False
    )
    buy_unit_quantity = models.IntegerField(blank=False, null=False)
    is_buyed = models.BooleanField(default=False, blank=True)

    class Meta:
        db_table = 'recipe_cart_ingredient'
        unique_together = (('shopping_cart_recipe', 'ingredient'),)

    def __str__(self) -> str:
        return f"{self.id}"
