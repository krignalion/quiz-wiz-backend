from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserListViewSet

router = DefaultRouter()
router.register(r'', UserListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
