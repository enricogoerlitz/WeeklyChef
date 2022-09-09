from rest_framework.decorators import action
from rest_framework.views import Request, Response, APIView

from djdevted import response as res


class AuthTokenAPIView(APIView):
    """Handle JWT generating and refreshing tokens"""
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        if request.path == "/api/v1/token/refresh/":
            return self.refresh(request, *args, **kwargs)
        return self.token(request, *args, **kwargs)
    
    def token(self, request: Request, *args, **kwargs) -> Response:
        """Handle generating and returning jwt token"""
        return Response({"url": request.path})

    def refresh(self, request: Request, *args, **kwargs) -> Response:
        """Handle generating an new access token when the refresh token is valid"""
        return Response({"url": request.path})
