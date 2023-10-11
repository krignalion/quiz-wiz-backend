from django.urls import path
from . import views
# from .views import HealthCheckView

urlpatterns = [
    path('', views.health_check, name='health_check'),
]
