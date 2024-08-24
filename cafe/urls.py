from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='cafe-home'),
    path('history/', views.history, name='cafe-history')
]
