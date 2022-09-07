from django.test import TestCase

from core.models import User


def create_user(
    username: str,
    email: str = "teddy@email.com",
    is_staff: bool = False,
    password: str = "testPW198o12u1938u9"
) -> User:
    return User.objects.create_user(username, email, is_staff, password)


class UserModelTests(TestCase):
    """Test models."""

    def test_create_user_successful(self):
        """Test creating a basic user"""
        username = "test_create_user_successful1"
        password = "testPW1872123983"
        user = create_user(username, password=password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_superuser_successful(self):
        """Test creating a superuser"""
        username = "test_create_superuser_successful1"
        password = "testPW1872123983"
        user = User.objects.create_superuser(
            username,
            email=None,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_with_bad_username(self):
        """Test failing creating a basic user"""

        #  without username
        with self.assertRaises(ValueError):
            create_user(username=None)
        
        #  username with whitespaces
        with self.assertRaises(ValueError):
            create_user(username="teddy with whitespaces")

        #  to long username
        with self.assertRaises(Exception):
            create_user(username="very very long username \
                                  with more then 35 chars.")

        #  duplicate username
        with self.assertRaises(Exception):
            dup_username = "teddy_dup"
            _ = create_user(username=dup_username)
            _ = create_user(username=dup_username)
