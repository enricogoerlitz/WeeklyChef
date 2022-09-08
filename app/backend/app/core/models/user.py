from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(
        self,
        username: str,
        email: str = None,
        is_staff: bool = False,
        password: str = None
    ) -> AbstractBaseUser:
        """Create, save and return a new user."""
        if not username:
            raise ValueError("User must have an username.")

        if " " in username:
            raise ValueError("Whitespaces are not allowed in a username.")
        
        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, is_staff=is_staff)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str
    ) -> AbstractBaseUser:
        """Create and return a new superuser."""
        user = self.create_user(username, email, True, password)
        #  user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """Application user"""
    
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(
        max_length=35,
        unique=True
    )
    email = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        db_table = "user"

    def __str__(self) -> str:
        return f"{self.id} | {self.username}"
