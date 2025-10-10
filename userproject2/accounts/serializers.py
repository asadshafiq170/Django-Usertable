from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer): # Serializer for CustomUser model
    class Meta:  # Meta class to define model and fields
        model = CustomUser
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "phone", "date_of_birth", "is_active",
            "full_name", "is_adult"
        )
        read_only_fields = ("full_name", "is_adult")   # ensure these are not editable


class RegisterSerializer(serializers.ModelSerializer):  # Serializer for user registration
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'date_of_birth')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):  # Create user with hashed password
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data.get('date_of_birth')
        )
        return user

class LoginSerializer(serializers.Serializer):   # Serializer for user login
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data): # Validate user credentials
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data