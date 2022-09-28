from django.urls import path

from app_auth import views


urlpatterns = [
    path("token/", views.AuthTokenAPIView.as_view()),
    path("token/refresh/", views.AuthTokenAPIView.as_view()),
    path("token/register/", views.AuthTokenAPIView.as_view()),
]
