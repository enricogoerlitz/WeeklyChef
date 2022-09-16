from django.urls import path, include # noqa

from rest_framework.routers import DefaultRouter

from recipe import views # noqa


router = DefaultRouter()
router.register("unit", views.UnitViewSet)
router.register("tag", views.TagViewSet)
router.register("ingredient", views.IngredientViewSet)
router.register("recipe", views.RecipeViewSet)
router.register("recipe-favorite", views.RecipeFavoriteViewSet)
router.register("recipe-ingredient", views.RecipeIngredientViewSet)

# .../<int:id>/... # decorator: get_id -> if id=None -> Request.user_id

urlpatterns = [
    path("", include(router.urls))
]
