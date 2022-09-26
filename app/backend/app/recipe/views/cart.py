"""
Views for cart.
DayTime, RecipeCart, RecipeCartIngredient
"""
from rest_framework.permissions import IsAuthenticated

from core import models
from recipe import serializers
from recipe.permissions import (
    OnDeleteIsStaff,
    IsOwnerOrIsStaff,
    IsCartOwnerOrIsStaff
)
from .general import (
    CRDModelViewSet,
    BaseAuthModelViewSet
)


class DayTimeViewSet(CRDModelViewSet):
    """Endpoints for DayTime"""
    serializer_class = serializers.DayTimeSerializer
    queryset = models.DayTime.objects.all()
    permission_classes = [IsAuthenticated, OnDeleteIsStaff]


class RecipeCartViewSet(BaseAuthModelViewSet):
    """Endpoints for RecipeCart"""
    serializer_class = serializers.RecipeCartSerializer
    queryset = models.RecipeCart.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrIsStaff]


class RecipeCartIngredientViewSet(BaseAuthModelViewSet):
    """Endpoints for RecipeCartIngredient"""
    serializer_class = serializers.RecipeCartIngredientSerializer
    queryset = models.RecipeCartIngredient.objects.all()
    permission_classes = [IsAuthenticated]

    @IsCartOwnerOrIsStaff
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @IsCartOwnerOrIsStaff
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @IsCartOwnerOrIsStaff
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @IsCartOwnerOrIsStaff
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
