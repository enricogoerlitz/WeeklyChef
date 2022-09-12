from rest_framework import serializers

from core.models import User


class UserPostSerializer(serializers.ModelSerializer):
    """Serializer for user model post requerst"""

    class Meta:
        model = User
        fields = [
            "username",
            "email"
        ]

        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "username": {"min_length": 4}
        }


class UserGetSerializer(UserPostSerializer):
    """Serializer for user model get request"""

    class Meta(UserPostSerializer.Meta):
        fields = [
            "username",
            "email",
            "is_staff"
        ]
