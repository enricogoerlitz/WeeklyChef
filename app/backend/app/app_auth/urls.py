from django.urls import path, include

from rest_framework.routers import DefaultRouter

from app_auth import views


router = DefaultRouter()
#router.register("token", views.AuthTokenViewSet, basename="token")

urlpatterns = [
    path("token/", views.AuthTokenAPIView.as_view()),
    path("token/refresh/", views.AuthTokenAPIView.as_view()),
    path("", include(router.urls))
]