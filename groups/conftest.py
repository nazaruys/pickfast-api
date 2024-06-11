import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth import get_user_model
from groups.models import Group, Store, Product

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return baker.make(User)

@pytest.fixture
def group(user):
    return baker.make(Group, admin=user)

@pytest.fixture
def store(group):
    return baker.make(Store, group=group)

@pytest.fixture
def product(group, store, user):
    return baker.make(Product, group=group, store=store, added_by=user)
