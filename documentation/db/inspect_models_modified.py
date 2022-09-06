# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_superuser = models.IntegerField()
    is_staff = models.IntegerField()

    class Meta:
        db_table = 'user'
        unique_together = (('username', 'email'),)
    
    def __str__(self) -> str:
        return f"{self.id} | {self.username} | {self.email}"


class Unit(models.Model):
    id = models.BigAutoField(primary_key=True)
    unit_name = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'unit'
    
    def __str__(self) -> str:
        return f"{self.id} | {self.unit_name}"


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    ingredient_name = models.CharField(unique=True, max_length=50, blank=False, null=False)
    default_price = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    ingredient_display_name = models.CharField(max_length=50, blank=False, null=False)
    quantity_per_unit = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    unit = models.ForeignKey(Unit, models.SET_NULL, null=True)
    is_spices = models.BooleanField(default=False)
    search_description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'ingredient'

    def __str__(self) -> str:
        return f"{self.id} | {self.ingredient_name}"


class DayTime(models.Model):
    id = models.BigAutoField(primary_key=True)
    day_time_name = models.CharField(unique=True, max_length=10, blank=False, null=False)

    class Meta:
        db_table = 'day_time'
    
    def __str__(self) -> str:
        return f"{self.id} | {self.day_time_name}"


class FoodShop(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop_name = models.CharField(unique=True, max_length=100, blank=False, null=False)
    address = models.CharField(max_length=75, blank=False, null=False)
    zip_code = models.CharField(max_length=10, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    shop_comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'food_shop'
    
    def __str__(self) -> str:
        return f"{self.id} | {self.shop_name} | {self.address}"


class FoodShopArea(models.Model):
    id = models.BigAutoField(primary_key=True)
    food_shop = models.ForeignKey(FoodShop, models.CASCADE, blank=False, null=False)
    area_name = models.CharField(max_length=100, blank=False, null=False)
    area_order_number = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'food_shop_area'
        unique_together = (('food_shop', 'area_order_number'),)
    
    def __str__(self) -> str:
        return f"{self.id} | {self.area_name} | {self.area_order_number}"


class FoodShopAreaPart(models.Model):
    id = models.BigAutoField(primary_key=True)
    area = models.ForeignKey(FoodShopArea, models.CASCADE, blank=False, null=False)
    area_part_name = models.CharField(max_length=100, blank=False, null=False)
    area_part_order_number = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'food_shop_area_part'
        unique_together = (('area', 'area_part_order_number'),)
    
    def __str__(self) -> str:
        return f"{self.id} | {self.area_part_name} | {self.area_part_order_number}"


class FoodShopAreaPartIngredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    ingredient = models.ForeignKey(Ingredient, models.CASCADE, blank=False, null=False)
    area_part = models.ForeignKey(FoodShopAreaPart, models.CASCADE, blank=False, null=False)
    ingredient_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'food_shop_area_part_ingredient'
        unique_together = (('ingredient', 'area_part'),)
    
    def __str__(self) -> str:
        return f"{self.id}"


class PreferredUserFoodShop(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, models.CASCADE, blank=False, null=False)
    food_shop = models.ForeignKey(FoodShop, models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'preferred_user_food_shop'
        unique_together = (('user', 'food_shop'),)
    
    def __str__(self) -> str:
        return f"{self.id}"


class Recipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe_name = models.CharField(unique=True, max_length=75, blank=False, null=False)
    person_count = models.IntegerField(blank=False, null=False)
    prep_description = models.CharField(max_length=1000, blank=False, null=False)
    cooking_duration_min = models.IntegerField(blank=False, null=False)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'recipe'
    
    def __str__(self) -> str:
        return f"{self.id} | {self.recipe_name}"


class RecipeCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, blank=False, null=False)
    date = models.DateField(blank=False, null=False)
    day_time = models.ForeignKey(DayTime, models.SET_NULL, blank=True, null=True)
    recipe_name = models.CharField(max_length=75)
    food_shop = models.ForeignKey(FoodShop, models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'recipe_cart'
    
    def __str__(self) -> str:
        return f"{self.id} | {self.user} | {self.recipe_name}"


class RecipeCartIngredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopping_cart_recipe = models.ForeignKey(RecipeCart, models.CASCADE, blank=False, null=False)
    ingredient = models.ForeignKey(Ingredient, models.CASCADE, blank=False, null=False)
    buy_unit_quantity = models.IntegerField(blank=False, null=False)
    is_buyed = models.BooleanField(default=False, blank=True)

    class Meta:
        db_table = 'recipe_cart_ingredient'
        unique_together = (('shopping_cart_recipe', 'ingredient'),)
    
    def __str__(self) -> str:
        return f"{self.id}"


class RecipeFavorite(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, blank=False, null=False)
    recipe = models.ForeignKey(Recipe, models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'recipe_favorite'
        unique_together = (('user', 'recipe'),)
    
    def __str__(self) -> str:
        return f"{self.id}"


class RecipeImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, models.CASCADE, blank=False, null=False)
    image_path = models.CharField(unique=True, max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'recipe_image'
    
    def __str__(self) -> str:
        return f"{self.id} | {self.recipe} | {self.image_path}"


class RecipeIngredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, models.CASCADE, blank=False, null=False)
    ingredient = models.ForeignKey(Ingredient, models.CASCADE, blank=False, null=False)
    unit_quantity = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)

    class Meta:
        db_table = 'recipe_ingredient'
        unique_together = (('recipe', 'ingredient'),)
    
    def __str__(self) -> str:
        return f"{self.id}"


class RecipeRating(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, models.CASCADE, blank=False, null=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=False, null=False)

    class Meta:
        db_table = 'recipe_rating'
        unique_together = (('user', 'recipe'),)
    
    def __str__(self) -> str:
        return f"{self.id} | {self.recipe} | {self.rating}"


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(unique=True, max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'tag'
    
    def __str__(self) -> str:
        return f"{self.id} | {self.tag_name}"


class RecipeTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, models.CASCADE, blank=True, null=True)
    tag = models.ForeignKey(Tag, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'recipe_tag'
        unique_together = (('recipe', 'tag'),)
    
    def __str__(self) -> str:
        return f"{self.id}"


class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    watchlist_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'watchlist'
        unique_together = (('user', 'watchlist_name'),)
    
    def __str__(self) -> str:
        return f"{self.id} | {self.user} | {self.watchlist_name}"


class RecipeWatchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    watchlist = models.ForeignKey(Watchlist, models.CASCADE)
    recipe = models.ForeignKey(Recipe, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'recipe_watchlist'
        unique_together = (('watchlist', 'recipe'),)
    
    def __str__(self) -> str:
        return f"{self.id}"
