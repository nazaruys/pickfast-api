from rest_framework import status
import pytest
from model_bakery import baker
from django.contrib.auth import get_user_model
from groups.models import Group


User = get_user_model()

@pytest.mark.django_db
class TestCreateUser:
    def test_if_user_is_valid_returns_201(self, api_client):
        data = {
            "username": "a",
            "email": "aaa@aaa.aaa",
            "password": "111111Aa"
        }

        response = api_client.post(f'/api/core/users/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user'] and response.data['token']
        

    def test_if_user_is_invalid_returns_400(self, api_client, user, group):
        data = {
            "username": 1,
            "email": "a",
            "password": "a"
        }

        response = api_client.post(f'/api/core/users/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestListUsers:
    def test_if_user_is_admin_returns_201(self, api_client, user):
        user.is_staff = 1
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/core/users/')

        assert response.status_code == status.HTTP_200_OK
        

    def test_if_user_is_not_admin_returns_403(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/core/users/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestRetrieveUser:
    def test_if_users_profile_returns_200(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/core/users/{user.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user.pk
    
    def test_if_not_users_profile_returns_403(self, api_client, user):
        api_client.force_authenticate(user=user)
        user_2 = baker.make(User)

        response = api_client.get(f'/api/core/users/{user_2.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestUpdateUser:
    def test_if_users_profile_returns_200(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/api/core/users/{user.pk}/', {"username": "a"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "a"
    
    def test_if_not_users_profile_returns_403(self, api_client, user):
        api_client.force_authenticate(user=user)
        user_2 = baker.make(User)

        response = api_client.patch(f'/api/core/users/{user_2.pk}/', {"username": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_data_returns_400(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/api/core/users/{user.pk}/', {"password": '1'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_group_is_private_returns_403(self, api_client, user):
        group = baker.make(Group, admin=user, private=True)
        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/api/core/users/{user.pk}/', {"group_id": group.pk})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert user.group_id != group.pk

    def test_if_user_is_blacklisted_returns_403(self, api_client, user):
            group = baker.make(Group, admin=user)
            group.users_blacklist.add(user)
            api_client.force_authenticate(user=user)

            response = api_client.patch(f'/api/core/users/{user.pk}/', {"group_id": group.pk})

            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert user.group_id != group.pk
