import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import UserProfile
from django.contrib.auth.models import Permission

@pytest.mark.django_db
def test_create_user_authenticated():
    authorized_user = UserProfile.objects.create_user(
        username='test_user',
        password='test_user_password'
    )

    permission = Permission.objects.get(codename='add_userprofile')
    authorized_user.user_permissions.add(permission)

    api_client = APIClient()
    api_client.force_authenticate(user=authorized_user)

    url = reverse('userprofile-create-user')
    user_data = {
        'username': 'newuser',
        'password': 'newpassword',
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',
        'created_at': '2023-10-10',
    }

    response = api_client.post(url, json.dumps(user_data), content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED
