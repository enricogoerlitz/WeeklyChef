"""
Core views for app.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from djdevted.request import IRequest


@api_view(['GET'])
def health_check(request: IRequest):
    """Returns successful response."""
    return Response({
        "healthy": True,
        "endpoint": request.path
    })
