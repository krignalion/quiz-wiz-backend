from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet
from .views import CreateUserView

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/create-user/', CreateUserView.as_view(), name='userprofile-create-user'),
]
