from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .signals import user_registered


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user_registered.send(sender=user.__class__, user=user, request=self.request)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"})


class HomeView(APIView):
    permission_classes = [permissions.AllowAny]  # Public endpoint

    def get(self, request):
        return Response({
            "message": " Welcome Asad! Good to see you here ",
            "developer": "Asad Hussain",
            "endpoints": {
                "register": "/api/auth/register/",
                "login": "/api/auth/login/",
                "users": "/api/auth/users/",
                "profile": "/api/auth/profile/",
                "logout": "/api/auth/logout/",
                "jwt_token": "/api/token/",
                "jwt_refresh": "/api/token/refresh/",
                "admin": "/admin/"
            }
        }, status=status.HTTP_200_OK)
    