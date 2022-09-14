"""
Cart model serializers
"""
from rest_framework.serializers import ModelSerializer

from core import models
from core.serializers import UserGetSerializer


class DayTimeSerializer(ModelSerializer):
    """Serialize day time serializer"""

    class Meta:
        model = models.DayTime
        fields = ["id", "day_time_name"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "day_time_name": {"min_length": 4}
        }

