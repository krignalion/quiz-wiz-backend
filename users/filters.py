import django_filters
from .models import UserProfile

class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = ['created_at']