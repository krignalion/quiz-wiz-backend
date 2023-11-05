import pytest
from django.urls import reverse

from users.models import UserRequest
from company.models import Invitation
from rest_framework import status
from common.models import RequestStatus, InvitationStatus
from company.models import Company


# @pytest.mark.django_db  # company 1.1
# def test_owner_send_invitations(create_authenticated_users):
#     owner, company, user, owner_client, user_client = create_authenticated_users
#
#     # response = owner_client.get(reverse("send_invitation") + f'?company_id={company.id}&user_id={user.id}')
#
#     response = owner_client.post(reverse("send_invitation", args=[company.id, user.id]))
#
#     assert response.status_code == status.HTTP_200_OK
#     assert Invitation.objects.filter(
#         sender=owner, receiver=user, company=company
#     ).exists()


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
