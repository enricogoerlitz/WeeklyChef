"""
FoodShop model serializers
"""
from rest_framework.serializers import ModelSerializer

from core import models
from recipe.serializers.recipe import IngredientSerializer


class FoodShopSerializer(ModelSerializer):
    """Serialize food shop model"""

    class Meta:
        model = models.FoodShop
        fields = [
            "id", "shop_name", "address",
            "zip_code", "city", "shop_comment"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "shop_name": {"min_length": 5},
            "address": {"min_length": 5},
            "zip_code": {"min_length": 3},
            "city": {"min_length": 2},
        }


class FoodShopAreaSerializer(ModelSerializer):
    """Serialize food shop area model"""

    class Meta:
        model = models.FoodShopArea
        fields = [
            "id", "food_shop",
            "area_name", "area_order_number"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "area_name": {"min_length": 3},
            "area_order_number": {"min_value": 1},
        }


class FoodShopAreaDetailSerializer(
    FoodShopAreaSerializer
):
    """Serialize food shop area model with details"""
    food_shop = FoodShopSerializer(many=False)


class FoodShopAreaPartSerializer(ModelSerializer):
    """Serialize food shop area part model"""

    class Meta:
        model = models.FoodShopAreaPart
        fields = [
            "id", "area", "area_part_name"
            "area_part_order_number"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "area_part_name": {"min_length": 3},
            "area_part_order_number": {"min_value": 1},
        }


class FoodShopAreaPartDetailSerializer(
    FoodShopAreaPartSerializer
):
    """
    Serialize food shop area part model
    with details
    """
    area = FoodShopAreaDetailSerializer(many=False)


class FoodShopAreaPartIngredientSerializer(ModelSerializer):
    """Serialize food shop area part ingredient model"""

    class Meta:
        model = models.FoodShopAreaPartIngredient
        fields = [
            "id", "ingredient", "area_part",
            "ingredient_price"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "ingredient_price": {"min_value": 0},
        }


class FoodShopAreaPartIngredientDetailSerializer(
    FoodShopAreaPartIngredientSerializer
):
    """
    Serialize food shop area part ingredient model
    with details
    """
    ingredient = IngredientSerializer(many=False)
    area_part = FoodShopAreaPartDetailSerializer(many=False)


class PreferredUserFoodShopSerializer(ModelSerializer):
    """Serialize favorite user food shop model"""

    class Meta:
        model = models.PreferredUserFoodShop
        fields = ["id", "user", "food_shop"]
        read_only_fields = ["id"]


class PreferredUserFoodShopDetailSerializer(PreferredUserFoodShopSerializer):
    """
    Serialize favorite user food shop model
    with details
    """
