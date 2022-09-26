"""
Test cart models api endpoints
DayTime, RecipeCart, RecipeCartIngredient
"""
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.test import APIClient
from rest_framework import status
from core.tests.test_model_recipe import create_ingredient, create_unit


from djdevted.test import (  # noqa
    check_is_auth_required,
    get_payload_data,
    id_url,
)

from core import models
from core.tests.test_model_cart import (
    create_day_time,
    create_recipe_cart,
    create_recipe_cart_ingredient,
)
from core.tests.test_model_food_shop import create_food_shop
from recipe import serializers
from recipe.tests.test_views_user import setup_login

URL_DAY_TIME = "/api/v1/day-time/"
URL_RECIPE_CART = "/api/v1/recipe-cart/"
URL_RECIPE_CART_ING = "/api/v1/recipe-cart-ingredient/"


class PublicCartAuthRequired(TestCase):
    """Test endpoints require an authorization token"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_day_time(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_DAY_TIME
            )
        )

    def test_auth_required_recipe_cart(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_RECIPE_CART
            )
        )

    def test_auth_required_recipe_cart_ingredient(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_RECIPE_CART_ING
            )
        )


class PrivateDayTimeApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.daytime = create_day_time("daytime1")
        self.serializer = serializers.DayTimeSerializer(
            self.daytime
        )

    def test_retrieve(self):
        """Test get model by id"""
        url = id_url(URL_DAY_TIME, self.daytime.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_list(self):
        """Test get all models"""
        payload = [
            self.daytime,
            create_day_time("daytime2"),
        ]
        payload_data = get_payload_data(
            serializers.DayTimeSerializer,
            payload,
            True
        )

        res = self.client.get(URL_DAY_TIME)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_create(self):
        """Test creating model"""
        payload = {
            "day_time_name": "post_dt"
        }
        payload_data = get_payload_data(
            serializers.DayTimeSerializer,
            payload
        )

        res = self.client.post(URL_DAY_TIME, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res_data = res.data
        del res_data["id"]
        self.assertEqual(res.data, payload_data)

    def test_delete(self):
        """Test deleting model, as staff user"""
        access_client = APIClient()
        _ = setup_login(access_client, True, "access_username")
        url = id_url(URL_DAY_TIME, self.daytime.id)
        res = access_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            _ = models.Unit.objects.get(id=self.daytime.id)

    def test_fail_create_length(self):
        """Test failing validation. Not creating the model"""
        res_to_short = self.client.post(URL_DAY_TIME, {"day_time_name": ""})
        res_to_long = self.client.post(URL_DAY_TIME, {
            "day_time_name": "very very very to long"
        })

        self.assertEqual(
            res_to_short.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            res_to_long.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_fail_delete(self):
        """Test deleting model, no authorization"""
        denied_client = APIClient()
        _ = setup_login(denied_client, username="denied_username")
        url = id_url(URL_DAY_TIME, self.daytime.id)
        res = denied_client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRecipeCartApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.foodshop = create_food_shop("shopname1")
        self.daytime = create_day_time("daytime1")
        self.cart = create_recipe_cart(
            self.user,
            self.foodshop,
            self.daytime,
        )
        self.serializer = serializers.RecipeCartSerializer(
            self.cart
        )

    def test_retrieve(self):
        """Test get model by id"""
        url = id_url(URL_RECIPE_CART, self.cart.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_list(self):
        """Test get all models"""
        payload = [
            self.cart,
            create_recipe_cart(
                self.user,
                self.foodshop,
                self.daytime,
            ),
        ]
        payload_data = get_payload_data(
            serializers.RecipeCartSerializer,
            payload,
            True
        )

        res = self.client.get(URL_RECIPE_CART)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_create(self):
        """Test creating model"""
        payload = {
            "user": self.user.id,
            "date": "2022-02-05",
            "day_time": self.daytime.id,
            "recipe_name": "my_recipe_name",
            "food_shop": self.foodshop.id,
        }
        payload_data = get_payload_data(
            serializers.RecipeCartSerializer,
            payload
        )

        res = self.client.post(URL_RECIPE_CART, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res_data = res.data
        del res_data["id"]
        self.assertEqual(res.data, payload_data)

    def test_patch(self):
        """Test update model"""
        payload = {
            "recipe_name": "my_recipe_new",
        }

        url = id_url(URL_RECIPE_CART, self.cart.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["recipe_name"], payload["recipe_name"])

    def test_put(self):
        """Test update model"""
        id = self.cart.id
        payload = {**self.serializer.data}
        payload["recipe_name"] = "r_name_put"

        res = self.client.put(id_url(URL_RECIPE_CART, id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        model = models.RecipeCart.objects.get(
            id=id
        )
        self.assertEqual(
            model.recipe_name,
            payload["recipe_name"]
        )

    def test_fail_create_length(self):
        """Test failing validation. Not creating the model"""
        res_to_short = self.client.post(URL_RECIPE_CART, {"recipe_name": ""})
        res_to_long = self.client.post(URL_RECIPE_CART, {
            "recipe_name": "very very very to long"
        })

        self.assertEqual(
            res_to_short.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            res_to_long.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_delete(self):
        """Test deleting model, as staff user"""
        url = id_url(URL_RECIPE_CART, self.cart.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            _ = models.RecipeCart.objects.get(id=self.cart.id)

    def test_fail_delete(self):
        """Test deleting model, no authorization"""
        denied_client = APIClient()
        _ = setup_login(denied_client, username="denied_username")
        url = id_url(URL_RECIPE_CART, self.cart.id)
        res = denied_client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRecipeCartIngredientApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client)
        self.foodshop = create_food_shop("shopname1")
        self.daytime = create_day_time("daytime1")
        self.unit = create_unit("unit_name")
        self.cart1 = create_recipe_cart(
            self.user,
            self.foodshop,
            self.daytime,
        )
        self.cart2 = create_recipe_cart(
            self.user,
            self.foodshop,
            self.daytime,
        )
        self.ingredient1 = create_ingredient(
            "ing_name:1",
            "ing_name:1",
            self.unit
        )
        self.ingredient2 = create_ingredient(
            "ing_name:2",
            "ing_name:2",
            self.unit
        )
        self.cart_ing = create_recipe_cart_ingredient(
            self.cart1,
            self.ingredient1,
        )
        self.serializer = serializers.RecipeCartIngredientSerializer(
            self.cart_ing
        )

    def test_retrieve(self):
        """Test get model by id"""
        url = id_url(URL_RECIPE_CART_ING, self.cart_ing.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_list(self):
        """Test get all models"""
        payload = [
            self.cart_ing,
            create_recipe_cart_ingredient(
                self.cart1,
                self.ingredient2,
            ),
        ]
        payload_data = get_payload_data(
            serializers.RecipeCartIngredientSerializer,
            payload,
            True
        )

        res = self.client.get(URL_RECIPE_CART_ING)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_create(self):
        """Test creating model"""
        payload = {
            "shopping_cart_recipe": self.cart2.id,
            "ingredient": self.ingredient1.id,
            "buy_unit_quantity": 5,
            "is_done": True,
        }
        payload_data = get_payload_data(
            serializers.RecipeCartIngredientSerializer,
            payload
        )

        res = self.client.post(URL_RECIPE_CART_ING, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res_data = res.data
        del res_data["id"]
        self.assertEqual(res.data, payload_data)

    def test_patch(self):
        """Test update model"""
        payload = {
            "buy_unit_quantity": 101,
        }

        url = id_url(URL_RECIPE_CART_ING, self.cart_ing.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data["buy_unit_quantity"],
            payload["buy_unit_quantity"]
        )

    def test_put(self):
        """Test update model"""
        id = self.cart_ing.id
        payload = {**self.serializer.data}
        payload["buy_unit_quantity"] = 102

        url = id_url(URL_RECIPE_CART_ING, id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        model = models.RecipeCartIngredient.objects.get(
            id=id
        )
        self.assertEqual(
            model.buy_unit_quantity,
            payload["buy_unit_quantity"]
        )

    def test_delete(self):
        """Test deleting model, as staff user"""
        url = id_url(URL_RECIPE_CART_ING, self.cart_ing.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            _ = models.RecipeCartIngredient.objects.get(id=self.cart_ing.id)

    def test_fail_delete(self):
        """Test deleting model, no authorization"""
        denied_client = APIClient()
        _ = setup_login(denied_client, username="denied_username")
        url = id_url(URL_RECIPE_CART_ING, self.cart_ing.id)
        res = denied_client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
