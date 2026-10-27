from rest_framework.routers import DefaultRouter
from .views import PositionsViewSet

router = DefaultRouter()
router.register("positions", PositionsViewSet, basename="positions")
urlpatterns = router.urls
