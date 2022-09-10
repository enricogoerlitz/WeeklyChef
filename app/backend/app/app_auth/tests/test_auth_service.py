from django.test import TestCase

from app_auth import auth_service # noqa
from core.tests.test_model_user import setup_user


class TestAuthService(TestCase):
    """Test auth service and jwt token generation/validation"""

    def setUp(self):
        self.user = setup_user()
    
    def test_create_jwt(self):
        """Test creating jwt"""
        pass

    def test_decode_token(self):
        """Test decoding an valid jwt"""
        pass

    def test_decode_token_raises(self):
        """Test failing jwt at invalid signature and expiring"""
        pass

    def test_create_access_refresh_token(self):
        """Test creating access as well as refrsh token"""
        pass

    def test_create_access_token(self):
        """Should create an valid access"""
        pass

    def test_create_refresh_token(self):
        """Should create an valid refresh token"""
        pass
    
    def test_register_user(self):
        """
        Test registering user and
        returning access and refresh token
        """
        pass
    
    def test_login_user(self):
        """
        Test the login of an user and
        returning access and refresh token
        """
        pass
