from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    group_id = serializers.CharField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'password', 'group_id', 'admin_of', 'verified']
        extra_kwargs = {'password': {'write_only': True}, 'admin_of': {'read_only': True}, 'verified': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()