from django.contrib.auth import get_user_model
from rest_framework import status
import pytest

User = get_user_model()

@pytest.mark.django_db
class TestCreateStore:
    def test_if_store_is_valid_returns_201(self, api_client, user, group):
        user.group = group
        api_client.force_authenticate(user=user)

        response = api_client.post(f'/api/group/groups/{group.pk}/stores/', {"name": "a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "a"
    
    def test_if_user_is_not_group_member_returns_403(self, api_client, user, group):
        api_client.force_authenticate(user=user)

        response = api_client.post(f'/api/group/groups/{group.pk}/stores/', {"name": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_invalid_returns_400(self, api_client, user, group):
        user.group = group
        api_client.force_authenticate(user=user)

        response = api_client.post(f'/api/group/groups/{group.pk}/stores/', {'a': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestRetrieveStore:
    def test_if_store_exists_returns_200(self, api_client, user, group, store):
        user.group = group
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/stores/{store.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == store.id
    
    def test_if_user_is_not_group_member_returns_403(self, api_client, user, group, store):
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/stores/{store.pk}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_store_does_not_exist_returns_404(self, api_client, user, group):
        user.group = group
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/stores/0/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestUpdateStore:
    def test_if_data_is_valid_returns_200(self, api_client, user, group, store):
        user.group = group
        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/api/group/groups/{group.pk}/stores/{store.pk}/', {"name": "a"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "a"
    
    def test_if_user_is_not_group_member_returns_403(self, api_client, user, group, store):
        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/api/group/groups/{group.pk}/stores/{store.pk}/', {"name": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_invalid_returns_400(self, api_client, user, group, store):
        user.group = group
        api_client.force_authenticate(user=user)

        response = api_client.patch(f'/api/group/groups/{group.pk}/stores/{store.pk}/', {'name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestListStores:
    def test_if_stores_exist_returns_200(self, api_client, user, group, store):
        user.group = group
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/stores/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['id'] == store.id
        
    def test_if_user_is_not_group_member_returns_403(self, api_client, user, group):
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/stores/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestListStores:
    def test_if_stores_exist_returns_200(self, api_client, user, group, store):
        user.group = group
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/stores/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['id'] == store.id
        
    def test_if_user_is_not_group_member_returns_403(self, api_client, user, group):
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/group/groups/{group.pk}/stores/')

        assert response.status_code == status.HTTP_403_FORBIDDEN
