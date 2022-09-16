"""
Permissions for recipe models
"""
from typing import Any

from rest_framework.permissions import BasePermission

from djdevted.request import IRequest


def is_owner_or_staff(request: IRequest, obj: Any) -> bool:
    return obj.user == request.user.id or request.user.is_staff


class IsStaff(BasePermission):
    """Check that the request user is staff"""

    def has_permission(self, request: IRequest, view: Any):
        return request.user.is_staff


class IsOwnerOrStaff(BasePermission):
    """Check that the request user is the owner of staff"""

    def has_object_permission(self, request: IRequest, view: Any, obj: Any):
        # user: JWTAuthUser = request.user
        # obj.user == user.id or user.is_staff
        # TODO: test only obj.user/obj.user.id
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
