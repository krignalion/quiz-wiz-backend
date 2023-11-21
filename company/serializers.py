from rest_framework import serializers
from users.models import UserProfile
from users.serializers import UserProfileSerializer, UserRequestSerializer

from .models import Company, CompanyMember, Invitation, UserCompanyRole


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True, read_only=True)
    invitations = serializers.SerializerMethodField()
    user_requests = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "description",
            "is_visible",
            "members",
            "invitations",
            "user_requests",
            "admins",
            "owner",
        ]

    def get_admins(self, obj):
        admins = CompanyMember.objects.filter(
            company=obj.id, role=UserCompanyRole.ADMIN
        )
        return CompanyMemberSerializer(admins, many=True).data

    def get_invitations(self, obj):
        from company.models import Invitation

        invitations = Invitation.objects.filter(sender=obj.owner, company=obj)
        return InvitationSerializer(invitations, many=True).data

    def get_user_requests(self, obj):
        from users.models import UserRequest

        user_requests = UserRequest.objects.filter(user=obj.owner, company=obj)
        return UserRequestSerializer(user_requests, many=True).data


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "description")


class CompanyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMember
        fields = "__all__"

    def get_user(self, obj):
        user = UserProfile.objects.get(id=obj.user.id)
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
