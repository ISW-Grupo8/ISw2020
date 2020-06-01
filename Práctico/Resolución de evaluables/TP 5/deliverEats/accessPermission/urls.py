from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ClientCreateView

app_name = 'access_permission'

urlpatterns = [
  # Client
  path('client/create/', ClientCreateView.as_view(), name='client_create'),
  ]