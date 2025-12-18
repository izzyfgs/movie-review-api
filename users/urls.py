from django.urls import path
from .views import UserRegisterView, CurrentUserView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', obtain_auth_token, name='api_token_auth'),  # POST username & password
    path('me/', CurrentUserView.as_view(), name='current_user'),  # GET info about logged-in user
]
