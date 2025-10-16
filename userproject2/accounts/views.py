import datetime
from functools import wraps
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, AdultUser
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer
)
from .signals import user_registered
from .permissions import IsAdultUser

# ✅ Custom decorator
def log_api_call(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        with open("api_log.txt", "a") as f:
            f.write(f"[{datetime.datetime.now()}] {func.__name__} called by {request.user}\n")
        return func(self, request, *args, **kwargs)
    return wrapper


# ✅ Unified ViewSet
class UserModelViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ---------------------- REGISTER ----------------------
    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_registered.send(sender=user.__class__, user=user, request=request)
            return Response({
                "message": "User registered successfully!",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------------- LOGIN ----------------------
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

    # ---------------------- LOGOUT ----------------------
    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)

    # ---------------------- USER LIST (Adults Only) ----------------------
    @log_api_call
    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated, IsAdultUser])
    def users(self, request):
        adults = AdultUser.objects.all()
        serializer = UserSerializer(adults, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ---------------------- PROFILE ----------------------
    @action(detail=False, methods=["get", "put", "patch"], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data)

        serializer = UserSerializer(user, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------------- DELETE ACCOUNT ----------------------
    @action(detail=False, methods=["delete"], permission_classes=[permissions.IsAuthenticated])
    def delete_account(self, request):
        username = request.user.username
        request.user.delete()
        return Response({"message": f"User '{username}' deleted successfully."})
