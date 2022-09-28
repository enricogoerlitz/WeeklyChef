"""
Example Codes
"""


# Example API TestCase

# ----- PREP ----- #

from django.db import models
from rest_framework import serializers

class ExampleModel(models.Model): pass
class ExampleSerializer(serializers.ModelSerializer): pass
def create_example_obj(t_payload) -> models.Model: pass
def setup_login(t_payload) -> models.Model: pass

# ----- PREP ----- #

from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from djdevted.test import (
    check_is_auth_required,
    get_payload_data,
    id_url,
    detail_url,
)


URL_EXAMPLE = "/api/v1/test/"
URL_EXAMPLE_2 = "/api/v1/test2/"


class PublicExampleAuthRequired(TestCase):
    """Test endpoints require an authorization token"""

    def setUp(self):
        self.client = APIClient()  # no auth user

    def test_auth_required_test_1(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(self.client, URL_EXAMPLE)
        )

    def test_auth_required_test_2(self):
        """Test auth required for model endpoint"""
        self.assertTrue(
            check_is_auth_required(self.client, URL_EXAMPLE_2)
        )

class PrivateExampleApiTests(TestCase):
    """Test model CRUD api endpoint"""

    def setUp(self):
        self.url = URL_EXAMPLE
        self.model = ExampleModel
        self.serializer_class = ExampleSerializer
        self.create_method = create_example_obj

        self.client = APIClient()
        self.denied_client = APIClient()
        self.user = setup_login(self.client)
        self.denied_user = setup_login(self.denied_client)
        self.example_obj = self.create_method("exampleObj")
        self.serializer = self.serializer_class(
            self.example_obj
        )

    def test_retrieve(self):
        """Test get model by id"""
        access_client = self.client
        url = id_url(self.url, self.example_obj.id)
        res = access_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.serializer.data)

    def test_list(self):
        """Test get all models"""
        access_client = self.client
        payload = [
            self.example_obj,
            self.create_method("payload1"),
            self.create_method("payload2"),
        ]
        payload_data = get_payload_data(
            self.serializer_class,
            payload,
            True,
        )

        url = self.url
        res = access_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, payload_data)

    def test_create(self):
        """Test creating model"""
        access_client = self.client
        payload = {
            "payload": "data"
        }
        payload_data = get_payload_data(
            self.serializer_class,
            payload
        )

        url = self.url
        res = access_client.post(url, payload)
        res_data = res.data
        del res_data["id"]

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_data, payload_data)

    def test_patch(self):
        """Test update model"""
        access_client = self.client
        obj = self.create_method("patch_base_unit")
        payload = {
            "patch": "data"
        }
        payload_data = get_payload_data(
            self.serializer_class,
            payload
        )

        url = id_url(self.url, obj.id)
        res = access_client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patched_obj = self.model.objects.get(id=obj.id)
        res_data = self.serializer_class(patched_obj).data
        del res_data["id"]

        self.assertEqual(res_data, payload_data)

    def test_put(self):
        """Test update model"""
        access_client = self.client
        obj_id = self.example_obj.id
        payload = {**self.serializer.data}
        payload["key1"] = "data1"
        payload["key2"] = "data2"

        url = id_url(self.url, obj_id)
        res = access_client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        put_obj = self.model.objects.get(id=obj_id)
        res_data = self.serializer_class(put_obj).data
        del res_data["id"]

        self.assertEqual(res_data, payload)

    def test_delete(self):
        """Test deleting model"""
        access_client = self.client
        obj_id = self.example_obj.id

        url = id_url(self.url, obj_id)
        res = access_client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            _ = self.model.objects.get(id=obj_id)

    def test_fail_retrieve_not_existing(self):
        """Test fail retrieve not existing object"""
        pass

    def test_fail_retrieve_no_auth(self):
        """Test fail retrieve object without auth"""
        pass
    
    def test_fail_create_validation(self):
        """Test fail creating object by validation"""
        pass
    
    def test_fail_create_no_auth(self):
        """Test fail creating object without auth"""
        pass
    
    def test_fail_patch_validation(self):
        """Test fail creating object by validation"""
        pass
    
    def test_fail_patch_no_auth(self):
        """Test fail creating object without auth"""
        pass
    
    def test_fail_put_validation(self):
        """Test fail creating object by validation"""
        pass
    
    def test_fail_put_no_auth(self):
        """Test fail creating object without auth"""
        pass
    
    def test_fail_delete_no_auth(self):
        """Test fail deleting object without auth"""
        pass


class ExampleModelTests(TestCase):
    """Test ExampleModel"""

    def test_create(self):
        """Tests creating model"""
        pass