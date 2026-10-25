from django.urls import path
from . import views
urlpatterns = [
    path('positions/', views.positions, name='positions'),

]