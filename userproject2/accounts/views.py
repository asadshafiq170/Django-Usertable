from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
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
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Successfully logged out'})

from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Welcome to User API",
        "developer": "Asad Hussain",
        "endpoints": {
            "register": "/api/auth/register/",
            "login": "/api/auth/login/",
            "profile": "/api/auth/profile/",
            "logout": "/api/auth/logout/",
            "admin": "/admin/"
        }
    })
