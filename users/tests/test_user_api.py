import pytest
from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APIClient
from users.models import UserProfile


@pytest.mark.django_db
def test_create_user_authenticated():
    authorized_user = UserProfile.objects.create(
        username="test_user", password="test_user_password"
    )

    permission = Permission.objects.get(codename="add_userprofile")
    authorized_user.user_permissions.add(permission)

    api_client = APIClient()
    api_client.force_authenticate(user=authorized_user)

    url = "/users/"
    user_data = {
        "username": "newuser",
        "password": "newpassword",
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "created_at": "2023-10-10",
    }

    response = api_client.post(url, user_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
