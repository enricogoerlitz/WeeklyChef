"""
Module for general ModelViewsets
"""
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app_auth.authentication import JWTAuthentication


class BaseAuthModelViewSet(viewsets.ModelViewSet):
    """Base model for recipe endpoint authentication"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CRDModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
