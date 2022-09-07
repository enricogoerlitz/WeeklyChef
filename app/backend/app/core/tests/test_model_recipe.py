from django.test import TestCase

from core import models


def create_unit(
    unit_name: str
) -> models.Unit:
    return models.Unit.objects.create(unit_name=unit_name)


def create_tag(
    tag_name: str
) -> models.Tag:
    return models.Tag.objects.create(tag_name=tag_name)


def create_ingredient(
    ingredient_name: str,
    ingredient_display_name: str,
    unit: models.Unit,
    default_price: float = 2.49,
    quantity_per_unit: float = 200,
    is_spices: bool = False,
    search_description: str = None
) -> models.Ingredient:
    return models.Ingredient.objects.create(
        ingredient_name=ingredient_name,
        ingredient_display_name=ingredient_display_name,
        unit=unit,
        default_price=default_price,
        quantity_per_unit=quantity_per_unit,
        is_spices=is_spices,
        search_description=search_description
    )


def create_recipe(
    recipe_name: str,
    user: models.User,
    person_count: int = 2,
    prep_description: str = "prep_description",
    cooking_duration_min: int = 35,
) -> models.Recipe:
    return models.Recipe.objects.create(
        recipe_name=recipe_name,
        person_count=person_count,
        prep_description=prep_description,
        cooking_duration_min=cooking_duration_min,
        user=user
    )


def create_recipe_favorite(
    user: models.User,
    recipe: models.Recipe
) -> models.RecipeFavorite:
    return models.RecipeFavorite.objects.create(
        user=user,
        recipe=recipe
    )


def create_recipe_image(
    recipe: models.Recipe,
    image_path: str = "image_path"
) -> models.RecipeImage:
    return models.RecipeImage.objects.create(
        recipe=recipe,
        image_path=image_path
    )


def create_recipe_ingredient(
    recipe: models.Recipe,
    ingredient: models.Ingredient,
    unit_quantity: float = 200
) -> models.RecipeIngredient:
    return models.RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        unit_quantity=unit_quantity
    )


def create_recipe_rating(
    user: models.User,
    recipe: models.Recipe,
    rating: float = 4.5
) -> models.RecipeRating:
    return models.RecipeRating.objects.create(
        user=user,
        recipe=recipe,
        rating=rating
    )


def create_recipe_tag(
    recipe: models.Recipe,
    tag: models.Tag
) -> models.RecipeTag:
    return models.RecipeTag.objects.create(
        recipe=recipe,
        tag=tag
    )


def create_watchlist(
    user: models.User,
    watchlist_name: str = "MyWatchListName"
) -> models.Watchlist:
    return models.Watchlist.objects.create(
        watchlist_name=watchlist_name,
        user=user
    )


def create_recipe_watchlist(
    watchlist: models.Watchlist,
    recipe: models.Recipe
) -> models.RecipeWatchlist:
    return models.RecipeWatchlist.objects.create(
        watchlist=watchlist,
        recipe=recipe
    )


class RecipeModelTests(TestCase):
    """Test recipe models"""

    def setUp(self):
        self.user = models.User.objects.create_user(
            username="recipe_teddy",
            email="teddy@email.com",
            password="pasiuerhfiuho83r"
        )
