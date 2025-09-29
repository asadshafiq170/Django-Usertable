from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_adult = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "date_of_birth",
            "is_active",
            "full_name",
            "is_adult",
        )

    def get_full_name(self, obj):
        return obj.full_name()   # Model function call

    def get_is_adult(self, obj):
        return obj.is_adult()    # Model function call
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "first_name", "last_name", "phone", "date_of_birth")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone=validated_data.get("phone", ""),
            date_of_birth=validated_data.get("date_of_birth", None),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if user and user.is_active:
            data["user"] = user
            return data
        raise serializers.ValidationError("Invalid credentials")
