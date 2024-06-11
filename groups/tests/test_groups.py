from rest_framework import status
import pytest
from model_bakery import baker
from django.contrib.auth import get_user_model
from groups.models import Group

User = get_user_model()

@pytest.mark.django_db
class TestCreateGroup:
    def test_if_group_is_valid_returns_201(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.post('/api/group/groups/', {})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["admin"] == user.id
    
    def test_if_user_is_anonymous_returns_401(self, api_client):

        response = api_client.post('/api/group/groups/', {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_has_group_returns_403(self, api_client, group):
        user = baker.make(User, group=group)
        api_client.force_authenticate(user=user)

        response = api_client.post('/api/group/groups/', {})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'] == 'You do not have permission to perform this action.'

@pytest.mark.django_db
class TestRetrieveGroup:
    def test_if_group_exists_and_user_is_member_returns_200(self, api_client, group):
        user = baker.make(User, group=group)
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == group.pk

    def test_if_user_is_not_group_member_returns_403(self, api_client, group):
        user = baker.make(User)
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'] == 'You do not have permission to perform this action.'

    def test_if_group_does_not_exist_returns_404(self, api_client):

        response = api_client.get(f'/api/group/group/00000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateGroup:
    def test_if_valid_data_returns_200(self, api_client, user):
        admin_user = user
        group = baker.make(Group, admin=admin_user)
        api_client.force_authenticate(user=admin_user)
        new_admin = baker.make(User, group=group)

        response = api_client.patch(f'/api/group/groups/{group.pk}/', {"admin": new_admin.pk})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["admin"] == new_admin.pk

    def test_if_invalid_data_returns_404(self, api_client, user):
        admin_user = user
        group = baker.make(Group, admin=admin_user)
        api_client.force_authenticate(user=admin_user)

        response = api_client.patch(f'/api/group/groups/{group.pk}/', {"admin": 0})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["admin"] != 0
    
    def test_if_user_is_not_admin_returns_403(self, api_client, group, user):
        user = baker.make(User, group=group)
        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/api/group/groups/{group.pk}/', {"admin": user.pk})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'] == 'You do not have permission to perform this action.'

