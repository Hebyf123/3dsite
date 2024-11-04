from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        fields = (
            'id', 'email', 'username', 'password', 'name', 'surname',
            'photo', 'telegram_id', 'address', 'city','country','phone'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'role': {'required': True},
            'name' : {'required' : False},
            'surname' : {'required' : False},
            'country' : {'required' : False},
            'city' : {'required' : False},
            'address': {'required': False},
            'phone': {'required': False},
        }
    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'username' ,'name', 'surname',
            'photo', 'telegram_id', 'address', 'city','country','phone'
        )




