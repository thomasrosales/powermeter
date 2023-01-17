from rest_framework.routers import SimpleRouter

from .api.views import MeterViewSet

router = SimpleRouter()

router.register("meters", MeterViewSet, basename="meters")

urlpatterns = router.urls
