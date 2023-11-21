import pytest
from django.urls import reverse

from company.models import CompanyMember, UserCompanyRole
from rest_framework import status


@pytest.mark.django_db
def test_appoint_role_admin(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users
    company.members.add(user)

    response = owner_client.post(
        reverse("company-member-appoint-role", args=[company.id]),
        data={"user_id": user.id, "status_role": UserCompanyRole.ADMIN},
    )

    assert response.status_code == status.HTTP_200_OK

    user_role = CompanyMember.objects.get(user=user, company=company)
    assert user_role.role == UserCompanyRole.ADMIN


@pytest.mark.django_db
def test_remove_role_admin(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    company.members.add(user)
    user_role = CompanyMember.objects.create(
        user=user, company=company, role=UserCompanyRole.ADMIN
    )

    response = owner_client.post(
        reverse("company-member-appoint-role", args=[company.id]),
        data={"user_id": user.id, "status_role": UserCompanyRole.USER},
    )

    assert response.status_code == status.HTTP_200_OK

    user_role = CompanyMember.objects.get(user=user, company=company)
    assert user_role.role == UserCompanyRole.USER
