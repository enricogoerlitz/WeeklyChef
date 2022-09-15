"""
Views for recipe.
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from app_auth.authentication import JWTAuthentication
from recipe import serializers
from core.models import Unit


class UnitViewSet(ModelViewSet):
    """Endpoints for unit"""
    serializer_class = serializers.UnitSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Unit.objects.all()
