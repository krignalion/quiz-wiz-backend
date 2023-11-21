import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from company.models import Company
from rest_framework.test import APIClient
from users.models import UserProfile


@pytest.fixture
def create_authenticated_users():
    owner_client = APIClient()
    user_client = APIClient()
    owner = UserProfile.objects.create_user(
        username="owner_user",
        email="owner@example.com",
        password="password",
        first_name="First Name Owner",
        last_name="Last Name Owner",
    )

    user = UserProfile.objects.create_user(
        username="test_user",
        email="user@example.com",
        password="password",
        first_name="First Name User",
        last_name="Last Name User",
    )

    company = Company.objects.create(name="Test Company", owner=owner)

    owner_token = str(RefreshToken.for_user(owner).access_token)
    user_token = str(RefreshToken.for_user(user).access_token)

    owner_client.credentials(HTTP_AUTHORIZATION=f"JWT {owner_token}")
    user_client.credentials(HTTP_AUTHORIZATION=f"JWT {user_token}")

    return owner, company, user, owner_client, user_client
