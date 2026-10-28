from rest_framework.routers import DefaultRouter
from .views import PromotionViewSet
router = DefaultRouter()
router.register('', PromotionViewSet, basename='promotions')
urlpatterns = router.urls