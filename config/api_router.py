from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from powermeter.meters.urls import urlpatterns as meters_url
from powermeter.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
urlpatterns += meters_url
