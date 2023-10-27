from django.urls import path
from app_main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboardData', views.dashboardData, name='dashboardData'),
]
