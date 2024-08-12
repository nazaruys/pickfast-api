from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Store, Group, Product

User = get_user_model()

class StoreSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
 
    class Meta:
        model = Store
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['code', 'admin', 'private', 'users_blacklist']

class MembersUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'admin_of']
        
class ProductSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    added_by = MembersUserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'priority', 'date_buyed', 'store_id', 'store_name', 'added_by']