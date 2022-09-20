"""
Views for recipe.
"""
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from app_auth.authentication import JWTAuthentication
from djdevted.request import IRequest
from djdevted import response as res
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
    is_recipe_owner_or_staff,
)


class BaseAuthModelViewSet(viewsets.ModelViewSet):
    """Base model for recipe endpoint authentication"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CRDModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
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


class RecipeFavoriteViewSet(CRDModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.RecipeFavoriteSerializer
    queryset = RecipeFavorite.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    # def get_serializer_class() -> if action...
    # ... self.get_serializer()

    def list(self, request: IRequest):
        qs = self.queryset.filter(user=request.user.id)
        serializer: ModelSerializer = self.get_serializer(
            many=True,
            data=qs
        )
        _ = serializer.is_valid()
        return res.success(serializer.data)
        

class RecipeIngredientViewSet(CRDModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.RecipeIngredientSerializer
    queryset = RecipeIngredient.objects.all()
    permission_classes = [IsAuthenticated]
    # def get_serializer_class() -> if action...
    # ... self.get_serializer()

    @is_recipe_owner_or_staff
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @is_recipe_owner_or_staff
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)