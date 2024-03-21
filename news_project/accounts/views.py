from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
# Create your views here.
from django.shortcuts import redirect
from django.views.generic import CreateView

from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    """Представление с формой регистрации для новых Users"""
    model = User
    form_class = BaseRegisterForm
    success_url = '/appnews'


@login_required
def upgrade_me(request):
    """Даем расширенные права для Users"""
    user = request.user
    authors_group = Group.objects.get(name='Autors')
    if not request.user.groups.filter(name='Autors').exists():
        authors_group.user_set.add(user)
    return redirect('/appnews')
