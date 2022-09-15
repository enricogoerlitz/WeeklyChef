from django.urls import path, include # noqa

from rest_framework.routers import DefaultRouter

from recipe import views # noqa


router = DefaultRouter()
router.register("unit", views.UnitViewSet)

# .../<int:id>/... # decorator: get_id -> if id=None -> Request.user_id

urlpatterns = [
    path("", include(router.urls))
]
