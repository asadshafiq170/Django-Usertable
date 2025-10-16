from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_adult = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone", "date_of_birth", "is_active", "full_name", "is_adult"
        ]

    def get_full_name(self, obj):
        return obj.full_name()

    def get_is_adult(self, obj):
        return obj.is_adult()


# ✅ Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "first_name", "last_name", "phone", "date_of_birth"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


# ✅ Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
