from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "phone", "date_of_birth", "is_active",
            "full_name", "is_adult"
        )
        read_only_fields = ("full_name", "is_adult")   # ensure these are not editable


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "first_name", "last_name", "phone", "date_of_birth")

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
