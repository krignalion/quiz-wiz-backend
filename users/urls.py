from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserListViewSet , UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('users/', UserListViewSet.as_view({'get': 'list'}), name='user-list'),
    path('', include(router.urls)),
]
