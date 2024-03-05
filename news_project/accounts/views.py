from django.contrib.auth.models import User

# Create your views here.
from django.views.generic import CreateView

from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/appnews/'
