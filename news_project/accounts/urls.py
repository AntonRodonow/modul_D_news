from django.contrib.auth.views import LoginView
from django.urls import path

from .views import BaseRegisterView

urlpatterns = [
    path('signup/', BaseRegisterView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    ]
