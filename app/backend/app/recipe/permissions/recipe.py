"""
Permissions for recipe models
"""
from typing import Any, Callable, Union

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import BasePermission

from core import models
from djdevted import response as res
from djdevted.exceptions import FieldRequiredException
from djdevted.request import IRequest


def is_owner_or_staff(request: IRequest, obj: Any) -> bool:
    return obj.user.id == request.user.id or request.user.is_staff


class IsOwnerOrStaff(BasePermission):
    """Check that the request user is the owner of staff"""

    def has_object_permission(self, request: IRequest, view: Any, obj: Any):
        return is_owner_or_staff(request, obj)


class OnDeleteIsStaff(BasePermission):
    """Check if delete is staff user"""

    def has_object_permission(self, request: IRequest, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff
        return True


def is_recipe_owner_or_staff(func: Callable) -> Callable:
    """Checks whether the user is the recipe creator"""
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
        except (ObjectDoesNotExist, FieldRequiredException) as exp:
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
        raise FieldRequiredException("The field 'recipe' is required.")
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
        return request.data.get("recipe")
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
