"""
Permissions for cart models
"""
from typing import Callable, Any, Union

from django.core.exceptions import ObjectDoesNotExist

from djdevted.request import IRequest
from djdevted import response as res
from djdevted.exceptions import FieldRequiredError

from core import models


def IsCartOwnerOrIsStaff(func: Callable) -> Callable:
    """
    Permission decorator
    Checks whether the user is the cart owner or staff
    """
    def wrapper(view: Any, request: IRequest, *args, **kwargs):
        try:
            shopping_cart = _get_shopping_cart(request, *args, **kwargs)
            if request.user.is_staff:
                return func(view, request, *args, **kwargs)

            if shopping_cart.user.id == request.user.id:
                return func(view, request, *args, **kwargs)

            err_msg = "Only the cart owner can " + \
                      "modify the cart ingredients."
            return res.error_403_forbidden(err_msg)
        except (ObjectDoesNotExist, FieldRequiredError, ValueError) as exp:
            return res.error_400_bad_request(exp)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    return wrapper


def _get_shopping_cart(
    request: IRequest,
    *args,
    **kwargs
) -> models.RecipeCart:
    """
    Fetch the requested recipe
    Raises FieldRequiredException
    Raises ObjectDoesNotExit
    """
    cart_id = _get_shopping_cart_id(request, *args, **kwargs)
    if not cart_id:
        err_msg = "The field 'shopping_cart_recipe' is required."
        raise FieldRequiredError(err_msg)
    return models.RecipeCart.objects.get(id=cart_id)


def _get_shopping_cart_id(
    request: IRequest,
    *args,
    **kwargs
) -> Union[None, int]:
    """
    Investigates the cart id
    Raises ObjectDoesNotExit
    Raises NotImplementedError
    Raises ValueError
    """
    if request.method == "POST":
        return int(request.data.get("shopping_cart_recipe"))
    if request.method == "GET":
        raise NotImplementedError("GET-Method not implemented.")

    pk: int = kwargs.get("pk")  # type: ignore
    req_path = request.path

    if "recipe-cart-ingredient" in req_path:
        return models.RecipeCartIngredient.objects.get(
            id=pk
        ).shopping_cart_recipe.id
    return None
