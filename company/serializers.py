from rest_framework import serializers

from .models import Company, Invitation
from users.serializers import UserProfileSerializer


class CompanySerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Company
        fields = ["name", "description", "is_visible", "members"]


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "description")


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"
