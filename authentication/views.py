from authentication.views import UserCreateView, TokenCreateView, PasswordChangeView
from rest_framework import generics
from users.models import UserProfile
from users.serializers import UserProfileSerializer

class UserRegistrationView(UserCreateView):
    # Добавьте свои настройки, если необходимо
    pass

class UserLoginView(TokenCreateView):
    # Добавьте свои настройки, если необходимо
    pass

class UserPasswordChangeView(PasswordChangeView):
    # Добавьте свои настройки, если необходимо
    pass

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
