from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.test_model_user import setup_user, create_user # noqa
from core import models
from app_auth import auth_service


URL_TOKEN = "/api/v1/token"
URL_REGISTER = f"{URL_TOKEN}/register/"
URL_LOGIN = f"{URL_TOKEN}/login/"
URL_REFRESH = f"{URL_TOKEN}/refresh/"


class PublicAuthTokenApiTests(TestCase):
    """Test auth token api-endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user: models.User = setup_user()

    def test_register_user(self):
        """Test registration of an user"""
        user_data = {
            "username": "CoolerTeddy",
            "password": "mySecretPw",
            "email": "teddy@email.com"
        }

        res = self.client.post(URL_REGISTER, user_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", res.data)
        self.assertIn("refresh_token", res.data)

    def test_register_no_staff_user(self):
        """Test registration of an staff user not working"""
        user_data = {
            "username": "CoolerTeddy",
            "password": "mySecretPw",
            "email": "teddy@email.com",
            "is_staff": True
        }

        res = self.client.post(URL_REGISTER, user_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", res.data)
        self.assertIn("refresh_token", res.data)

        user_id = auth_service.decode_token(res.data["token"])["user_id"]
        user: models.User = models.User.objects.get(id=user_id)

        self.assertFalse(user.is_staff)

    def test_register_user_wrong_data(self):
        """Test wrong user data passed"""
        user_data1 = {
            "username": "---",
            "password": "OkayPassword"
        }

        user_data2 = {
            "username": "OkayUsername",
            "password": "---"
        }

        user_data3 = {
            "username": "OkayUsername",
        }

        user_data4 = {
            "password": "OkayPassword",
        }

        res1 = self.client.post(URL_REGISTER, user_data1)
        res2 = self.client.post(URL_REGISTER, user_data2)
        res3 = self.client.post(URL_REGISTER, user_data3)
        res4 = self.client.post(URL_REGISTER, user_data4)

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """Test logging in user"""
        username = "teddy_test"
        password = "secretPW"
        user = create_user(username=username, password=password)
        res = self.client.post(
            f"{URL_TOKEN}/",
            {"username": username, "password": password}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)
        self.assertIn("refresh_token", res.data)

        decoded_token = auth_service.decode_token(res.data["token"])
        decoded_refresh_token = auth_service.decode_token(
            res.data["refresh_token"]
        )

        self.assertEqual(user.id, decoded_token["user_id"])
        self.assertEqual(user.id, decoded_refresh_token["user_id"])

    def test_login_user_missing_data(self):
        """Test logging in user"""
        res1 = self.client.post(
            f"{URL_TOKEN}/",
            {"username": "usernameNoPW"}
        )
        res2 = self.client.post(
            f"{URL_TOKEN}/",
            {"password": "passwordNoUName"}
        )

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_wrong_password(self):
        """Test logging in user"""
        username = "teddy_test"
        password = "secretPW"
        wrong_password = "secretpw"
        _ = create_user(username=username, password=password)
        res = self.client.post(
            f"{URL_TOKEN}/",
            {"username": username, "password": wrong_password}
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_not_existing_user(self):
        """Test logging in user"""
        username = "notExisting"
        password = "secretPW"
        res = self.client.post(
            f"{URL_TOKEN}/",
            {"username": username, "password": password}
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_refresh_an_token(self):
        """Test refreshing the token"""
        user = self.user
        refresh_token = auth_service._create_refresh_token(
            {"user_id": user.id}
        )

        res = self.client.post(URL_REFRESH, {"refresh_token": refresh_token})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)
        self.assertIn("refresh_token", res.data)

        decoded_token = auth_service.decode_token(res.data["token"])
        decoded_refresh_token = auth_service.decode_token(
            res.data["refresh_token"]
        )

        self.assertEqual(user.id, decoded_token["user_id"])
        self.assertEqual(user.id, decoded_refresh_token["user_id"])

    def test_refresh_token_without_token(self):
        """Test refreshing an token without an any token passed"""
        res = self.client.post(URL_REFRESH, {})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token_not_refresh_token_passed(self):
        """Test passing an access token, no refresh token"""
        access_token = auth_service._create_access_token({"user_id": 1})

        res = self.client.post(URL_REFRESH, {"refresh_token": access_token})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token_invalid_token(self):
        """Test passing invalid and expired token"""
        refresh_token = auth_service._create_refresh_token({"user_id": 1})

        res = self.client.post(URL_REFRESH, {"refresh_token": refresh_token})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
