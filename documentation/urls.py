from django.urls import path
from . import views

app_name = 'documentation'

urlpatterns = [
    path('deployment-guide/<slug>/',views.deployment_guide_view, name='deployment-guide'),
]
