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
router.register("recipe-rating", views.RecipeRatingViewSet)
router.register("recipe-tag", views.RecipeTagViewSet)
router.register("watchlist", views.WatchlistViewSet)
router.register("recipe-watchlist", views.RecipeWatchlistViewSet)
router.register("food-shop", views.FoodShopViewSet)
router.register("food-shop-area", views.FoodShopAreaViewSet)
router.register("food-shop-area-part", views.FoodShopAreaPartViewSet)
router.register("food-shop-area-part-ingredient", views.FoodShopAreaPartIngViewSet)  # noqa
router.register("food-shop-favorite", views.FoodShopUserFavorite)
router.register("day-time", views.DayTimeViewSet)
router.register("recipe-cart", views.RecipeCartViewSet)
router.register("recipe-cart-ingredient", views.RecipeCartIngredientViewSet)

# .../<int:id>/... # decorator: get_id -> if id=None -> Request.user_id

urlpatterns = [
    path("", include(router.urls))
]
