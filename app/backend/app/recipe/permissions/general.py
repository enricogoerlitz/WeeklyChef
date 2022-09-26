"""
Module for general permissions
"""
from typing import Any

from rest_framework.permissions import BasePermission

from djdevted.request import IRequest


def _is_owner_or_staff(request: IRequest, obj: Any) -> bool:
    return obj.user.id == request.user.id or request.user.is_staff


class IsStaff(BasePermission):
    """Check that the request user is staff"""

    def has_permission(self, request: IRequest, view: Any):
        return request.user.is_staff


class OnDeleteIsStaff(BasePermission):
    """Check on delete user is staff"""

    def has_permission(self, request: IRequest, view: Any):
        if request.method == "DELETE":
            return request.user.is_staff
        return True


class IsOwnerOrIsStaff(BasePermission):
    """Check that the request user is the owner of staff"""

    def has_object_permission(self, request: IRequest, view: Any, obj: Any):
        return _is_owner_or_staff(request, obj)
