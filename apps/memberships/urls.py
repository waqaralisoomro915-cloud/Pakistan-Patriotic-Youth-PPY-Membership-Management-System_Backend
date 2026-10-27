from rest_framework.routers import DefaultRouter
from .views import MembershipViewSet
router = DefaultRouter()
router.register('', MembershipViewSet, basename='memberships')
urlpatterns = router.urls