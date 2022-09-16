"""
Test recipe models api endpoints
Models:
Unit, Tag, Ingredient, Recipe
RecipeFavorite, RecipeImage, RecipeIngredient
RecipeRating, RecipeTag, Watchlist, RecipeWatchlist
"""
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core import models
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
from recipe import serializers
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


def id_url(url, id):
    return f"{url}{id}/"


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
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client, is_staff=True)

    def test_retrieve(self):
        """Test get model by id"""
        unit = create_unit("get_unit_name")
        serializer = serializers.UnitSerializer(unit)

        res = self.client.get(id_url(URL_UNIT, unit.id))
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list(self):
        """Test get all models"""
        units = [
            create_unit("list_unit1"),
            create_unit("list_unit2"),
        ]

        serializer = serializers.UnitSerializer(many=True, data=units)
        serializer.is_valid()
        
        res = self.client.get(URL_UNIT)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create(self):
        """Test creating model"""
        payload = {
            "unit_name": "post_unit"
        }

        res = self.client.post(URL_UNIT, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        unit = models.Unit.objects.get(id=res.data["id"])
        for key, value in payload.items():
            self.assertEqual(getattr(unit, key), value)
        
    def test_patch(self):
        """Test update model, only staff"""
        unit = create_unit("patch_base_unit")
        patch_payload = {
            "unit_name": "patch_unit"
        }

        res = self.client.patch(id_url(URL_UNIT, unit.id), patch_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        patched_unit = models.Unit.objects.get(id=unit.id)
        for key, value in patch_payload.items():
            self.assertEqual(getattr(patched_unit, key), value)

    def test_put(self):
        """Test update model, only staff"""
        unit = create_unit("patch_base_unit")
        put_payload = {
            "unit_name": "put_unit"
        }

        res = self.client.put(id_url(URL_UNIT, unit.id), put_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        patched_unit = models.Unit.objects.get(id=unit.id)
        for key, value in put_payload.items():
            self.assertEqual(getattr(patched_unit, key), value)

    def test_delete(self):
        """Test deleting model, only staff"""
        unit = create_unit("delete_unit")

        res = self.client.delete(id_url(URL_UNIT, unit.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            _ = models.Unit.objects.get(id=unit.id)

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        res = self.client.get(id_url(URL_UNIT, 100))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create_length(self):
        """Test failing validation. Not creating the model"""
        res_to_short = self.client.post(URL_UNIT, {"unit_name": ""})
        res_to_long = self.client.post(URL_UNIT, {
            "unit_name": "very very very to long"
        })

        self.assertEqual(
            res_to_short.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            res_to_long.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_fail_create_empty(self):
        """Test failing validation. Not creating the model"""
        res = self.client.post(URL_UNIT, {})
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_is_staff_only_access(self):
        """Test each route, is staff only allowed"""
        denied_client = APIClient()
        _ = setup_login(denied_client, username="teddy_auth_2")
        unit = create_unit("__new__")
        
        res_get = denied_client.get(URL_UNIT)
        res_post = denied_client.post(URL_UNIT, {"unit_name": "_new_"})
        res_put = denied_client.put(
            id_url(URL_UNIT, unit.id),
            {"unit_name": "___new___"}
        )
        res_patch = denied_client.patch(
            id_url(URL_UNIT, unit.id),
            {"unit_name": "__new__"}
        )
        res_delete = denied_client.delete(
            id_url(URL_UNIT, unit.id)
        )

        self.assertEqual(res_get.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_patch.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)


class PrivateTagApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)

    def test_retrieve(self):
        """Test get model by id"""
        tag = create_tag("get_tag_name")
        serializer = serializers.TagSerializer(tag)

        res = self.client.get(id_url(URL_TAG, tag.id))
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list(self):
        """Test get all models"""
        tags = [
            create_tag("list_tag1"),
            create_tag("list_tag2"),
        ]

        serializer = serializers.TagSerializer(many=True, data=tags)
        serializer.is_valid()
        
        res = self.client.get(URL_TAG)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create(self):
        """Test creating model"""
        payload = {
            "tag_name": "post_tag"
        }

        res = self.client.post(URL_TAG, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        unit = models.Tag.objects.get(id=res.data["id"])
        for key, value in payload.items():
            self.assertEqual(getattr(unit, key), value)

    def test_patch(self):
        """Test update model, only staff"""
        tag = create_tag("patch_base_tag")
        patch_payload = {
            "tag_name": "patch_tag"
        }

        res = self.client.patch(id_url(URL_TAG, tag.id), patch_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        patched_tag = models.Tag.objects.get(id=tag.id)
        for key, value in patch_payload.items():
            self.assertEqual(getattr(patched_tag, key), value)

    def test_put(self):
        """Test update model, only staff"""
        tag = create_tag("patch_base_tag")
        put_payload = {
            "tag_name": "put_tag"
        }

        res = self.client.put(id_url(URL_TAG, tag.id), put_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        patched_tag = models.Tag.objects.get(id=tag.id)
        for key, value in put_payload.items():
            self.assertEqual(getattr(patched_tag, key), value)

    def test_delete(self):
        """Test deleting model, only staff"""
        staff_client = APIClient()
        _ = setup_login(staff_client, is_staff=True, username="teddy_auth_2")
        tag = create_tag("teg_delete")

        tag_id_url = id_url(URL_TAG, tag.id)
        delete_res = staff_client.delete(tag_id_url)
        is_delete_res = staff_client.get(tag_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        res = self.client.get(id_url(URL_TAG, 100))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create_length(self):
        """Test failing validation. Not creating the object"""
        res_to_short = self.client.post(URL_TAG, {"tag_name": ""})
        res_to_long = self.client.post(URL_TAG, {
            "tag_name": "very very very very to long"
        })

        self.assertEqual(
            res_to_short.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            res_to_long.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_fail_create_empty(self):
        """Test failing validation. Not creating the model"""
        res = self.client.post(URL_TAG, {})
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        tag = create_tag("teg_delete")

        res = self.client.delete(id_url(URL_TAG, tag.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateIngredientApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.unit = create_unit("ing_unit")
        self.ingredient = create_ingredient(
            ingredient_name="ingredient1",
            ingredient_display_name="ingredient1",
            unit=self.unit
        )
        self.serializer = serializers.IngredientSerializer(
            self.ingredient
        )

    def test_retrieve(self):
        """Test get model by id"""
        ing_id = self.ingredient.id
        res = self.client.get(id_url(URL_INGREDIENT, ing_id))
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_list(self):
        """Test get all models"""
        ings = [
            self.ingredient,
            create_ingredient(
                ingredient_name="ingredient_list1",
                ingredient_display_name="ingredient_list1",
                unit=self.unit
            ),
            create_ingredient(
                ingredient_name="ingredient_list2",
                ingredient_display_name="ingredient_list2",
                unit=self.unit
            ),
        ]

        serializer_ = serializers.IngredientSerializer(
            many=True,
            data=ings
        )
        serializer_.is_valid()
        
        res = self.client.get(URL_INGREDIENT)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer_.data)

    def test_list_filtered_ids(self):
        """Test get models filtered by ids"""
        pass

    def test_list_filtered_all(self):
        """Test get all models filtered by all"""
        pass

    def test_create(self):
        """Test creating model"""
        # get_serializer_class -> if post -> post serializer!
        print("ID:")
        print(self.unit.id)
        payload = {
            "ingredient_name": "ingredient_name_create",
            "ingredient_display_name": "ingredient_name_create",
            "unit": self.unit.id,
            "default_price": 5.92,
            "quantity_per_unit": 200,
            "is_spices": False,
            "search_description": "good",
        }

        res = self.client.post(URL_INGREDIENT, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ingredient = models.Ingredient.objects.get(id=res.data["id"])
        for key, value in payload.items():
            print(f"{key}: {getattr(ingredient, key)}")
            self.assertEqual(getattr(ingredient, key), value)

    def test_patch(self):
        """Test update model"""
        pass

    def test_put(self):
        """Test update model"""
        pass

    def test_delete(self):
        """Test deleting model, only staff"""
        staff_client = APIClient()
        _ = setup_login(staff_client, is_staff=True, username="teddy_auth_2")
        ingredient = create_ingredient(
            ingredient_name="ingredient_name1",
            ingredient_display_name="ingredient_name1",
            unit=create_unit("unit1")
        )

        ing_id_url = id_url(URL_INGREDIENT, ingredient.id)
        delete_res = staff_client.delete(ing_id_url)
        is_delete_res = staff_client.get(ing_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        ingredient = create_ingredient(
            ingredient_name="ingredient_name1",
            ingredient_display_name="ingredient_name1",
            unit=create_unit("unit1")
        )

        res = self.client.delete(id_url(URL_INGREDIENT, ingredient.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


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

    def test_put(self):
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

    def test_put(self):
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

    def test_put(self):
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

    def test_put(self):
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

    def test_put(self):
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

    def test_put(self):
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

    def test_put(self):
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

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        pass
