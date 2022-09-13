from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import Response, APIView

import jwt  # type: ignore

from djdevted import response as res
from djdevted.request import IRequest

from app_auth import auth_service


class AuthTokenAPIView(APIView):
    """
    Handle JWT generating and refreshing tokens
    Handle register user
    Handle logging user in
    """

    def post(self, request: IRequest, *args, **kwargs) -> Response:
        if request.path == "/api/v1/token/refresh/":
            return self.refresh(request, *args, **kwargs)
        if request.path == "/api/v1/token/register/":
            return self.register(request, *args, **kwargs)
        return self.login(request, *args, **kwargs)
    
    def login(self, request: IRequest, *args, **kwargs) -> Response:
        """Handle user login, generating and returning jwt token"""
        try:
            result = auth_service.login_user(request)
            return res.success(result)
        except ValueError as exp:
            return res.error_400_bad_request(exp)
        except ObjectDoesNotExist:
            return res.error_403_forbidden("Wrong user data given.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)

    def refresh(self, request: IRequest, *args, **kwargs) -> Response:
        """
        Handle generating an new access token
        when the refresh token is valid
        """
        try:
            result = auth_service.refresh_token(request)
            return res.success(result)
        except (ValueError, ObjectDoesNotExist) as exp:
            return res.error_400_bad_request(exp)
        except jwt.InvalidSignatureError:
            return res.error_401_unauthorized("Invalid Token signature.")
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
    
    def register(self, request: IRequest, *args, **kwargs):
        """
        Handle user registration and
        Returns valid access and refresh token
        """
        try:
            result = auth_service.register_user(request)
            return res.created(result)
        except ValueError as exp:
            return res.error_400_bad_request(exp)
        except Exception as exp:
            return res.error_500_internal_server_error(exp)
