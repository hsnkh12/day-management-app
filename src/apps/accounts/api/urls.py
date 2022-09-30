from django.urls import path,include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    
    path("register/",registerView,name="register"),
    path("login/",obtain_auth_token,name="login"),
    path("logout/",Logout.as_view(),name="logout"),
    path("profile/",ProfileView.as_view(),name="profile")
]
