from datetime import datetime, timezone, timedelta

from django.test import TestCase

from app import settings
from app_auth import auth_service
from core.tests.test_model_user import setup_user


def compare_dates(date1: datetime, date2: datetime) -> bool:
    date1 = str(date1)[:10]  # type: ignore
    date2 = str(date2)[:10]  # type: ignore
    return date1 == date2


class TestAuthService(TestCase):
    """Test auth service and jwt token generation/validation"""

    def setUp(self):
        self.user = setup_user()
    
    def test_create_jwt(self):
        """Test creating jwt"""
        data_dict = {"data1": "Teddy", "data2": "Bear"}
        token = auth_service._create_token(
            data_dict,
            auth_service.EXP_DURATION
        )
        token2 = auth_service._create_token(data_dict, exp_duration=None)

        self.assertTrue(isinstance(token, str))
        self.assertTrue(isinstance(token2, str))
        
        decoded_token = auth_service.decode_token(token)
        decoded_token2 = auth_service.decode_token(token2)

        self.assertIn("data1", decoded_token)
        self.assertIn("data1", decoded_token)
        self.assertIn("data2", decoded_token2)
        self.assertIn("data2", decoded_token2)
        self.assertIn("creation_date", decoded_token)
        self.assertIn("creation_date", decoded_token2)
        self.assertIn("exp", decoded_token)
        self.assertNotIn("exp", decoded_token2)
        self.assertIn("iss", decoded_token)
        self.assertIn("iss", decoded_token2)

        current_date = datetime.now(tz=timezone.utc)
        expected_exp_date = (
            current_date + timedelta(**auth_service.EXP_DURATION)
        )
        exp_token_date = datetime.fromtimestamp(decoded_token["exp"])
        
        self.assertTrue(compare_dates(expected_exp_date, exp_token_date))
        
        self.assertEqual(str(current_date)[:10],
                         decoded_token["creation_date"][:10])
        self.assertEqual(str(current_date)[:10],
                         decoded_token2["creation_date"][:10])

        self.assertEqual(decoded_token["iss"], settings.JWT_ISSUER)
        self.assertEqual(decoded_token2["iss"], settings.JWT_ISSUER)

        self.assertEqual(decoded_token["data1"], data_dict["data1"])
        self.assertEqual(decoded_token["data2"], data_dict["data2"])
        self.assertEqual(decoded_token2["data1"], data_dict["data1"])
        self.assertEqual(decoded_token2["data2"], data_dict["data2"])

    def test_decode_token(self):
        """Test decoding an valid jwt"""
        pass

    def test_decode_token_raises(self):
        """Test failing jwt at invalid signature and expiring"""
        pass

    def test_create_access_token(self):
        """Should create an valid access"""
        pass

    def test_create_refresh_token(self):
        """Should create an valid refresh token"""
        pass

    def test_create_access_refresh_token(self):
        """Test creating access as well as refresh token"""
        tokens_response = auth_service.create_access_refresh_token(
            self.user.id
        )

        decoded_token = auth_service.decode_token(
            tokens_response["token"]
        )
        decoded_refresh_token = auth_service.decode_token(
            tokens_response["refresh_token"]
        )

        self.assertIn("token", tokens_response)
        self.assertIn("refresh_token", tokens_response)
        self.assertIn("user_id", decoded_token)
        self.assertIn("user_id", decoded_refresh_token)
        self.assertIn("is_refresh_token", decoded_token)
        self.assertIn("is_refresh_token", decoded_refresh_token)
        self.assertIn("creation_date", decoded_token)
        self.assertIn("creation_date", decoded_refresh_token)
        self.assertIn("exp", decoded_token)
        self.assertNotIn("exp", decoded_refresh_token)
        self.assertIn("iss", decoded_token)
        self.assertIn("iss", decoded_refresh_token)

        current_date = datetime.now(tz=timezone.utc)
        expected_exp_date = (
            current_date + timedelta(**auth_service.EXP_DURATION)
        )
        exp_token_date = datetime.fromtimestamp(decoded_token["exp"])

        self.assertTrue(compare_dates(expected_exp_date, exp_token_date))
        
        self.assertEqual(str(current_date)[:10],
                         decoded_token["creation_date"][:10])
        self.assertEqual(str(current_date)[:10],
                         decoded_refresh_token["creation_date"][:10])

        self.assertEqual(decoded_token["user_id"], self.user.id)
        self.assertEqual(decoded_refresh_token["user_id"], self.user.id)
        
        self.assertEqual(decoded_token["is_refresh_token"], False)
        self.assertEqual(decoded_refresh_token["is_refresh_token"], True)
        
        self.assertEqual(decoded_token["iss"], settings.JWT_ISSUER)
        self.assertEqual(decoded_refresh_token["iss"], settings.JWT_ISSUER)
