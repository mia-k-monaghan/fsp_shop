from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('terms-of-service/', views.TermsView.as_view(),name='terms'),
    path('privacy-policy/',views.PrivacyView.as_view(),name='privacy'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('webhooks', views.webhook_view),
]
