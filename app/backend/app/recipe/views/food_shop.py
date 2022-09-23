"""
Views for food-shop.
"""
from rest_framework.permissions import IsAuthenticated

from core import models
from recipe import serializers
from recipe.permissions import (
    OnDeleteIsStaff,
    IsOwnerOrStaff,
)
from .general import BaseAuthModelViewSet


class BaseOnDeleteIsStaffViewSet(BaseAuthModelViewSet):
    """Base class for on delete only staff user"""
    permission_classes = [IsAuthenticated, OnDeleteIsStaff]


class FoodShopViewSet(BaseOnDeleteIsStaffViewSet):
    """Endpoints for FoodShop"""
    serializer_class = serializers.FoodShopSerializer
    queryset = models.FoodShop.objects.all()


class FoodShopAreaViewSet(BaseOnDeleteIsStaffViewSet):
    """Endpoints for FoodShopArea"""
    serializer_class = serializers.FoodShopAreaSerializer
    queryset = models.FoodShopArea.objects.all()


class FoodShopAreaPartViewSet(BaseOnDeleteIsStaffViewSet):
    """Endpoints for FoodShopAreaPart"""
    serializer_class = serializers.FoodShopAreaPartSerializer
    queryset = models.FoodShopAreaPart.objects.all()
    # -> endpoint for new Order!


class FoodShopAreaPartIngViewSet(BaseOnDeleteIsStaffViewSet):
    """Endpoints for FoodShopAreaPartIngredient"""
    serializer_class = serializers.FoodShopAreaPartIngredientSerializer
    queryset = models.FoodShopAreaPartIngredient.objects.all()


class FoodShopUserFavorite(BaseAuthModelViewSet):
    """Endpoints for FoodShopFavorite"""
    serializer_class = serializers.PreferredUserFoodShopSerializer
    queryset = models.PreferredUserFoodShop.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
