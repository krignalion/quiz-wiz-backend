import pytest
from django.urls import reverse

from users.models import UserRequest
from company.models import Company, Invitation
from rest_framework import status
from common.models import InvitationStatus, RequestStatus


@pytest.mark.django_db  # 2.1
def test_user_accept_invitation(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    invitation = Invitation.objects.create(sender=owner, receiver=user, company=company)

    response = user_client.post(reverse("accept-invitation", args=[invitation.id]))

    assert response.status_code == status.HTTP_200_OK

    invitation = Invitation.objects.get(id=invitation.id)
    assert invitation.status == InvitationStatus.APPROVED
    assert user in company.members.all()


@pytest.mark.django_db  # 2.2
def test_user_canceled_invitation(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    invitation = Invitation.objects.create(sender=owner, receiver=user, company=company)

    response = user_client.post(reverse("revoke_invitation", args=[invitation.id]))

    assert response.status_code == 200
    invitation = Invitation.objects.get(id=invitation.id)
    assert invitation.status == InvitationStatus.REJECTED


@pytest.mark.django_db  # 2.3
def test_send_request(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    company = Company.objects.create(name="New Company")

    response = user_client.post(reverse("send-request", args=[company.id]))

    assert response.status_code == status.HTTP_200_OK

    request = UserRequest.objects.get(user=user, company=company)
    assert request.status == RequestStatus.PENDING


@pytest.mark.django_db  # 2.4
def test_owner_reject_request(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    request = UserRequest.objects.create(user=user, company=company)

    response = user_client.post(reverse("cancel-request", args=[request.id]))

    assert response.status_code == status.HTTP_200_OK

    request = UserRequest.objects.get(id=request.id)
    assert request.status == RequestStatus.CANCELED


@pytest.mark.django_db  # 2.5
def test_owner_remove_user_from_company(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    company.members.add(user)

    response = user_client.post(
        reverse("remove-user-from-company", args=[company.id, user.id])
    )

    assert response.status_code == status.HTTP_200_OK
    company = Company.objects.get(id=company.id)
    assert user not in company.members.all()
