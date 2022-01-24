from django.urls import path
from .views import LoginView,ProfileView, AccountSetUpView, activate, confirm_email, OrderDetailView, UpdateOrderView,CheckInboxView, InvalidLinkView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('profile/<pk>',ProfileView.as_view(), name='profile'),
    path('order/<pk>', OrderDetailView.as_view(), name='order-detail'),
    path('update-order/<pk>', UpdateOrderView.as_view(), name='update-order'),
    path('create-account/', AccountSetUpView.as_view(), name='set-password'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('confirm_email/<orderid>', confirm_email, name='confirm-email'),
    path('check-your-inbox/', CheckInboxView.as_view(), name='check-inbox'),
    path('invalid-link/', InvalidLinkView.as_view(), name='invalid-link'),
    path('activate/<orderidb64>/<token>', activate, name='activate'),

]
