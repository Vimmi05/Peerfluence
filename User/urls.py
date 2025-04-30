from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserProfile, name='userProfile'),
    path('UpdateUserProfile/<int:id>/', views.UpdateUserProfile, name="updateProfile"),
    path('manage-skills/', views.manage_skills, name='manage_skills'),
    
]

             