import pytest
from django.urls import reverse

from common.models import Invitation, InvitationStatus, Request
from company.models import Company
from rest_framework import status


@pytest.mark.django_db  # 2.1
def test_user_can_accept_invitation(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    invitation = Invitation.objects.create(sender=owner, receiver=user, company=company)

    url = reverse("accept-invitation", args=[invitation.id])
    response = user_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    invitation.refresh_from_db()
    assert invitation.status == InvitationStatus.APPROVED.value

    assert user in company.members.all()


@pytest.mark.django_db  # 2.2
def test_user_can_canceled_invitation(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    invitation = Invitation.objects.create(sender=owner, receiver=user, company=company)

    url = reverse("revoke_invitation", args=[invitation.id])
    response = user_client.post(url)

    assert response.status_code == 200
    invitation.refresh_from_db()
    assert invitation.status == "Canceled"


@pytest.mark.django_db  # 2.3
def test_send_request(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    company = Company.objects.create(name="New Company")

    url = reverse("send-request", args=[company.id])
    response = user_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    request = Request.objects.get(user=user, company=company)
    assert request.status == "Pending"


@pytest.mark.django_db  # 2.4
def test_owner_can_reject_request(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    request = Request.objects.create(user=user, company=company)

    url = reverse("cancel-request", args=[request.id])
    response = user_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    request.refresh_from_db()
    assert request.status == "Canceled"


@pytest.mark.django_db  # 2.5
def test_owner_can_remove_user_from_company(create_authenticated_users):
    owner, company, user, owner_client, user_client = create_authenticated_users

    company.members.add(user)

    url = reverse("remove-user-from-company", args=[company.id, user.id])
    response = user_client.post(url)

    assert response.status_code == status.HTTP_200_OK

    company.refresh_from_db()
    assert user not in company.members.all()
