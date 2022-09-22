"""
Test foodshop models api endpoints
"""
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from djdevted.test import (  # noqa
    check_is_auth_required,
    get_payload_data,
    id_url,
)

from core.tests.test_model_food_shop import (  # noqa
    create_food_shop,
    create_food_shop_area,
    create_food_shop_area_part,
    create_food_shop_area_part_ingredient,
    create_ingredient,
    create_preferred_user_food_shop,
)
from core import models
from recipe import serializers
from recipe.tests.test_views_user import setup_login


URL_FOOD_SHOP = "/api/v1/food-shop/"
URL_FOOD_SHOP_A = "/api/v1/food-shop-area/"
URL_FOOD_SHOP_AP = "/api/v1/food-shop-area-part/"
URL_FOOD_SHOP_API = "/api/v1/food-shop-area-part-ingredient/"
URL_FAV_FOOD_SHOP = "/api/v1/food-shop-favorite/"


class PublicFoodShopAuthRequired(TestCase):
    """Test endpoints require an authorization token"""

    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required_food_shop(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_FOOD_SHOP
            )
        )

    def test_auth_required_food_shop_area(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_FOOD_SHOP_A
            )
        )

    def test_auth_required_food_shop_area_part(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_FOOD_SHOP_AP
            )
        )

    def test_auth_required_food_shop_area_part_ing(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_FOOD_SHOP_API
            )
        )

    def test_auth_required_food_shop_favorite(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(
                self.client,
                URL_FAV_FOOD_SHOP
            )
        )


class PrivateFoodShopApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client, username="food_shop_user")
        self.foodshop = create_food_shop("shopname1")
        self.serializer = serializers.FoodShopSerializer(
            self.foodshop
        )

    def test_retrieve(self):
        """Test get model by id"""
        res = self.client.get(
            id_url(URL_FOOD_SHOP, self.foodshop.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_retrieve_details(self):
        """Test get model by id with details"""
        pass

    def test_list(self):
        """Test get all models"""
        payload = [
            self.foodshop,
            create_food_shop("foodshop2"),
            create_food_shop("foodshop3"),
        ]
        payload_data = get_payload_data(
            serializers.FoodShopSerializer,
            payload,
            True
        )

        res = self.client.get(URL_FOOD_SHOP)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_list_details(self):
        """Test get all models with details"""
        pass

    def test_create(self):
        """Test creating model"""
        payload = {
            "shop_name": "shop_post",
            "address": "address_shop",
            "zip_code": "F73820",
            "city": "Berlin",
            "shop_comment": "shop_comment",
        }
        payload_data = get_payload_data(
            serializers.FoodShopSerializer,
            payload
        )

        res = self.client.post(URL_FOOD_SHOP, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        foodshop = models.FoodShop.objects.get(id=res.data["id"])
        res_data = serializers.FoodShopSerializer(foodshop).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_patch(self):
        """Test update model"""
        foodshop_id = self.foodshop.id
        payload = {
            "shop_name": "NewFoodShopName",
        }

        res = self.client.patch(id_url(URL_FOOD_SHOP, foodshop_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        foodshop = models.FoodShop.objects.get(id=foodshop_id)
        self.assertEqual(
            foodshop.shop_name,
            payload["shop_name"]
        )

    def test_put(self):
        """Test update model"""
        foodshop_id = self.foodshop.id
        payload = {**self.serializer.data}
        payload["shop_name"] = "foodshop_name_edited"
        payload["address"] = "Updated address"
        payload["zip_code"] = "zip_code"
        payload["city"] = "updated city"

        res = self.client.put(id_url(URL_FOOD_SHOP, foodshop_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        foodshop: models.FoodShop = models.FoodShop.objects.get(
            id=foodshop_id
        )
        self.assertEqual(
            foodshop.shop_name,
            payload["shop_name"]
        )
        self.assertEqual(
            foodshop.address,
            payload["address"]
        )
        self.assertEqual(
            foodshop.zip_code,
            payload["zip_code"]
        )
        self.assertEqual(
            foodshop.city,
            payload["city"]
        )

    def test_delete_as_staff(self):
        """Test deleting model, as staff user"""
        staff_client = APIClient()
        _ = setup_login(staff_client, True, "staff_user_delete")

        delete_id_url = id_url(URL_FOOD_SHOP, self.foodshop.id)
        delete_res = staff_client.delete(delete_id_url)
        is_delete_res = staff_client.get(delete_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        payload = {**self.serializer.data}
        del payload["id"]
        payload["shop_name"] = "----"
        payload["address"] = "----"
        payload["zip_code"] = "--"
        payload["city"] = "-"

        res = self.client.post(URL_FOOD_SHOP, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("shop_name", res.data)
        self.assertIn("address", res.data)
        self.assertIn("zip_code", res.data)
        self.assertIn("city", res.data)

    def test_fail_delete(self):
        """Test deleting model, no authorization"""
        denied_client = self.client
        delete_id_url = id_url(URL_FOOD_SHOP, self.foodshop.id)

        delete_res = denied_client.delete(delete_id_url)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateFoodShopAreaApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client, username="food_shop_user")
        self.foodshop = create_food_shop("shopname1")
        self.area = create_food_shop_area(
            self.foodshop,
            "area_name1",
            1
        )
        self.area2 = create_food_shop_area(
            self.foodshop,
            "area_name2",
            2
        )
        self.serializer = serializers.FoodShopAreaSerializer(
            self.area
        )

    def test_retrieve(self):
        """Test get model by id"""
        res = self.client.get(
            id_url(URL_FOOD_SHOP_A, self.area.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_retrieve_details(self):
        """Test get model by id with details"""
        pass

    def test_list(self):
        """Test get all models"""
        payload = [
            self.area,
            self.area2,
            create_food_shop_area(
                self.foodshop,
                "area3",
                3
            ),
            create_food_shop_area(
                self.foodshop,
                "area4",
                4
            ),
        ]
        payload_data = get_payload_data(
            serializers.FoodShopAreaSerializer,
            payload,
            True
        )

        res = self.client.get(URL_FOOD_SHOP_A)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_list_details(self):
        """Test get all models with details"""
        pass

    def test_create(self):
        """Test creating model"""
        payload = {
            "food_shop": self.foodshop.id,
            "area_name": "new_area",
            "area_order_number": 6,
        }
        payload_data = get_payload_data(
            serializers.FoodShopAreaSerializer,
            payload
        )

        res = self.client.post(URL_FOOD_SHOP_A, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        foodshop = models.FoodShopArea.objects.get(id=res.data["id"])
        res_data = serializers.FoodShopAreaSerializer(foodshop).data
        del res_data["id"]

        self.assertEqual(payload_data, res_data)

    def test_patch(self):
        """Test update model"""
        area_id = self.area.id
        payload = {
            "area_name": "NewAreaName",
        }

        res = self.client.patch(id_url(URL_FOOD_SHOP_A, area_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        foodshop = models.FoodShopArea.objects.get(id=area_id)
        self.assertEqual(
            foodshop.area_name,
            payload["area_name"]
        )

    def test_put(self):
        """Test update model"""
        area_id = self.area.id
        payload = {**self.serializer.data}
        payload["area_name"] = "area_name_edited"
        payload["area_order_number"] = 9

        res = self.client.put(id_url(URL_FOOD_SHOP_A, area_id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        area: models.FoodShopArea = models.FoodShopArea.objects.get(
            id=area_id
        )
        self.assertEqual(
            area.area_name,
            payload["area_name"]
        )
        self.assertEqual(
            area.area_order_number,
            payload["area_order_number"]
        )

    def test_delete_as_staff(self):
        """Test deleting model, as staff user"""
        staff_client = APIClient()
        _ = setup_login(staff_client, True, "staff_user_delete")

        delete_id_url = id_url(URL_FOOD_SHOP_A, self.area.id)
        delete_res = staff_client.delete(delete_id_url)
        is_delete_res = staff_client.get(delete_id_url)

        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_delete_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        payload = {**self.serializer.data}
        del payload["id"]
        payload["area_name"] = "--"
        payload["area_order_number"] = 0

        res = self.client.post(URL_FOOD_SHOP_A, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("area_name", res.data)
        self.assertIn("area_order_number", res.data)

    def test_fail_delete(self):
        """Test deleting model, no authorization"""
        denied_client = self.client
        delete_id_url = id_url(URL_FOOD_SHOP_A, self.area.id)

        delete_res = denied_client.delete(delete_id_url)
        self.assertEqual(delete_res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateFoodShopAreaPartApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client, username="food_shop_user")

    def test_retrieve(self):
        """Test get model by id"""
        pass

    def test_retrieve_details(self):
        """Test get model by id with details"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_details(self):
        """Test get all models with details"""
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

    def test_delete_as_staff(self):
        """Test deleting model, as staff user"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_delete(self):
        """Test deleting model, no authorization"""
        pass


class PrivateFoodShopAreaPartIngApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client, username="food_shop_user")

    def test_retrieve(self):
        """Test get model by id"""
        pass

    def test_retrieve_details(self):
        """Test get model by id with details"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_details(self):
        """Test get all models with details"""
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

    def test_delete_as_staff(self):
        """Test deleting model, as staff user"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_delete(self):
        """Test deleting model, no authorization"""
        pass


class PrivateFoodShopUserFavoriteApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_login(self.client, username="food_shop_user")

    def test_retrieve(self):
        """Test get model by id"""
        pass

    def test_retrieve_details(self):
        """Test get model by id with details"""
        pass

    def test_list(self):
        """Test get all models"""
        pass

    def test_list_details(self):
        """Test get all models with details"""
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

    def test_delete_as_staff(self):
        """Test deleting model, as staff user"""
        pass

    def test_fail_create(self):
        """Test failing validation. Not creating the object"""
        pass

    def test_fail_delete(self):
        """Test deleting model, no authorization"""
        pass
