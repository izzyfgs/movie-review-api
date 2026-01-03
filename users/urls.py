from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserCreateView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),     
    path('login/', obtain_auth_token, name='user-login'),
    path('register/', UserCreateView.as_view(), name='register'),
]
