from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


# ✅ User Display Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "phone", "date_of_birth", "is_active",
            "full_name", "is_adult"
        )
        read_only_fields = ("full_name", "is_adult")

    # 🧠 Customize Response Representation
    def to_representation(self, instance):
        """Yahan hum response customize karte hain"""
        data = super().to_representation(instance)
        data["full_name"] = f"{instance.first_name} {instance.last_name}"
        data["is_adult"] = instance.date_of_birth.year <= 2007  # Example logic
        data["status"] = "Active" if instance.is_active else "Inactive"
        return data


# ✅ Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'date_of_birth')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data.get('date_of_birth')
        )
        return user


# ✅ Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data


# ✅ Full Update Serializer (PUT)
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "date_of_birth"
        )

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.save()
        return instance


# ✅ Partial Update Serializer (PATCH)
class PartialUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "date_of_birth"
        )
        extra_kwargs = {
            field: {"required": False} for field in fields
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# ✅ Delete Serializer (Optional)
class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email"]

    def delete(self, instance):
        instance.delete()
        return {"message": f"User '{instance.username}' deleted successfully."}
