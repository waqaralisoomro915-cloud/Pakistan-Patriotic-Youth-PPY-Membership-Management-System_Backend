from django.urls import path
from . import views
urlpatterns = [
    path('organizations/', views.organizations, name='organizations'),
]