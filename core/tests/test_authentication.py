from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import pytest
from model_bakery import baker
from groups.models import Group
from core.functions import is_refresh_token_blacklisted

User = get_user_model()

@pytest.mark.django_db
class TestAuthentications:
    def test_if_user_created_returns_tokens(self, api_client):
        
        response = api_client.post('/api/core/users/', {"username": "a", "email": "aaa@aaa.aaa", "password": "123456Aa"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["token"]["refresh"]
        assert response.data["token"]["access"]
    
    def test_if_logged_in_returns_tokens(self, api_client):
        baker.make(User, username='a', password=make_password('123456Aa'))

        response = api_client.post('/api/core/login/', {"username": "a", "password": "123456Aa"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["refresh"]
        assert response.data["access"]
    
    def test_if_invalid_login_returns_401(self, api_client):

        response = api_client.post('/api/core/login/', {"username": "a", "password": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not 'refresh' in response.data

    def test_if_refresh_token_is_valid_returns_access_token(self, api_client, user):
        refresh_token = RefreshToken.for_user(user)
        
        response = api_client.post('/api/core/refresh/', {"refresh": str(refresh_token)})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['access']

    def test_if_refresh_token_is_invalid_returns_401(self, api_client, user):
        
        response = api_client.post('/api/core/refresh/', {"refresh": 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not 'access' in response.data
    
    def test_token_is_blacklisted_after_logout(self, api_client, user):
        refresh_token = str(RefreshToken.for_user(user))

        response = api_client.post('/api/core/logout/', {'refresh': refresh_token})

        assert response.status_code == status.HTTP_200_OK
        assert is_refresh_token_blacklisted(refresh_token)

    
