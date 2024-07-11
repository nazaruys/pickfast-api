from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Store, Group, Product

User = get_user_model()

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name']
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['code', 'admin', 'private', 'users_blacklist']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'priority', 'date_buyed', 'store_id', 'added_by']

class MembersUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']