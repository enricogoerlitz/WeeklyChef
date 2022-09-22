"""
Module for general permissions
"""
from typing import Any

from rest_framework.permissions import BasePermission

from djdevted.request import IRequest


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
