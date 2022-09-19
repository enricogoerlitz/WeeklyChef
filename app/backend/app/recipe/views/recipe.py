"""
Views for recipe.
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from app_auth.authentication import JWTAuthentication
from recipe import serializers
from core.models import (
    Unit,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    RecipeFavorite,
)
from recipe.permissions.recipe import (
    IsStaff,
    OnDeleteIsStaff,
    IsOwnerOrStaff,
)


class BaseAuthModelViewSet(ModelViewSet):
    """Base model for recipe endpoint authentication"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class UnitViewSet(BaseAuthModelViewSet):
    """Endpoints for unit"""
    serializer_class = serializers.UnitSerializer
    queryset = Unit.objects.all()
    permission_classes = [IsAuthenticated, IsStaff]


class TagViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated, OnDeleteIsStaff]


class IngredientViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.IngredientDetailSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated, OnDeleteIsStaff]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.IngredientSerializer
        return self.serializer_class


class RecipeViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    # def get_serializer_class() -> if action...
    # ... self.get_serializer()


class RecipeFavoriteViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.RecipeFavoriteSerializer
    queryset = RecipeFavorite.objects.all()
    # def get_serializer_class() -> if action...
    # ... self.get_serializer()


class RecipeIngredientViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.RecipeIngredientSerializer
    queryset = RecipeIngredient.objects.all()
    # def get_serializer_class() -> if action...
    # ... self.get_serializer()
