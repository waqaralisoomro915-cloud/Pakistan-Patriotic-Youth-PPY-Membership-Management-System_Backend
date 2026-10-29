from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from .views import AuditViewSet
router.register('', AuditViewSet,basename='audit')
urlpatterns = router.urls