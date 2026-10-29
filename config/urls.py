
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/accounts/", include('apps.accounts.urls')),
    path("api/organizations/", include('apps.organizations.urls')),
    path('', include('apps.cards.urls')),
    path('', include('apps.common.urls')),
    path('api/memberships/', include('apps.memberships.urls')),
    path('api/positions/', include('apps.positions.urls')),
    path('api/promotions/', include('apps.promotions.urls')),
    path('api/verification/', include('apps.verification.urls')),
    path('api/audit/', include('apps.audit.urls')),
]
