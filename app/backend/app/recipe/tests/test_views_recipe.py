"""
Test recipe models api endpoints
Models:
Unit, Tag, Ingredient, Recipe
RecipeFavorite, RecipeImage, RecipeIngredient
RecipeRating, RecipeTag, Watchlist, RecipeWatchlist
"""
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from djdevted.test import (
    check_is_auth_required,
    get_payload_data,
    id_url,
)
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
from core.tests.test_model_user import create_user
from recipe import serializers
from recipe.tests.test_views_user import setup_login


URL_UNIT = "/api/v1/unit/"
URL_TAG = "/api/v1/tag/"
URL_INGREDIENT = "/api/v1/ingredient/"
URL_RECIPE = "/api/v1/recipe/"
URL_RECIPE_FAV = "/api/v1/recipe-favorite/"
URL_RECIPE_ING = "/api/v1/recipe-ingredient/"
URL_RECIPE_RAT = "/api/v1/recipe-rating/"
URL_RECIPE_TAG = "/api/v1/recipe-tag/"
URL_WATCHLIST = "/api/v1/watchlist/"
URL_RECIPE_WLIST = "/api/v1/recipe-watchlist/"


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

        ingredient = models.Ingredient.objects.get(
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
        # usernames = [user.username for user in User.objects.all()]
        # ^ eg is normal and queryset is iterable
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

        recipe = models.Recipe.objects.get(
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
        denied_client = APIClient()
        _ = setup_login(denied_client, is_staff=False, username="teddy_auth_4")

        recipe_id_url = id_url(URL_RECIPE, self.recipe.id)
        delete_res = denied_client.delete(recipe_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRecipeFavoriteApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user1 = setup_login(self.client)
        self.user2 = create_user("user2")
        self.recipe1 = create_recipe(
            "recipe_fav1",
            self.user1
        )
        self.recipe2 = create_recipe(
            "recipe_fav2",
            self.user1
        )
        self.recipe_fav = create_recipe_favorite(
            create_user("dummy_rf"),
            self.recipe1
        )
        self.serializer = serializers.RecipeFavoriteSerializer(self.recipe_fav)

    def test_retrieve(self):
        """
        Test get model by id
        Only owner or staff
        """
        recipe_fav = create_recipe_favorite(self.user1, self.recipe1)
        recipe_fav_id = recipe_fav.id
        serializer = serializers.RecipeFavoriteSerializer(recipe_fav)

        res = self.client.get(id_url(URL_RECIPE_FAV, recipe_fav_id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_details(self):
        """Test get model by id only owner or staff"""
        pass

    def test_list(self):
        """Test get all models, only owner or staff"""
        # user2 recipes should not be shown!
        create_recipe_favorite(
            self.user2,
            self.recipe1,
        ),
        create_recipe_favorite(
            self.user2,
            self.recipe2,
        ),
        payload = [
            create_recipe_favorite(
                self.user1,
                self.recipe1,
            ),
            create_recipe_favorite(
                self.user1,
                self.recipe2,
            ),
        ]
        payload_data = get_payload_data(
            serializers.RecipeFavoriteSerializer,
            payload,
            True
        )

        res = self.client.get(URL_RECIPE_FAV)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_list_details(self):
        """Test get all models, only owner or staff"""
        pass

    def test_create(self):
        """Test creating model"""
        payload = {
            "user": create_user("recipe_fav_user").id,
            "recipe": self.recipe1.id,
        }
        payload_data = get_payload_data(
            serializers.RecipeFavoriteSerializer,
            payload
        )

        res = self.client.post(URL_RECIPE_FAV, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ingredient = models.RecipeFavorite.objects.get(id=res.data["id"])
        res_data = serializers.RecipeFavoriteSerializer(ingredient).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_delete(self):
        """Test deleting model, only owner or staff"""
        staff_client = APIClient()
        user = setup_login(staff_client, username="teddy_auth_rf")
        recipe_fav = create_recipe_favorite(user, self.recipe1)

        rf_id_url = id_url(URL_RECIPE_FAV, recipe_fav.id)
        delete_res = staff_client.delete(rf_id_url)
        is_delete_res = staff_client.get(rf_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        res = self.client.get(id_url(URL_RECIPE_FAV, 100))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_retrieve_unauthorized(self):
        """Test trying getting foreign favorite"""
        denied_client = APIClient()
        _ = setup_login(denied_client, username="denied_user")

        res = denied_client.get(id_url(URL_RECIPE_FAV, self.recipe_fav.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_create_duplicate_key(self):
        """Test failing validation. Not creating the object"""
        payload = {**self.serializer.data}
        res = self.client.post(URL_RECIPE_FAV, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        denied_client = APIClient()
        _ = setup_login(denied_client, username="denied_user")

        res = denied_client.get(id_url(URL_RECIPE_FAV, self.recipe_fav.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRecipeIngredientApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.recipe = create_recipe("ri_recipe1", self.user)
        self.unit = create_unit("ri_unit")
        self.recipe_ing = create_recipe_ingredient(
            self.recipe,
            create_ingredient(
                "ing_name_ri",
                "ing_name_ri",
                self.unit
            ),
            400
        )
        self.serializer = serializers.RecipeIngredientSerializer(
            self.recipe_ing
        )

    def test_retrieve(self):
        """Test get model by id"""
        res = self.client.get(id_url(URL_RECIPE_ING, self.recipe_ing.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_retrieve_details(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        ing1 = create_ingredient(
            "recipe_ing1_ri",
            "recipe_ing1_ri",
            self.unit
        )
        ing2 = create_ingredient(
            "recipe_ing2_ri",
            "recipe_ing2_ri",
            self.unit
        )
        payload = [
            self.recipe_ing,
            create_recipe_ingredient(
                self.recipe,
                ing1
            ),
            create_recipe_ingredient(
                self.recipe,
                ing2
            ),
        ]
        payload_data = get_payload_data(
            serializers.RecipeIngredientSerializer,
            payload,
            True
        )

        res = self.client.get(URL_RECIPE_ING)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_list_details(self):
        """Test get all models"""
        pass

    def test_create(self):
        """Test creating model"""
        ingredient = create_ingredient(
            "ing_name1",
            "ing_name1",
            self.unit
        )
        payload = {
            "recipe": self.recipe.id,
            "ingredient": ingredient.id,
            "unit_quantity": 250
        }
        payload_data = get_payload_data(
            serializers.RecipeIngredientSerializer,
            payload
        )

        res = self.client.post(URL_RECIPE_ING, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ingredient = models.RecipeIngredient.objects.get(id=res.data["id"])
        res_data = serializers.RecipeIngredientSerializer(ingredient).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_patch(self):
        """Test update model"""
        recipe_ing_id = self.recipe_ing.id
        payload = {**self.serializer.data}
        payload["unit_quantity"] = 18921

        res = self.client.patch(id_url(URL_RECIPE_ING, recipe_ing_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe_ing = models.RecipeIngredient.objects.get(id=recipe_ing_id)
        self.assertEqual(
            recipe_ing.unit_quantity,
            payload["unit_quantity"]
        )

    def test_delete(self):
        """Test deleting model, only owner or staff"""
        rf_id_url = id_url(URL_RECIPE_ING, self.recipe_ing.id)
        delete_res = self.client.delete(rf_id_url)
        is_delete_res = self.client.get(rf_id_url)
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        res = self.client.get(id_url(URL_RECIPE_ING, 100))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create_not_auth(self):
        """Test failing auth. Not creating the object"""
        denied_client = APIClient()
        _ = setup_login(denied_client, username="denied_user1")
        ingredient = create_ingredient(
            "ing_name132",
            "ing_name12",
            self.unit
        )
        payload = {
            "recipe": self.recipe.id,
            "ingredient": ingredient.id,
            "unit_quantity": 250
        }

        res = denied_client.post(URL_RECIPE_ING, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        ri_id_url = id_url(URL_RECIPE_ING, self.recipe_ing.id)
        delete_res = self.client.delete(ri_id_url)
        is_delete_res = self.client.get(ri_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)


class PrivateRecipeRatingApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.recipe1 = create_recipe("rr_recipe1", self.user)
        self.recipe2 = create_recipe("rr_recipe2", self.user)
        self.recipe_rat = create_recipe_rating(
            self.user,
            self.recipe1,
            4.5
        )
        self.serializer = serializers.RecipeRatingSerializer(
            self.recipe_rat
        )

    def test_retrieve(self):
        """Test get model by id"""
        res = self.client.get(
            id_url(URL_RECIPE_RAT, self.recipe_rat.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_retrieve_details(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        payload = [
            self.recipe_rat,
            create_recipe_rating(self.user, self.recipe2, 3.5),
        ]
        payload_data = get_payload_data(
            serializers.RecipeRatingSerializer,
            payload,
            True
        )

        res = self.client.get(URL_RECIPE_RAT)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

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
        recipe_id = create_recipe("rr_recipe3", self.user).id
        payload = {
            "user": self.user.id,
            "recipe": recipe_id,
            "rating": 1.5,
        }
        payload_data = get_payload_data(
            serializers.RecipeRatingSerializer,
            payload
        )

        res = self.client.post(URL_RECIPE_RAT, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = models.RecipeRating.objects.get(id=res.data["id"])
        res_data = serializers.RecipeRatingSerializer(recipe).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_patch(self):
        """Test update model"""
        payload = {
            "rating": 2.5
        }

        res = self.client.patch(
            id_url(URL_RECIPE_RAT, self.recipe_rat.id),
            payload,
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe_rat = models.RecipeRating.objects.get(id=res.data["id"])
        self.assertEqual(recipe_rat.rating, payload["rating"])

    def test_delete(self):
        """Test deleting model, only owner or staff"""
        owner_client = self.client

        recipe_id_url = id_url(URL_RECIPE_RAT, self.recipe_rat.id)
        delete_res = owner_client.delete(recipe_id_url)
        is_delete_res = owner_client.get(recipe_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        res = self.client.get(id_url(URL_RECIPE_RAT, 100))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        payload_min = {**self.serializer.data}
        payload_max = {**self.serializer.data}
        payload_min["rating"] = -1
        payload_max["rating"] = 5.5

        res_min = self.client.post(URL_RECIPE_RAT, payload_min)
        res_max = self.client.post(URL_RECIPE_RAT, payload_max)

        self.assertEqual(res_max.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_min.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        staff_client = APIClient()
        _ = setup_login(staff_client, is_staff=False, username="teddy_auth_rr")

        recipe_rat_id_url = id_url(URL_RECIPE_RAT, self.recipe_rat.id)
        delete_res = staff_client.delete(recipe_rat_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRecipeTagApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.recipe = create_recipe("rt_recipe", self.user)
        self.tag1 = create_tag("rr_tag1")
        self.tag2 = create_tag("rr_tag2")
        self.tag3 = create_tag("rr_tag3")
        self.recipe_tag = create_recipe_tag(
            self.recipe,
            self.tag1
        )
        self.serializer = serializers.RecipeTagSerializer(
            self.recipe_tag
        )

    def test_retrieve(self):
        """Test get model by id"""
        res = self.client.get(
            id_url(URL_RECIPE_TAG, self.recipe_tag.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_retrieve_details(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        payload = [
            self.recipe_tag,
            create_recipe_tag(self.recipe, self.tag2),
            create_recipe_tag(self.recipe, self.tag3),
        ]
        payload_data = get_payload_data(
            serializers.RecipeTagSerializer,
            payload,
            True
        )

        res = self.client.get(URL_RECIPE_TAG)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

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
        tag_id = create_tag("create_rr_test").id
        payload = {
            "recipe": self.recipe.id,
            "tag": tag_id,
        }
        payload_data = get_payload_data(
            serializers.RecipeTagSerializer,
            payload
        )

        res = self.client.post(URL_RECIPE_TAG, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = models.RecipeTag.objects.get(id=res.data["id"])
        res_data = serializers.RecipeTagSerializer(recipe).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_delete(self):
        """
        Test deleting model,
        only recipe owner or staff
        """
        recipe_tag_id_url = id_url(URL_RECIPE_TAG, self.recipe_tag.id)
        delete_res = self.client.delete(recipe_tag_id_url)
        is_delete_res = self.client.get(recipe_tag_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        denied_client = APIClient()
        _ = setup_login(denied_client, username="rt_username")

        delete_id_url = id_url(URL_RECIPE_TAG, self.recipe_tag.id)
        res = denied_client.delete(delete_id_url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateWatchlistTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.watchlist = create_watchlist(self.user, "wlist1")
        self.serializer = serializers.WatchlistSerializer(
            self.watchlist
        )

    def test_retrieve(self):
        """Test get model by id, only owner or staff"""
        res = self.client.get(
            id_url(URL_WATCHLIST, self.watchlist.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_list(self):
        """Test get all models, only owner or staff"""
        payload = [
            self.watchlist,
            create_watchlist(self.user, "wlist2"),
            create_watchlist(self.user, "wlist3"),
        ]
        payload_data = get_payload_data(
            serializers.WatchlistSerializer,
            payload,
            True
        )

        res = self.client.get(URL_WATCHLIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_create(self):
        """Test creating model"""
        payload = {
            "user": self.user.id,
            "watchlist_name": "new_wlist",
        }
        payload_data = get_payload_data(
            serializers.WatchlistSerializer,
            payload
        )

        res = self.client.post(URL_WATCHLIST, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        wlist = models.Watchlist.objects.get(id=res.data["id"])
        res_data = serializers.WatchlistSerializer(wlist).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_patch(self):
        """Test update model, only owner or staff"""
        wlist_id = self.watchlist.id
        payload = {
            "watchlist_name": "wlist_patch",
        }

        res = self.client.patch(id_url(URL_WATCHLIST, wlist_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        wlist = models.Watchlist.objects.get(id=wlist_id)
        self.assertEqual(
            wlist.watchlist_name,
            payload["watchlist_name"]
        )

    def test_put(self):
        """Test update model, only owner or staff"""
        wlist_id = self.watchlist.id
        payload = {**self.serializer.data}
        payload["watchlist_name"] = "wlist_put"

        res = self.client.put(id_url(URL_WATCHLIST, wlist_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        wlist = models.Watchlist.objects.get(id=wlist_id)
        self.assertEqual(
            wlist.watchlist_name,
            payload["watchlist_name"]
        )

    def test_delete(self):
        """Test deleting model, only owner or staff"""
        owner_client = self.client

        wlist_id_url = id_url(URL_WATCHLIST, self.watchlist.id)
        delete_res = owner_client.delete(wlist_id_url)
        is_delete_res = owner_client.get(wlist_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_retrieve(self):
        """Test failing get not existing model"""
        res = self.client.get(id_url(URL_WATCHLIST, 100))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        payload = {
            "watchlist_name": "---"
        }

        res = self.client.post(URL_WATCHLIST, payload)

        # should contain an error dict with the validation error fields
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("watchlist_name", res.data)

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        denied_client = APIClient()
        _ = setup_login(denied_client, is_staff=False, username="teddy_auth_4")

        watchlist_id_url = id_url(URL_WATCHLIST, self.watchlist.id)
        delete_res = denied_client.delete(watchlist_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRecipeWatchlistApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.recipe1 = create_recipe("recipe_rw_1", self.user)
        self.recipe2 = create_recipe("recipe_rw_2", self.user)
        self.wlist1 = create_watchlist(self.user, "wlist_rw1")
        self.wlist2 = create_watchlist(
            create_user("wlist2_username"),
            "wlist_rw2"
        )
        self.recipe_wlist = create_recipe_watchlist(
            self.wlist1,
            self.recipe1
        )
        self.serializer = serializers.RecipeWatchlistSerializer(
            self.recipe_wlist
        )

    def test_retrieve(self):
        """Test get model by id"""
        res = self.client.get(
            id_url(URL_RECIPE_WLIST, self.recipe_wlist.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_retrieve_details(self):
        """Test get model by id"""
        pass

    def test_list(self):
        """Test get all models"""
        payload = [
            self.recipe_wlist,
            create_recipe_watchlist(
                self.wlist1,
                self.recipe2
            ),
            create_recipe_watchlist(
                self.wlist2,
                self.recipe1
            ),
        ]
        payload_data = get_payload_data(
            serializers.RecipeWatchlistSerializer,
            payload,
            True
        )

        res = self.client.get(URL_RECIPE_WLIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_list_details(self):
        """Test get all models"""
        pass

    def test_create(self):
        """
        Test creating model,
        only watchlist owner or staff
        """
        payload = {
            "watchlist": self.wlist2.id,
            "recipe": self.recipe2.id,
        }
        payload_data = get_payload_data(
            serializers.RecipeWatchlistSerializer,
            payload
        )

        res = self.client.post(URL_RECIPE_WLIST, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe_wlist = models.RecipeWatchlist.objects.get(id=res.data["id"])
        res_data = serializers.RecipeWatchlistSerializer(recipe_wlist).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_delete(self):
        """
        Test deleting model,
        only watchlist owner or staff
        """
        recipe_wlist_id_url = id_url(URL_RECIPE_WLIST, self.recipe_wlist.id)
        delete_res = self.client.delete(recipe_wlist_id_url)
        is_delete_res = self.client.get(recipe_wlist_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_fail(self):
        """Test creating only recipe owner or staff"""
        denied_client = APIClient()
        _ = setup_login(denied_client, is_staff=False, username="teddy_auth_4")
        payload = {
            "watchlist": self.wlist2.id,
            "recipe": self.recipe1.id,
        }

        res = denied_client.post(URL_RECIPE_WLIST, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_fail_delete(self):
        """Test deleting deleting model, no authorization"""
        denied_client = APIClient()
        _ = setup_login(denied_client, is_staff=False, username="teddy_auth_4")

        recipe_wlist_id_url = id_url(URL_RECIPE_WLIST, self.recipe_wlist.id)
        delete_res = denied_client.delete(recipe_wlist_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)
