from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

def home(request):
    return JsonResponse({"message": "Welcome to JWT Auth API 🚀"})

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('accounts/', include('accounts.urls')),  # apne app ke urls
    path('api/auth/', include('accounts.urls')),  # API endpoints

]
