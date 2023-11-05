import pytest
from django.urls import reverse

from users.models import UserRequest
from company.models import Invitation, Company
from rest_framework import status
from common.models import RequestStatus, InvitationStatus


@pytest.mark.django_db  # company 1.1
def test_owner_send_invitations(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    response = owner_client.post(reverse("send_invitation", args=[company.id, user.id]))

    assert response.status_code == status.HTTP_200_OK
    assert Invitation.objects.filter(
        sender=owner, receiver=user, company=company
    ).exists()


@pytest.mark.django_db  # 1.2
def test_owner_revoke_invitation(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    invitation = Invitation.objects.create(sender=owner, receiver=user, company=company)

    response = owner_client.post(reverse("revoke_invitation", args=[invitation.id]))

    assert response.status_code == 200
    invitation = Invitation.objects.get(id=invitation.id)
    assert invitation.status == InvitationStatus.REVOKED


@pytest.mark.django_db  # 1.3
def test_owner_approve_request(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    request = UserRequest.objects.create(user=user, company=company)
    response = owner_client.post(reverse("approve-request", args=[request.id]))

    assert response.status_code == status.HTTP_200_OK

    request = UserRequest.objects.get(id=request.id)
    assert request.status == RequestStatus.APPROVED


@pytest.mark.django_db  # 1.4
def test_owner_reject_request(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    request = UserRequest.objects.create(user=user, company=company)

    response = owner_client.post(reverse("cancel-request", args=[request.id]))

    assert response.status_code == status.HTTP_200_OK

    request = UserRequest.objects.get(id=request.id)
    assert request.status == RequestStatus.REJECTED


@pytest.mark.django_db  # 1.5
def test_owner_remove_user_from_company(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    company.members.add(user)

    response = owner_client.post(
        reverse("remove-user-from-company", args=[company.id, user.id])
    )

    assert response.status_code == status.HTTP_200_OK

    company = Company.objects.get(id=company.id)
    assert user not in company.members.all()
