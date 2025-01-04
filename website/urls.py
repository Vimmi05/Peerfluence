from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('Profile/', views.Profile, name='profile'),
    path('Followers/', views.Followers, name='followers'),

    path('SignUp/', views.SignUp, name='signup'),
    path('LogIn/', views.LogIn, name='login'),
    path('LogOut/', views.LogOut, name='logout'),

    path('CreateUserPost/', views.create_post, name='create_user_post'),

    

]
