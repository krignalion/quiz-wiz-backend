from django.contrib import admin
from django.urls import include, path
from djoser.views import UserCreateView, TokenCreateView, PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('health_access.urls')),
    path('users/', include('users.urls')),
    path('auth/user/create/', UserCreateView.as_view(), name='user-create'),
    path('auth/token/create/', TokenCreateView.as_view(), name='token-create'),
    path('auth/password/reset/', PasswordResetView.as_view(), name='password-reset'),
]
