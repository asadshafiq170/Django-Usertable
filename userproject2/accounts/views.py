from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    UpdateUserSerializer,
    PartialUpdateUserSerializer,
    DeleteUserSerializer
)
from .signals import user_registered
from .permissions import IsAdultUser


class UserModelViewSet(viewsets.ModelViewSet):
    """
    🔹 Unified ViewSet for all User operations
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # -------------------------
    # REGISTER
    # -------------------------
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_registered.send(sender=user.__class__, user=user, request=request)
            return Response(
                {"message": "User registered successfully!", "user": UserSerializer(user).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------
    # LOGIN
    # -------------------------
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------
    # LOGOUT
    # -------------------------
    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)

    # -------------------------
    # USERS LIST (ADULTS ONLY)
    # -------------------------
    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated, IsAdultUser])
    def users(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # -------------------------
    # PROFILE VIEW / UPDATE / PATCH
    # -------------------------
    @action(detail=False, methods=["get", "put", "patch"], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        user = request.user

        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            serializer = UpdateUserSerializer(user, data=request.data)
        else:
            serializer = PartialUpdateUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            msg = "Profile fully updated" if request.method == "PUT" else "Profile partially updated"
            return Response({"message": msg, "user": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------
    # DELETE ACCOUNT
    # -------------------------
    @action(detail=False, methods=["delete"], permission_classes=[permissions.IsAuthenticated])
    def delete_account(self, request):
        user = request.user
        username = user.username
        user.delete()
        return Response(
            {"message": f"User '{username}' deleted successfully."},
            status=status.HTTP_200_OK
        )
