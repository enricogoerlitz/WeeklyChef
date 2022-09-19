"""
Test recipe models api endpoints
Models:
Unit, Tag, Ingredient, Recipe
RecipeFavorite, RecipeImage, RecipeIngredient
RecipeRating, RecipeTag, Watchlist, RecipeWatchlist
"""
from decimal import Decimal
from typing import Callable, Union

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.serializers import ModelSerializer
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


def check_is_auth_required(client: APIClient, endpoint: str):
    res = client.get(endpoint)
    return res.status_code == status.HTTP_403_FORBIDDEN


def id_url(url: str, id: int):
    return f"{url}{id}/"


def get_payload_data(
    Serializer_class: Callable,
    payload: Union[list, dict],
    many=False
) -> dict:
    serializer: ModelSerializer = Serializer_class(many=many, data=payload)
    serializer.is_valid()
    return serializer.data


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
        payload = [
            create_unit("list_unit1"),
            create_unit("list_unit2"),
        ]
        payload_data = get_payload_data(
            serializers.UnitSerializer,
            payload,
            True
        )
        
        res = self.client.get(URL_UNIT)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_create(self):
        """Test creating model"""
        payload = {
            "unit_name": "post_unit"
        }
        payload_data = get_payload_data(
            serializers.UnitSerializer,
            payload
        )

        res = self.client.post(URL_UNIT, payload)
        res_data = res.data
        del res_data["id"]

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, payload_data)
        
    def test_patch(self):
        """Test update model, only staff"""
        unit = create_unit("patch_base_unit")
        payload = {
            "unit_name": "patch_unit"
        }
        payload_data = get_payload_data(
            serializers.UnitSerializer,
            payload
        )

        res = self.client.patch(id_url(URL_UNIT, unit.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patched_unit = models.Unit.objects.get(id=unit.id)
        res_data = serializers.UnitSerializer(patched_unit).data
        del res_data["id"]

        self.assertEqual(res_data, payload_data)

    def test_put(self):
        """Test update model, only staff"""
        unit = create_unit("patch_base_unit")
        payload = {
            "unit_name": "put_unit"
        }
        payload_data = get_payload_data(
            serializers.UnitSerializer,
            payload
        )

        res = self.client.put(id_url(URL_UNIT, unit.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patched_unit = models.Unit.objects.get(id=unit.id)
        res_data = serializers.UnitSerializer(patched_unit).data
        del res_data["id"]
        self.assertEqual(res_data, payload_data)

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
        payload = [
            create_tag("list_tag1"),
            create_tag("list_tag2"),
        ]
        payload_data = get_payload_data(
            serializers.TagSerializer,
            payload,
            True
        )
        
        res = self.client.get(URL_TAG)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_create(self):
        """Test creating model"""
        payload = {
            "tag_name": "post_tag"
        }
        payload_data = get_payload_data(
            serializers.TagSerializer,
            payload
        )

        res = self.client.post(URL_TAG, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        tag = models.Tag.objects.get(id=res.data["id"])
        res_data = serializers.TagSerializer(tag).data
        del res_data["id"]

        self.assertEqual(res_data, payload_data)

    def test_patch(self):
        """Test update model, only staff"""
        tag = create_tag("patch_base_tag")
        payload = {
            "tag_name": "patch_tag"
        }
        payload_data = get_payload_data(
            serializers.TagSerializer,
            payload
        )

        res = self.client.patch(id_url(URL_TAG, tag.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patched_tag = models.Tag.objects.get(id=tag.id)
        res_data = serializers.TagSerializer(patched_tag).data
        del res_data["id"]

        self.assertEqual(res_data, payload_data)

    def test_put(self):
        """Test update model, only staff"""
        tag = create_tag("patch_base_tag")
        payload = {
            "tag_name": "put_tag"
        }
        payload_data = get_payload_data(
            serializers.TagSerializer,
            payload
        )

        res = self.client.put(id_url(URL_TAG, tag.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patched_tag = models.Tag.objects.get(id=tag.id)
        res_data = serializers.TagSerializer(patched_tag).data
        del res_data["id"]

        self.assertEqual(res_data, payload_data)

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
        self.serializer = serializers.IngredientDetailSerializer(
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
        payload = [
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
        payload_data = get_payload_data(
            serializers.IngredientDetailSerializer,
            payload,
            True
        )
        
        res = self.client.get(URL_INGREDIENT)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_list_filtered_ids(self):
        """Test get models filtered by ids"""
        pass

    def test_list_filtered_all(self):
        """Test get all models filtered by all"""
        pass

    def test_create(self):
        """Test creating model"""
        payload = {
            "ingredient_name": "ingredient_name_create",
            "ingredient_display_name": "ingredient_name_create",
            "unit": self.unit.id,
            "default_price": 5.92,
            "quantity_per_unit": 200.00,
            "is_spices": False,
            "search_description": "good",
        }
        payload_data = get_payload_data(
            serializers.IngredientSerializer,
            payload
        )

        res = self.client.post(URL_INGREDIENT, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ingredient = models.Ingredient.objects.get(id=res.data["id"])
        res_data = serializers.IngredientSerializer(ingredient).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_patch(self):
        """Test update model"""
        ing_id = self.ingredient.id
        payload = {
            "ingredient_name": "MyNewIngredientName",
            "default_price": 10.28,
        }

        res = self.client.patch(id_url(URL_INGREDIENT, ing_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredient = models.Ingredient.objects.get(id=ing_id)
        self.assertEqual(
            ingredient.ingredient_name,
            payload["ingredient_name"]
        )
        self.assertEqual(
            ingredient.default_price,
            Decimal(str(payload["default_price"]))
        )

    def test_put(self):
        """Test update model"""
        ing_id = self.ingredient.id
        unit = create_unit("new_unit")
        payload = {**self.serializer.data}
        payload["search_description"] = "search_edited"
        payload["unit"] = unit.id
        payload["quantity_per_unit"] = 1872

        res = self.client.put(id_url(URL_INGREDIENT, ing_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredient: models.Ingredient = models.Ingredient.objects.get(
            id=ing_id
        )
        self.assertEqual(
            ingredient.search_description,
            payload["search_description"]
        )
        self.assertEqual(
            ingredient.quantity_per_unit,
            payload["quantity_per_unit"]
        )
        self.assertEqual(
            ingredient.unit.id,
            payload["unit"]
        )

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
        res = self.client.get(id_url(URL_INGREDIENT, 100))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create_min_value_and_length(self):
        """Test failing validation. Not creating the object"""
        payload = {**self.serializer.data}
        del payload["id"]
        payload["unit"] = self.unit.id
        payload["ingredient_name"] = ""
        payload["ingredient_display_name"] = ""
        payload["default_price"] = -1
        payload["quantity_per_unit"] = -1

        res = self.client.post(URL_INGREDIENT, payload)

        # should contain an error dict with the validation error fields
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ingredient_name", res.data)
        self.assertIn("ingredient_display_name", res.data)
        self.assertIn("default_price", res.data)
        self.assertIn("quantity_per_unit", res.data)
    
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
        self.recipe = create_recipe("Spagetti", self.user)
        self.serializer = serializers.RecipeSerializer(
            self.recipe
        )

    def test_retrieve(self):
        """Test get model by id"""
        res = self.client.get(
            id_url(URL_RECIPE, self.recipe.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_retrieve_details(self):
        """Test get model by id"""
        # RecipeDataSerializer
        # {
        #     id,
        #     recipe_name,
        #     user: {},
        #     person_count,
        #     prep_description,
        #     cooking_duration_min,
        #     ingredients: [
        #         {...}
        #     ],
        #     tags: [
        #         {...}
        #     ],
        #     image: {...}
        # }
        pass

    def test_list(self):
        """Test get all models"""
        payload = [
            self.recipe,
            create_recipe("recipe1", self.user),
            create_recipe("recipe2", self.user),
        ]
        payload_data = get_payload_data(
            serializers.RecipeSerializer,
            payload,
            True
        )

        res = self.client.get(URL_RECIPE)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

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
        payload = {
            "recipe_name": "recipe_post",
            "user": self.user.id,
            "person_count": 5,
            "prep_description": "my good recipe description",
            "cooking_duration_min": 180,
        }
        payload_data = get_payload_data(
            serializers.RecipeSerializer,
            payload
        )

        res = self.client.post(URL_RECIPE, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = models.Recipe.objects.get(id=res.data["id"])
        res_data = serializers.RecipeSerializer(recipe).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_patch(self):
        """Test update model"""
        recipe_id = self.recipe.id
        payload = {
            "recipe_name": "NewRecipeName",
            "person_count": 3,
        }

        res = self.client.patch(id_url(URL_RECIPE, recipe_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe = models.Recipe.objects.get(id=recipe_id)
        self.assertEqual(
            recipe.recipe_name,
            payload["recipe_name"]
        )
        self.assertEqual(
            recipe.person_count,
            payload["person_count"]
        )

    def test_put(self):
        """Test update model"""
        recipe_id = self.recipe.id
        payload = {**self.serializer.data}
        payload["recipe_name"] = "recipe_name_edited"
        payload["prep_description"] = "Updated prep description"
        payload["cooking_duration_min"] = 30

        res = self.client.put(id_url(URL_RECIPE, recipe_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe: models.Recipe = models.Recipe.objects.get(
            id=recipe_id
        )
        self.assertEqual(
            recipe.recipe_name,
            payload["recipe_name"]
        )
        self.assertEqual(
            recipe.prep_description,
            payload["prep_description"]
        )
        self.assertEqual(
            recipe.cooking_duration_min,
            payload["cooking_duration_min"]
        )

    def test_delete_as_owner(self):
        """Test deleting model, as creator"""
        owner_client = self.client

        recipe_id_url = id_url(URL_RECIPE, self.recipe.id)
        delete_res = owner_client.delete(recipe_id_url)
        is_delete_res = owner_client.get(recipe_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_as_staff(self):
        """Test deleting model, as staff"""
        staff_client = APIClient()
        _ = setup_login(staff_client, is_staff=True, username="teddy_auth_3")

        recipe_id_url = id_url(URL_RECIPE, self.recipe.id)
        delete_res = staff_client.delete(recipe_id_url)
        is_delete_res = staff_client.get(recipe_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        res = self.client.get(id_url(URL_RECIPE, 100))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        payload = {**self.serializer.data}
        del payload["id"]
        payload["recipe_name"] = ""
        payload["person_count"] = 0
        payload["prep_description"] = ""
        payload["cooking_duration_min"] = 0

        res = self.client.post(URL_RECIPE, payload)

        # should contain an error dict with the validation error fields
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("recipe_name", res.data)
        self.assertIn("person_count", res.data)
        self.assertIn("prep_description", res.data)
        self.assertIn("cooking_duration_min", res.data)
    
    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        staff_client = APIClient()
        _ = setup_login(staff_client, is_staff=False, username="teddy_auth_4")

        recipe_id_url = id_url(URL_RECIPE, self.recipe.id)
        delete_res = staff_client.delete(recipe_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)


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
