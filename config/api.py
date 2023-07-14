from django.urls import include, path
from rest_framework.routers import DefaultRouter

from powermeter.meters.api.views import InstrumentViewSet
from powermeter.users.api.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("instrument", InstrumentViewSet, basename="instrument")

urlpatterns = [
    path("", include(router.urls)),
]
