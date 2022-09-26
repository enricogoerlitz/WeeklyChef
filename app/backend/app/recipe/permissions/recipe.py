"""
Permissions for recipe models
"""
from typing import Any, Callable, Union

from django.core.exceptions import ObjectDoesNotExist

from djdevted import response as res
from djdevted.exceptions import FieldRequiredError
from djdevted.request import IRequest

from core import models


def IsRecipeOwnerOrIsStaff(func: Callable) -> Callable:
    """
    Permission decorator
    Checks whether the user is the recipe creator or staff
    """
    def wrapper(view: Any, request: IRequest, *args, **kwargs):
        try:
            recipe = _get_recipe(request, *args, **kwargs)
            if request.user.is_staff:
                return func(view, request, *args, **kwargs)

            if recipe.user.id == request.user.id:
                return func(view, request, *args, **kwargs)

            err_msg = "Only the recipe creator can " + \
                      "modify the recipe ingredients."
            return res.error_403_forbidden(err_msg)
        except (ObjectDoesNotExist, FieldRequiredError) as exp:
            return res.error_400_bad_request(exp)
        except (Exception, NotImplementedError) as exp:
            return res.error_500_internal_server_error(exp)
    return wrapper


def _get_recipe(
    request: IRequest,
    *args,
    **kwargs
) -> models.Recipe:
    """
    Fetch the requested recipe
    Raises FieldRequiredException
    Raises ObjectDoesNotExit
    """
    recipe_id = _get_recipe_id(request, *args, **kwargs)
    if not recipe_id:
        raise FieldRequiredError("The field 'recipe' is required.")
    return models.Recipe.objects.get(id=recipe_id)


def _get_recipe_id(
    request: IRequest,
    *args,
    **kwargs
) -> Union[None, int]:
    """
    Investigates the recipe id
    Raises ObjectDoesNotExit
    Raises NotImplementedError
    """
    if request.method == "POST":
        return int(request.data.get("recipe"))
    if request.method == "GET":
        raise NotImplementedError("GET-Method not implemented.")

    pk: int = kwargs.get("pk")  # type: ignore
    req_path = request.path

    if "recipe-ingredient" in req_path:
        return models.RecipeIngredient.objects.get(
            id=pk
        ).recipe.id
    elif "recipe-tag" in req_path:
        return models.RecipeTag.objects.get(
            id=pk
        ).recipe.id
    elif "recipe-watchlist" in req_path:
        return models.RecipeWatchlist.objects.get(
            id=pk
        ).recipe.id
    return None
