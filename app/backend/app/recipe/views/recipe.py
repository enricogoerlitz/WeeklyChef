"""
Views for recipe.
"""
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated

from djdevted.request import IRequest
from djdevted import response as res
from recipe import serializers
from core import models
from recipe.permissions import (
    IsStaff,
    OnDeleteIsStaff,
    IsOwnerOrIsStaff,
    IsRecipeOwnerOrIsStaff,
)
from .general import (
    CRDModelViewSet,
    BaseAuthModelViewSet
)


class UnitViewSet(BaseAuthModelViewSet):
    """Endpoints for unit"""
    serializer_class = serializers.UnitSerializer
    queryset = models.Unit.objects.all()
    permission_classes = [IsAuthenticated, IsStaff]


class TagViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    permission_classes = [IsAuthenticated, OnDeleteIsStaff]


class IngredientViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.IngredientDetailSerializer
    queryset = models.Ingredient.objects.all()
    permission_classes = [IsAuthenticated, OnDeleteIsStaff]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.IngredientSerializer
        return self.serializer_class


class RecipeViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.RecipeSerializer
    queryset = models.Recipe.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrIsStaff]


class RecipeFavoriteViewSet(CRDModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.RecipeFavoriteSerializer
    queryset = models.RecipeFavorite.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrIsStaff]

    def list(self, request: IRequest):
        qs = self.queryset.filter(user=request.user.id)
        serializer: ModelSerializer = self.get_serializer(
            many=True,
            data=qs
        )
        _ = serializer.is_valid()
        return res.success(serializer.data)


class RecipeIngredientViewSet(BaseAuthModelViewSet):
    """Endpoints for tag"""
    serializer_class = serializers.RecipeIngredientSerializer
    queryset = models.RecipeIngredient.objects.all()
    permission_classes = [IsAuthenticated]

    @IsRecipeOwnerOrIsStaff
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @IsRecipeOwnerOrIsStaff
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @IsRecipeOwnerOrIsStaff
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @IsRecipeOwnerOrIsStaff
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class RecipeRatingViewSet(BaseAuthModelViewSet):
    """Endpoints for recipe rating"""
    serializer_class = serializers.RecipeRatingSerializer
    queryset = models.RecipeRating.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrIsStaff]


class RecipeTagViewSet(CRDModelViewSet):
    """Endpoints for recipe tag"""
    serializer_class = serializers.RecipeTagSerializer
    queryset = models.RecipeTag.objects.all()
    permission_classes = [IsAuthenticated]

    @IsRecipeOwnerOrIsStaff
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @IsRecipeOwnerOrIsStaff
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class WatchlistViewSet(BaseAuthModelViewSet):
    """Endpoints for watchlist"""
    serializer_class = serializers.WatchlistSerializer
    queryset = models.Watchlist.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrIsStaff]


class RecipeWatchlistViewSet(CRDModelViewSet):
    """Endpoints for recipe watchlist"""
    serializer_class = serializers.RecipeWatchlistSerializer
    queryset = models.RecipeWatchlist.objects.all()
    permission_classes = [IsAuthenticated]

    @IsRecipeOwnerOrIsStaff
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @IsRecipeOwnerOrIsStaff
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
