# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DayTime(models.Model):
    id = models.BigAutoField(primary_key=True)
    day_time_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'day_time'


class FoodShop(models.Model):
    id = models.BigAutoField(primary_key=True)
    shop_name = models.CharField(unique=True, max_length=-1)
    address = models.CharField(max_length=75)
    zip_code = models.CharField(max_length=10)
    shop_comment = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'food_shop'


class FoodShopArea(models.Model):
    id = models.BigAutoField(unique=True)
    food_shop = models.OneToOneField(FoodShop, models.DO_NOTHING, primary_key=True)
    area_name = models.CharField(max_length=100)
    area_order_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'food_shop_area'
        unique_together = (('food_shop', 'area_order_number'),)


class FoodShopAreaPart(models.Model):
    area = models.OneToOneField(FoodShopArea, models.DO_NOTHING, primary_key=True)
    area_part_order_number = models.IntegerField()
    area_part_name = models.CharField(max_length=100)
    id = models.BigAutoField(unique=True)

    class Meta:
        managed = False
        db_table = 'food_shop_area_part'
        unique_together = (('area', 'area_part_order_number'),)


class FoodShopAreaPartIngredient(models.Model):
    ingredient = models.OneToOneField('Ingredient', models.DO_NOTHING, primary_key=True)
    area_part = models.ForeignKey(FoodShopAreaPart, models.DO_NOTHING, to_field='id')
    ingredient_price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'food_shop_area_part_ingredient'
        unique_together = (('ingredient', 'area_part'),)


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    ingredient_name = models.CharField(unique=True, max_length=50)
    default_price = models.DecimalField(max_digits=7, decimal_places=2)
    search_description = models.CharField(max_length=100, blank=True, null=True)
    ingredient_display_name = models.CharField(max_length=50)
    quantity_per_unit = models.DecimalField(max_digits=7, decimal_places=2)
    unit = models.ForeignKey('Unit', models.DO_NOTHING)
    is_spices = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ingredient'


class PreferredUserFoodShop(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField('User', models.DO_NOTHING)
    food_shop = models.ForeignKey(FoodShop, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preferred_user_food_shop'


class Recipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe_name = models.CharField(unique=True, max_length=75)
    person_count = models.IntegerField()
    prep_description = models.CharField(max_length=1000)
    cooking_duration_min = models.IntegerField()
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe'


class RecipeCart(models.Model):
    user_id = models.BigIntegerField()
    date = models.DateField()
    day_time = models.ForeignKey(DayTime, models.DO_NOTHING, blank=True, null=True)
    recipe_name = models.CharField(max_length=-1)
    food_shop = models.ForeignKey(FoodShop, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'recipe_cart'


class RecipeCartIngredient(models.Model):
    shopping_cart_recipe = models.OneToOneField(RecipeCart, models.DO_NOTHING, primary_key=True)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING)
    buy_unit_quantity = models.IntegerField()
    is_buyed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe_cart_ingredient'
        unique_together = (('shopping_cart_recipe', 'ingredient'),)


class RecipeFavorite(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_favorite'
        unique_together = (('user', 'recipe'),)


class RecipeImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)
    image_path = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'recipe_image'


class RecipeIngredient(models.Model):
    recipe = models.OneToOneField(Recipe, models.DO_NOTHING, primary_key=True)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING)
    unit_quantity = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'recipe_ingredient'
        unique_together = (('recipe', 'ingredient'),)


class RecipeRating(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        managed = False
        db_table = 'recipe_rating'
        unique_together = (('user', 'recipe'),)


class RecipeTag(models.Model):
    recipe = models.OneToOneField(Recipe, models.DO_NOTHING, primary_key=True)
    tag = models.ForeignKey('Tag', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_tag'
        unique_together = (('recipe', 'tag'),)


class RecipeWatchlist(models.Model):
    watchlist = models.OneToOneField('Watchlist', models.DO_NOTHING, primary_key=True)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_watchlist'
        unique_together = (('watchlist', 'recipe'),)


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'tag'


class Unit(models.Model):
    id = models.BigAutoField(primary_key=True)
    unit_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'unit'


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    last_login = models.DateField(blank=True, null=True)
    is_superuser = models.IntegerField()
    is_staff = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('username', 'email'),)


class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    watchlist_name = models.CharField(unique=True, max_length=-1)
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'watchlist'
