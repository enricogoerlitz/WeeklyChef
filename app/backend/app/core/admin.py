from django.contrib import admin

from core import models


# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.RecipeIngredient)
admin.site.register(models.RecipeImage)
admin.site.register(models.RecipeFavorite)
admin.site.register(models.RecipeRating)
admin.site.register(models.RecipeTag)
admin.site.register(models.Watchlist)
admin.site.register(models.RecipeWatchlist)
admin.site.register(models.FoodShop)
admin.site.register(models.FoodShopArea)
admin.site.register(models.FoodShopAreaPartIngredient)
admin.site.register(models.PreferredUserFoodShop)
admin.site.register(models.DayTime)
admin.site.register(models.RecipeCart)
admin.site.register(models.RecipeCartIngredient)
admin.site.register(models.Tag)
admin.site.register(models.Unit)
