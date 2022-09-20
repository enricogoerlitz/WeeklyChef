"""
Permissions for recipe models
"""
from typing import Any, Callable, Union

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import BasePermission

from core import models
from djdevted import response as res
from djdevted.request import IRequest


def is_owner_or_staff(request: IRequest, obj: Any) -> bool:
    return obj.user.id == request.user.id or request.user.is_staff


class IsStaff(BasePermission):
    """Check that the request user is staff"""

    def has_permission(self, request: IRequest, view: Any):
        return request.user.is_staff


class IsOwnerOrStaff(BasePermission):
    """Check that the request user is the owner of staff"""

    def has_object_permission(self, request: IRequest, view: Any, obj: Any):
        return is_owner_or_staff(request, obj)


class OnUpdateOrDeleteIsStaff(BasePermission):
    """
    Check that the request user is staff
    On PUT, PATCH, DELETE
    """
    pass


class OnUpdateOrDeleteIsOwnerOrStaff(BasePermission):
    """
    Check that the request user is the owner of staff
    On PUT, PATCH, DELETE
    """
    pass


class OnDeleteIsStaff(BasePermission):
    """Check if delete is staff user"""

    def has_object_permission(self, request: IRequest, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff
        return True


# class OnCreateOrUpdateIsRecipeOwnerOrStaff(BasePermission):
#     """Check if the user is recipe owner or staff"""

#     def has_permission(self, request: IRequest, view):
#         if request.method == "GET": return True
#         recipe_id: int = request.data["recipe"]
        

def is_recipe_owner_or_staff(func: Callable) -> Callable:
    """Checks whether the user is the recipe creator"""
    def wrapper(view: Any, request: IRequest, *args, **kwargs):
        if request.method == "DELETE":
            recipe_id = kwargs.get("pk")
            print(recipe_id)
        else:
            recipe_id = request.data.get("recipe")
            
        if not recipe_id:
            err_msg = "The field 'recipe' is required."
            return res.error_400_bad_request(err_msg)

        if request.user.is_staff:
            return func(view, request, *args, **kwargs)

        try:
            recipe: models.Recipe = models.Recipe.objects.get(id=recipe_id)
            if recipe.user.id == request.user.id:
                return func(view, request, *args, **kwargs)
            
            err_msg = """Only the recipe creator can
                         modify the recipe ingredients."""
            return res.error_400_bad_request(err_msg)
        except ObjectDoesNotExist as exp:
            return res.error_400_bad_request(exp)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    return wrapper


# get recipe here!!!
def _get_recipe_id():
    pass
def _get_recipe(
    request: IRequest,
    *args,
    **kwargs
) -> Union[None, int]:
    if request.method == "POST":
        return request.data.get("recipe")

    req_path = request.path
    if "" in req_path:
        pass
    elif "" in req_path:
        pass
    return None


def _get_recipe_id_recipe_ingredient_path(
    request: IRequest,
    *args,
    **kwargs
) -> Union[None, int]:
    pass