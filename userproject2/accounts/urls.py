from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router banaya
router = DefaultRouter()
router.register(r'users-viewset', views.UserViewSet, basename='users-viewset')
router.register(r'users-generic', views.UserGenericViewSet, basename='users-generic')
router.register(r'users-model', views.UserModelViewSet, basename='users-model')

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("profile/", views.UserDetailView.as_view(), name="user-detail"),

    # Router ke URLs add kiye
    path("routers/", include(router.urls)),
]
