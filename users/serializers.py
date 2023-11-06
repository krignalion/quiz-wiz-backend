import importlib

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from company.models import Invitation
from rest_framework import serializers

from .models import UserProfile, UserRequest


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    received_invitations = serializers.SerializerMethodField()
    sent_requests = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "image_path",
            "received_invitations",
            "sent_requests",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserProfile.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_received_invitations(self, obj):
        invitation_module = importlib.import_module("company.serializers")
        InvitationSerializer = invitation_module.InvitationSerializer
        received_invitations = Invitation.objects.filter(receiver=obj)
        return InvitationSerializer(received_invitations, many=True).data

    def get_sent_requests(self, obj):
        sent_requests = UserRequest.objects.filter(user=obj)
        return UserRequestSerializer(sent_requests, many=True).data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email

        return token


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = "__all__"
