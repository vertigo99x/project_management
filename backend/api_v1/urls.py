# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectView.as_view(), name='projects'),
    path('projects/create/', views.ProjectView.as_view(), name='create_project'),
    path('projects/update/<uuid:uuid>/', views.ProjectView.as_view(), name='update_project'),
    path('projects/delete/<uuid:uuid>/', views.ProjectView.as_view(), name='delete_project'),
    path('dashboard/', views.DashboardData.as_view(), name='dashboard'),
    path('activities/', views.ActivityView.as_view(), name='activity'),
]
