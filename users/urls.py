from django.urls import path
from .views import LoginView,ProfileView, AccountSetUpView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('profile/<pk>',ProfileView.as_view(), name='profile'),
    path('create-account/', AccountSetUpView.as_view(), name='set-password'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
