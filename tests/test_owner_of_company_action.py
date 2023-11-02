import pytest
from django.urls import reverse

from common.models import Request
from company.models import Invitation
from rest_framework import status


@pytest.mark.django_db  # company 1.1
def test_owner_can_send_invitations(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    url = reverse("send_invitation", args=[company.id, user.id])
    response = owner_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert Invitation.objects.filter(
        sender=owner, receiver=user, company=company
    ).exists()


@pytest.mark.django_db  # 1.2
def test_owner_can_revoke_invitation(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    invitation = Invitation.objects.create(sender=owner, receiver=user, company=company)

    url = reverse("revoke_invitation", args=[invitation.id])
    response = owner_client.post(url)

    assert response.status_code == 200
    invitation.refresh_from_db()
    assert invitation.status == "Revoked"


@pytest.mark.django_db  # 1.3
def test_owner_can_approve_request(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    request = Request.objects.create(user=user, company=company)
    url = reverse("approve-request", args=[request.id])
    response = owner_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    request.refresh_from_db()
    assert request.status == "Approved"


@pytest.mark.django_db  # 1.4
def test_owner_can_reject_request(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    request = Request.objects.create(user=user, company=company)

    url = reverse("cancel-request", args=[request.id])
    response = owner_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    request.refresh_from_db()
    assert request.status == "Revoked"


@pytest.mark.django_db  # 1.5
def test_owner_can_remove_user_from_company(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    company.members.add(user)

    url = reverse("remove-user-from-company", args=[company.id, user.id])
    response = owner_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    company.refresh_from_db()
    assert user not in company.members.all()
