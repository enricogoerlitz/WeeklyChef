from django.test import TestCase

from core import models
from core.tests.test_model_user import setup_user


def create_unit(
    unit_name: str
) -> models.Unit:
    return models.Unit.objects.create(unit_name=unit_name)


def create_tag(
    tag_name: str
) -> models.Tag:
    return models.Tag.objects.create(tag_name=tag_name)


default_price: float = 2.49
quantity_per_unit: float = 200
is_spices: bool = False
search_description = ""


def create_ingredient(
    ingredient_name: str,
    ingredient_display_name: str,
    unit: models.Unit,
    default_price: float = default_price,
    quantity_per_unit: float = quantity_per_unit,
    is_spices: bool = is_spices,
    search_description: str = search_description
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


person_count: int = 2
prep_description: str = "prep_description"
cooking_duration_min: int = 35


def create_recipe(
    recipe_name: str,
    user: models.User,
    person_count: int = person_count,
    prep_description: str = prep_description,
    cooking_duration_min: int = cooking_duration_min,
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


unit_quantity: float = 200


def create_recipe_ingredient(
    recipe: models.Recipe,
    ingredient: models.Ingredient,
    unit_quantity: float = unit_quantity
) -> models.RecipeIngredient:
    return models.RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        unit_quantity=unit_quantity
    )


rating: float = 4.5


def create_recipe_rating(
    user: models.User,
    recipe: models.Recipe,
    rating: float = rating
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


watchlist_name: str = "MyWatchListName"


def create_watchlist(
    user: models.User,
    watchlist_name: str = watchlist_name
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


def setup_recipe(user: models.User):
    return create_recipe(
        recipe_name="BaseRecipeTest",
        user=user
    )


class UnitModelTests(TestCase):
    """Test Unit Model"""

    def test_create_unit(self):
        """Test creating unit"""
        unit_name = "ml"
        unit_name2 = "l"

        unit = create_unit(unit_name)
        unit2 = create_unit(unit_name2)

        self.assertEqual(unit.unit_name, unit_name)
        self.assertEqual(unit2.unit_name, unit_name2)


class TagModelTests(TestCase):
    """Test Tag Model"""

    def test_create_tag(self):
        """Test creating tag"""
        tag_name = "veggi"
        tag_name2 = "fleisch"

        tag = create_tag(tag_name)
        tag2 = create_tag(tag_name2)

        self.assertEqual(tag.tag_name, tag_name)
        self.assertEqual(tag2.tag_name, tag_name2)


class IngredientModelTests(TestCase):
    """Test Unit Model"""

    def setUp(self):
        self.params = {
            "ingredient_name": "Barilla Spagetti No3 500g",
            "ingredient_display_name": "Spagetti No3",
            "unit": create_unit("ml"),
        }

    def test_create_ingredient(self):
        """Test create ingredient"""

        ingredient = create_ingredient(**self.params)

        self.assertEqual(
            ingredient.ingredient_name,
            self.params["ingredient_name"]
        )
        self.assertEqual(
            ingredient.ingredient_display_name,
            self.params["ingredient_display_name"]
        )
        self.assertEqual(
            ingredient.unit.unit_name,
            self.params["unit"].unit_name
        )
        self.assertEqual(
            ingredient.default_price,
            default_price
        )
        self.assertEqual(
            ingredient.quantity_per_unit,
            quantity_per_unit
        )
        self.assertEqual(
            ingredient.is_spices,
            is_spices
        )
        self.assertEqual(
            ingredient.search_description,
            search_description
        )


class RecipeModelTests(TestCase):
    """Test recipe model"""

    def setUp(self):
        self.user = setup_user()

        self.params = {
            "recipe_name": "BaseRecipe",
            "user": self.user
        }

    def test_recipe_create(self):
        """Test creating recipe"""
        recipe = create_recipe(**self.params)

        self.assertEqual(recipe.recipe_name, self.params["recipe_name"])
        self.assertEqual(recipe.user.id, self.params["user"].id)
        self.assertEqual(recipe.person_count, person_count)
        self.assertEqual(recipe.prep_description, prep_description)
        self.assertEqual(recipe.cooking_duration_min, cooking_duration_min)


class RecipeFavoriteModelTests(TestCase):
    """Test recipe favorites model"""

    def test_create_recipe_favorite(self):
        creator_user = setup_user()
        user1 = setup_user("teddy1")
        user2 = setup_user("teddy2")
        recipe1 = create_recipe("recipe1", creator_user)
        recipe2 = create_recipe("recipe2", creator_user)

        recipe_fav1 = create_recipe_favorite(user1, recipe1)
        recipe_fav2 = create_recipe_favorite(user1, recipe2)
        recipe_fav3 = create_recipe_favorite(user2, recipe1)

        self.assertEqual(recipe_fav1.user.id, user1.id)
        self.assertEqual(recipe_fav1.recipe.id, recipe1.id)

        self.assertEqual(recipe_fav2.user.id, user1.id)
        self.assertEqual(recipe_fav2.recipe.id, recipe2.id)

        self.assertEqual(recipe_fav3.user.id, user2.id)
        self.assertEqual(recipe_fav3.recipe.id, recipe1.id)


class RecipeImageModelTests(TestCase):
    """Test recipe image model"""

    def setUp(self):
        self.recipe = setup_recipe(setup_user())

    def test_create_recipe_image(self):
        """Test creating an recipe image"""
        img_path = "/usr/img/path"
        recipe_img = create_recipe_image(self.recipe, img_path)

        self.assertEqual(recipe_img.recipe.id, self.recipe.id)
        self.assertEqual(recipe_img.image_path, img_path)


class RecipeIngredientModelTests(TestCase):
    """Test recipe ingredient model"""

    def setUp(self):
        self.user = setup_user()
        self.unit = create_unit("ml")

    def test_create_recipe_ingredient(self):
        """Test creating an recipe ingredient"""
        recipe1 = create_recipe("baseRecipe", self.user)
        recipe2 = create_recipe("baseRecipe2", self.user)
        ingredient1 = create_ingredient(
            "ingredient1",
            "ingredient1",
            self.unit
        )
        ingredient2 = create_ingredient(
            "ingredient2",
            "ingredient2",
            self.unit
        )
        ingredient3 = create_ingredient(
            "ingredient3",
            "ingredient3",
            self.unit
        )

        recipe_ing1 = create_recipe_ingredient(recipe1, ingredient1, 200)
        recipe_ing2 = create_recipe_ingredient(recipe1, ingredient3, 50)
        recipe_ing3 = create_recipe_ingredient(recipe2, ingredient1, 200)
        recipe_ing4 = create_recipe_ingredient(recipe2, ingredient2, 200)

        self.assertEqual(recipe_ing1.recipe.id, recipe1.id)
        self.assertEqual(recipe_ing1.ingredient.id, ingredient1.id)

        self.assertEqual(recipe_ing2.recipe.id, recipe1.id)
        self.assertEqual(recipe_ing2.ingredient.id, ingredient3.id)

        self.assertEqual(recipe_ing3.recipe.id, recipe2.id)
        self.assertEqual(recipe_ing3.ingredient.id, ingredient1.id)

        self.assertEqual(recipe_ing4.recipe.id, recipe2.id)
        self.assertEqual(recipe_ing4.ingredient.id, ingredient2.id)


class RecipeRatingModelTests(TestCase):
    """Test recipe rating model"""

    def setUp(self):
        self.user = setup_user()

    def test_create_recipe_rating(self):
        """Test creating recipe rating"""
        user1 = setup_user("teddy1")
        user2 = setup_user("teddy2")
        recipe1 = create_recipe("recipe1", self.user)
        recipe2 = create_recipe("recipe2", self.user)

        user_recipe_rating1 = create_recipe_rating(user1, recipe1, 4.5)
        user_recipe_rating2 = create_recipe_rating(user1, recipe2, 1.5)
        user_recipe_rating3 = create_recipe_rating(user2, recipe2, 3.5)

        self.assertEqual(user_recipe_rating1.user.id, user1.id)
        self.assertEqual(user_recipe_rating1.recipe.id, recipe1.id)

        self.assertEqual(user_recipe_rating2.user.id, user1.id)
        self.assertEqual(user_recipe_rating2.recipe.id, recipe2.id)

        self.assertEqual(user_recipe_rating3.user.id, user2.id)
        self.assertEqual(user_recipe_rating3.recipe.id, recipe2.id)


class RecipeTagModelTests(TestCase):
    """Test recipe tag"""

    def setUp(self):
        self.user = setup_user()

    def test_create_recipe_tag(self):
        """Test creating recipe tag"""
        recipe1 = create_recipe("recipe1", self.user)
        recipe2 = create_recipe("recipe2", self.user)
        tag1 = create_tag("tag1")
        tag2 = create_tag("tag2")

        recipe_tag1 = create_recipe_tag(recipe1, tag1)
        recipe_tag2 = create_recipe_tag(recipe1, tag2)
        recipe_tag3 = create_recipe_tag(recipe2, tag2)

        self.assertEqual(recipe_tag1.recipe.id, recipe1.id)
        self.assertEqual(recipe_tag1.tag.id, tag1.id)

        self.assertEqual(recipe_tag2.recipe.id, recipe1.id)
        self.assertEqual(recipe_tag2.tag.id, tag2.id)

        self.assertEqual(recipe_tag3.recipe.id, recipe2.id)
        self.assertEqual(recipe_tag3.tag.id, tag2.id)


class WatchlistModelTests(TestCase):
    """Test watchlist model"""

    def test_create_watchlist(self):
        """Test creating watchlist"""
        user1 = setup_user("teddy1")
        user2 = setup_user("teddy2")
        list_name1 = "watchlist1"
        list_name2 = "watchlist2"
        list_name3 = "watchlist3"

        watchlist1 = create_watchlist(user1, list_name1)
        watchlist2 = create_watchlist(user1, list_name2)
        watchlist3 = create_watchlist(user1, list_name3)
        watchlist4 = create_watchlist(user2, list_name3)

        self.assertEqual(watchlist1.user.id, user1.id)
        self.assertEqual(watchlist1.watchlist_name, list_name1)

        self.assertEqual(watchlist2.user.id, user1.id)
        self.assertEqual(watchlist2.watchlist_name, list_name2)

        self.assertEqual(watchlist3.user.id, user1.id)
        self.assertEqual(watchlist3.watchlist_name, list_name3)

        self.assertEqual(watchlist4.user.id, user2.id)
        self.assertEqual(watchlist4.watchlist_name, list_name3)


class RecipeWatchlistModelTests(TestCase):
    """Test recipe watchlist model"""

    def setUp(self):
        self.user = setup_user()

    def test_create_recipe_watchlist(self):
        """Test creating recipe watchlist"""
        watchlist1 = create_watchlist(self.user, "watchlist1")
        watchlist2 = create_watchlist(self.user, "watchlist2")
        recipe1 = create_recipe("recipe1", self.user)
        recipe2 = create_recipe("recipe2", self.user)
        recipe3 = create_recipe("recipe3", self.user)

        recipe_wl1 = create_recipe_watchlist(watchlist1, recipe1)
        recipe_wl2 = create_recipe_watchlist(watchlist1, recipe2)
        recipe_wl3 = create_recipe_watchlist(watchlist1, recipe3)
        recipe_wl4 = create_recipe_watchlist(watchlist2, recipe2)

        self.assertEqual(recipe_wl1.recipe.id, recipe1.id)
        self.assertEqual(recipe_wl1.watchlist.id, watchlist1.id)

        self.assertEqual(recipe_wl2.recipe.id, recipe2.id)
        self.assertEqual(recipe_wl2.watchlist.id, watchlist1.id)

        self.assertEqual(recipe_wl3.recipe.id, recipe3.id)
        self.assertEqual(recipe_wl3.watchlist.id, watchlist1.id)

        self.assertEqual(recipe_wl4.recipe.id, recipe2.id)
        self.assertEqual(recipe_wl4.watchlist.id, watchlist2.id)
