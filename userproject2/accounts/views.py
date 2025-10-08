from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .signals import user_registered
from .permissions import IsAdultUser


# -------------------
# API VIEWS
# -------------------

class RegisterView(generics.CreateAPIView):  ### sirf create krta hai
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user_registered.send(sender=user.__class__, user=user, request=self.request)


class LoginView(APIView):  ### login krta hai
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


class UserListView(generics.ListAPIView):  ### only list krta hai
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateAPIView): ### get krta hai aur update krta hai
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):  ### logout krta hai
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"})


class HomeView(APIView):  ### simple welcome message
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


# -------------------
#  ViewSets
# -------------------

# 1. Simple ViewSet (sab manually likhna parta hai)
class UserViewSet(viewsets.ViewSet):   #### manually sab kuch likhna parta hai
    def list(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# 2. GenericViewSet (mixins ke sath) ### ak time pay hum 3 cruds use kr sakty hain ###

class UserGenericViewSet(mixins.ListModelMixin,   ## sirf list aur retrieve krta hai
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


# 3. ModelViewSet (full CRUD ready-made)
class UserModelViewSet(viewsets.ModelViewSet):  ### full CRUD ready-made
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


## Permission Implementation ###

# class UserDetailView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

#     def get_object(self):
#         return self.request.user


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdultUser]
