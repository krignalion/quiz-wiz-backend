from django.contrib import admin
from django.urls import include, path
from djoser.views import UserCreateView, TokenCreateView, PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('health_access.urls')),
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls')),
]
