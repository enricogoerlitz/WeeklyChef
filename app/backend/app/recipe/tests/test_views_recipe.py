from django.test import TestCase # noqa

from core import models  # noqa
from core.tests.test_model_recipe import (  # noqa
    create_unit,
    create_tag,
    create_ingredient,
    create_recipe,  # noqa
    create_recipe_favorite,
    create_recipe_image,
    create_recipe_ingredient,
    create_recipe_rating,
    create_recipe_tag,
    create_watchlist,
    create_recipe_watchlist
)


# Unit, Tag, Ingredient, Recipe
# RecipeFavorite, RecipeImage, RecipeIngredient
# RecipeRating, RecipeTag, Watchlist, RecipeWatchlist


ULR_UNIT = "/api/v1/unit/"


class PrivateUnitApiTests(TestCase):
    """Test unit CRUD api"""

    def test_retrieve(self):
        """Test get unit"""
        pass
