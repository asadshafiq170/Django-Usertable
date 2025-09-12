from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'is_active')
        read_only_fields = ('id', 'is_active')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'date_of_birth')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid login credentials")
