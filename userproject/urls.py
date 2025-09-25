from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

def home(request):
    return JsonResponse({"message": "Welcome to JWT Auth API"})

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    # JWT endpoints
    path('accounts/', include('accounts.urls')), 
    path('auth/', include('accounts.urls')),  
]
