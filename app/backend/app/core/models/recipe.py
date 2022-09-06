from django.db import models

from core.models import User


class Unit(models.Model):
    id = models.BigAutoField(primary_key=True)
    unit_name = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'unit'

    def __str__(self) -> str:
        return f"{self.id} | {self.unit_name}"


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(
        unique=True,
        max_length=25,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'tag'

    def __str__(self) -> str:
        return f"{self.id} | {self.tag_name}"


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    ingredient_name = models.CharField(
        unique=True,
        max_length=50,
        blank=False,
        null=False
    )
    default_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=False,
        null=False
    )
    ingredient_display_name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    quantity_per_unit = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=False,
        null=False
    )
    unit = models.ForeignKey(
        Unit,
        models.SET_NULL,
        null=True
    )
    is_spices = models.BooleanField(default=False)
    search_description = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'ingredient'

    def __str__(self) -> str:
        return f"{self.id} | {self.ingredient_name}"


class Recipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe_name = models.CharField(
        unique=True,
        max_length=75, blank=False,
        null=False
    )
    person_count = models.IntegerField(
        blank=False,
        null=False
    )
    prep_description = models.CharField(
        max_length=1000,
        blank=False,
        null=False
    )
    cooking_duration_min = models.IntegerField(
        blank=False,
        null=False
    )
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'recipe'

    def __str__(self) -> str:
        return f"{self.id} | {self.recipe_name}"


class RecipeFavorite(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        blank=False,
        null=False
    )
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'recipe_favorite'
        unique_together = (('user', 'recipe'),)

    def __str__(self) -> str:
        return f"{self.id}"


class RecipeImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        blank=False,
        null=False
    )
    image_path = models.CharField(
        unique=True,
        max_length=255,
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'recipe_image'

    def __str__(self) -> str:
        return f"{self.id} | {self.recipe} | {self.image_path}"


class RecipeIngredient(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        blank=False,
        null=False
    )
    ingredient = models.ForeignKey(
        Ingredient,
        models.CASCADE,
        blank=False,
        null=False
    )
    unit_quantity = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'recipe_ingredient'
        unique_together = (('recipe', 'ingredient'),)

    def __str__(self) -> str:
        return f"{self.id}"


class RecipeRating(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        blank=False,
        null=False
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'recipe_rating'
        unique_together = (('user', 'recipe'),)

    def __str__(self) -> str:
        return f"{self.id} | {self.recipe} | {self.rating}"


class RecipeTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        blank=True,
        null=True
    )
    tag = models.ForeignKey(
        Tag,
        models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'recipe_tag'
        unique_together = (('recipe', 'tag'),)

    def __str__(self) -> str:
        return f"{self.id}"


class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    watchlist_name = models.CharField(
        unique=True,
        max_length=50,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'watchlist'
        unique_together = (('user', 'watchlist_name'),)

    def __str__(self) -> str:
        return f"{self.id} | {self.user} | {self.watchlist_name}"


class RecipeWatchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    watchlist = models.ForeignKey(
        Watchlist,
        models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'recipe_watchlist'
        unique_together = (('watchlist', 'recipe'),)

    def __str__(self) -> str:
        return f"{self.id}"
