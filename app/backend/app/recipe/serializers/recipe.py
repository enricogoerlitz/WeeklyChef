"""
Recipe model serializers
"""
from rest_framework.serializers import ModelSerializer

from core import models
from recipe.serializers import UserGetSerializer


class UnitSerializer(ModelSerializer):
    """Serialize unit model"""

    class Meta:
        model = models.Unit
        fields = ["id", "unit_name"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "unit_name": {"min_length": 1}
        }


class TagSerializer(ModelSerializer):
    """Serialize tag model"""

    class Meta:
        model = models.Tag
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            "tag_name": {"min_length": 2}
        }


class IngredientSerializer(ModelSerializer):
    """Serialize ingredient model"""
    unit = UnitSerializer(many=False, required=False)

    class Meta:
        model = models.Ingredient
        fields = [
            "id", "ingredient_name", "default_price",
            "ingredient_display_name", "quantity_per_unit",
            "unit", "is_spices", "search_description"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "ingredient_name": {"min_length": 3},
            "default_price": {"min_value": 0},
            "ingredient_display_name": {"min_length": 3},
            "quantity_per_unit": {"min_value": 0},
        }


class RecipeSerializer(ModelSerializer):
    """Serialize recipe model"""

    class Meta:
        model = models.Recipe
        fields = [
            "id", "recipe_name", "user", "person_count",
            "prep_description", "cooking_duration_min"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "recipe_name": {"min_length": 5},
            "person_count": {"min_value": 1},
            "prep_description": {"min_length": 10},
            "cooking_duration_min": {"min_value": 1},
        }


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize recipe model with details"""
    user = UserGetSerializer(many=False, required=False)


class RecipeFavoriteSerializer(ModelSerializer):
    """Serialize recipe favorite model"""

    class Meta:
        model = models.RecipeFavorite
        fields = ["id", "user", "recipe"]
        read_only_fields = ["id"]


class RecipeFavoriteDetailSerializer(RecipeFavoriteSerializer):
    """Serialize recipe favorite model with details"""
    user = UserGetSerializer(many=False, required=False)
    recipe = RecipeDetailSerializer(many=False, required=False)


class RecipeIngredientSerializer(ModelSerializer):
    """Serialize recipe ingredient model"""

    class Meta:
        model = models.RecipeIngredient
        fields = ["id", "recipe", "ingredient", "unit_quantity"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "unit_quantity": {"min_value": 0}
        }


class RecipeIngredientDetailSerializer(RecipeIngredientSerializer):
    """Serialize recipe ingredient model with details"""
    recipe = RecipeDetailSerializer(many=False)
    ingredient = IngredientSerializer(many=False)


class RecipeRatingSerializer(ModelSerializer):
    """Serialize recipe rating model"""

    class Meta:
        model = models.RecipeRating
        fields = ["id", "user", "recipe", "rating"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "rating": {"min_value": 0.5}
        }


class RecipeRatingDetailsSerializer(RecipeRatingSerializer):
    """Serialize recipe rating model with details"""
    user = UserGetSerializer(many=False, required=False)
    recipe = RecipeDetailSerializer(many=False)


class RecipeTagSerializer(ModelSerializer):
    """Serialize recipe tag model"""

    class Meta:
        model = models.RecipeTag
        fields = ["id", "recipe", "tag"]
        read_only_fields = ["id"]


class RecipeTagDetailsSerializer(ModelSerializer):
    """Serialize recipe tag model with details"""
    tag = TagSerializer(many=False)


class WatchlistSerializer(ModelSerializer):
    """Serialize watchlist model with details"""

    class Meta:
        model = models.Watchlist
        fields = ["id", "watchlist_name", "user"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "watchlist_name": {"min_length": 4}
        }


class RecipeWatchlistSerializer(ModelSerializer):
    """Serialize watchlist model with details"""

    class Meta:
        model = models.RecipeWatchlist
        fields = ["id", "watchlist", "recipe"]


class RecipeDataSerializer:
    """TEST: recipe with ingredients"""

    def __init__(self, recipe_serializer: RecipeSerializer) -> None:
        pass

    @property
    def data(self):
        """TEST: serialize recipe with ingredients"""
        pass
