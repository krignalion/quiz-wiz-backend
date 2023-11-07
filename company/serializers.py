from rest_framework import serializers
from users.serializers import UserProfileSerializer, UserRequestSerializer

from .models import Company, Invitation


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True, read_only=True)
    sent_invitations = serializers.SerializerMethodField()
    user_requests = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "name",
            "description",
            "is_visible",
            "members",
            "sent_invitations",
            "user_requests",
        ]

    def get_sent_invitations(self, obj):
        from company.models import Invitation

        sent_invitations = Invitation.objects.filter(sender=obj.owner, company=obj)
        return InvitationSerializer(sent_invitations, many=True).data

    def get_user_requests(self, obj):
        from company.models import UserRequest

        user_requests = UserRequest.objects.filter(user=obj.owner, company=obj)
        return UserRequestSerializer(user_requests, many=True).data


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "description")
