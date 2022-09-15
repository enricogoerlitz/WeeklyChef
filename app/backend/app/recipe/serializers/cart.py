"""
Cart model serializers
"""
from rest_framework.serializers import ModelSerializer

from core import models
from recipe import serializers


class DayTimeSerializer(ModelSerializer):
    """Serialize day time serializer"""

    class Meta:
        model = models.DayTime
        fields = ["id", "day_time_name"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "day_time_name": {"min_length": 4}
        }


class RecipeCartSerializer(ModelSerializer):
    """Serialize recipe cart model"""

    class Meta:
        models = models.RecipeCart
        fields = [
            "id", "user", "date",
            "day_time", "recipe_name", "food_shop"
        ]
        read_only_fields = ["id"]


class RecipeCartSerializer(RecipeCartSerializer):
    """Serialize recipe cart model"""
    user = serializers.UserGetSerializer(many=False)
    day_time = DayTimeSerializer
    food_shop = serializers.FoodShopSerializer(many=False)


class RecipeCartIngredientSerializer(ModelSerializer):
    """Serialize recipe cart ingredient model"""

    class Meta:
        model = models.RecipeCartIngredient
        fields = [
            "id", "shopping_cart_recipe",
            "ingredient", "buy_unit_quantity", "is_done"
        ]
        read_only_fields = ["id"]
