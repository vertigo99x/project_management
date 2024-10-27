from django.urls import path
from .views import UserDetailView, GetUsers, UserCreateView

urlpatterns = [
    path('userdata/', UserDetailView.as_view(), name='user-detail'),
    path('users/', GetUsers.as_view(), name='users'),
    path('create-user/', UserCreateView.as_view(), name='user-create'),
]


