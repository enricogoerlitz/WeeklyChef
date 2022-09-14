from django.db import models

from core.models import User, Ingredient, FoodShop


class DayTime(models.Model):
    id = models.BigAutoField(primary_key=True)
    day_time_name = models.CharField(
        unique=True,
        max_length=10
    )

    class Meta:
        db_table = 'day_time'

    def __str__(self) -> str:
        return f"{self.id} | {self.day_time_name}"


class RecipeCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        models.CASCADE
    )
    date = models.DateField()
    day_time = models.ForeignKey(
        DayTime,
        models.SET_NULL,
        blank=False,
        null=True
    )
    recipe_name = models.CharField(max_length=75)
    food_shop = models.ForeignKey(
        FoodShop,
        models.SET_NULL,
        blank=False,
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
        models.CASCADE
    )
    ingredient = models.ForeignKey(Ingredient, models.CASCADE)
    buy_unit_quantity = models.IntegerField()
    is_done = models.BooleanField(default=False, blank=True)

    class Meta:
        db_table = 'recipe_cart_ingredient'
        unique_together = (('shopping_cart_recipe', 'ingredient'),)

    def __str__(self) -> str:
        return f"{self.id}"
