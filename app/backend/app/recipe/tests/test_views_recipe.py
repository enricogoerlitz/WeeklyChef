"""
Test recipe models api endpoints
Models:
Unit, Tag, Ingredient, Recipe
RecipeFavorite, RecipeImage, RecipeIngredient
RecipeRating, RecipeTag, Watchlist, RecipeWatchlist
"""
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core import models  # noqa
from core.tests.test_model_recipe import (  # noqa
    create_unit,
    create_tag,
    create_ingredient,
    create_recipe,
    create_recipe_favorite,
    create_recipe_image,
    create_recipe_ingredient,
    create_recipe_rating,
    create_recipe_tag,
    create_watchlist,
    create_recipe_watchlist
)
from recipe.tests.test_views_user import setup_login


URL_UNIT = "/api/v1/unit/"
URL_TAG = "/api/v1/tag/"
URL_INGREDIENT = "/api/v1/ingredient/"
URL_RECIPE = "/api/v1/recipe/"
URL_RECIPE_FAV = "/api/v1/recipe-favorite/"
URL_RECIPE_ING = "/api/v1/recipe-ingredient/"


def check_is_auth_required(client: APIClient, endpoint):
    res = client.get(endpoint)
    return res.status_code == status.HTTP_403_FORBIDDEN


class PublicRecipeAuthRequired(TestCase):
    """Test endpoints require an authorization token"""

    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required_unit(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(self.client, URL_UNIT)
        )

    def test_auth_required_tag(self):
        """Test auth required for tag endpoint"""
        self.assertTrue(
            check_is_auth_required(self.client, URL_TAG)
        )

    def test_auth_required_ingredient(self):
        """Test auth required for ingredient endpoint"""
        self.assertTrue(
            check_is_auth_required(self.client, URL_INGREDIENT)
        )
        
    def test_auth_required_recipe(self):
        """Test auth required for recipe endpoint"""
        self.assertTrue(
            check_is_auth_required(self.client, URL_RECIPE)
        )
        
    def test_auth_required_recipe_favorite(self):
        """Test auth required for recipe favorite endpoint"""
        self.assertTrue(
            check_is_auth_required(self.client, URL_RECIPE_FAV)
        )
        
    def test_auth_required_recipe_ingredient(self):
        """Test auth required for recipe ingredient endpoint"""
        self.assertTrue(
            check_is_auth_required(self.client, URL_RECIPE_ING)
        )


class PrivateUnitApiTests(TestCase):
    """Test model CRUD api endpoint
    NOTE: STAFF ONLY"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model, only staff"""
        pass

    def test_update(self):
        """Test update model, only staff"""
        pass

    def test_delete(self):
        """Test deleting model, only staff"""
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the model"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateTagApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model, only staff"""
        pass

    def test_update(self):
        """Test update model, only staff"""
        pass

    def test_delete(self):
        """Test deleting model, only staff"""
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateIngredientApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_filtered_ids(self):
        """Test get models filtered by ids"""
        pass

    def test_list_filtered_all(self):
        """Test get all models filtered by all"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model"""
        pass

    def test_update(self):
        """Test update model"""
        pass

    def test_delete(self):
        """Test deleting model, only staff"""
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateRecipeApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        pass

    def test_retrieve_details(self):
        """Test get model by id"""
        # RecipeDataSerializer
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_by_ids(self):
        """Test get all models filtered by ids"""
        pass

    def test_list_by_creator(self):
        """Test get all models filtered by creator-user-id"""
        pass

    def test_list_by_all(self):
        """Test get all models filtered by all"""
        pass

    def test_list_details(self):
        """Test get all models"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model"""
        pass

    def test_update(self):
        """Test update model"""
        pass

    def test_delete(self):
        """Test deleting model, only creator and staff"""
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateRecipeFavoriteApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """
        Test get model by id
        Only owner or staff
        """
        # RecipeFavoriteDataSerializer
        pass

    def test_retrieve_details(self):
        """Test get model by id only owner or staff"""
        pass

    def test_list(self):
        """Test get all models, only owner or staff"""
        pass

    def test_list_details(self):
        """Test get all models, only owner or staff"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model"""
        pass

    def test_update(self):
        """Test update model"""
        pass

    def test_delete(self):
        """Test deleting model, only owner or staff"""
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_retrieve_unauthorized(self):
        """Test trying getting foreign favorite"""
        pass

    def test_fail_list_unauthorized(self):
        """Test trying getting foreign favorite"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateRecipeIngredientApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        # RecipeIngredientDataSerializer
        pass

    def test_retrieve_details(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_by_recipe_ids(self):
        """Test get all models filtered by recipe ids"""
        pass

    def test_list_details(self):
        """Test get all models"""
        pass

    def test_list_details_by_recipe_ids(self):
        """Test get all models"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model, only owner or staff"""
        pass

    def test_update(self):
        """Test update model, only owner or staff"""
        pass

    def test_delete(self):
        """Test deleting model, only owner or staff"""
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateRecipeRatingApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        # RecipeRatingDataSerializer
        pass

    def test_retrieve_details(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_by_recipe_ids(self):
        """Test get all models"""
        pass

    def test_list_by_user_ids(self):
        """Test get all models"""
        pass

    def test_list_by_recipe_and_user_ids(self):
        """Test get all models"""
        pass

    def test_list_details(self):
        """Test get all models"""
        pass

    def test_list_details_by_recipe_ids(self):
        """Test get all models"""
        pass

    def test_list_details_by_user_ids(self):
        """Test get all models"""
        pass

    def test_list_details_by_recipe_and_ids(self):
        """Test get all models"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model"""
        pass

    def test_update(self):
        """Test update model"""
        pass

    def test_delete(self):
        """Test deleting model, only owner or staff"""
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateRecipeTagApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        # RecipeTagDataSerializer
        pass

    def test_retrieve_details(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_by_recipe_ids(self):
        """Test get all models filtered by recipe ids"""
        pass

    def test_list_by_tag_ids(self):
        """Test get all models filtered by tag ids"""
        pass

    def test_list_details(self):
        """Test get all models"""
        pass

    def test_list_details_by_recipe_ids(self):
        """Test get all models"""
        pass

    def test_list_details_by_tag_ids(self):
        """Test get all models"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model"""
        pass

    def test_update(self):
        """
        Test update model,
        only recipe owner or staff
        """
        pass

    def test_delete(self):
        """
        Test deleting model,
        only recipe owner or staff
        """
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateWatchlistTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id, only owner or staff"""
        pass

    def test_list(self):
        """Test get all models, only owner or staff"""
        pass

    def test_create(self):
        """Test creating model"""
        pass

    def test_patch(self):
        """Test update model, only owner or staff"""
        pass

    def test_update(self):
        """Test update model, only owner or staff"""
        pass

    def test_delete(self):
        """Test deleting model, only owner or staff"""
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass


class PrivateRecipeWatchlistApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        # RecipeWatchlistDataSerializer
        pass

    def test_retrieve_details(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_details(self):
        """Test get all models"""
        pass

    def test_create(self):
        """
        Test creating model,
        only watchlist owner or staff
        """
        pass

    def test_patch(self):
        """
        Test update model,
        only watchlist owner or staff
        """
        pass

    def test_update(self):
        """
        Test update model,
        only watchlist owner or staff
        """
        pass

    def test_delete(self):
        """
        Test deleting model,
        only watchlist owner or staff
        """
        pass

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_patch(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_update(self):
        """Test failing update model with invalid data"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass
