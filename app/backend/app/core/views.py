"""
Core views for app.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_auth import auth_service


import time

@api_view(['GET'])
def health_check(request):
    """Returns successful response."""
    response_tokens = auth_service._get_access_refresh_token({"username": "CoolerTeddy", "nickname": "Teddy"})
    token_data = auth_service._decode_token(response_tokens["token"])

    return Response({'healthy': True, "decoded": token_data} | response_tokens)
