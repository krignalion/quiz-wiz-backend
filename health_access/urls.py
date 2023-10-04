from django.urls import path
from . import views
from .views import HealthCheckView

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('health-check-view/', HealthCheckView.as_view(), name='health-check'),
]
