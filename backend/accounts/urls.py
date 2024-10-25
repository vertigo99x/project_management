from django.urls import path
from .views import UserDetailView, GetUsers, ChangePassword

urlpatterns = [
    path('userdata/', UserDetailView.as_view(), name='user-detail'),
    path('users/', GetUsers.as_view(), name='users'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
]


