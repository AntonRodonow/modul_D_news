from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import BaseRegisterView, upgrade_me

urlpatterns = [
    path('signup/', BaseRegisterView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Он переопределяет выход из аккаунта, т.е. не переспрашивает выход. Работает либо template_name, либо next_page,
    # в которую передается name из этого же urls.py
    # (можно без этой строки кода, сбработает из настроек LOGOUT_REDIRECT_URL):
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html', next_page='login'), name='logout'),
    # нужен для аутентификации по почте (сторонний сервис), сейчас работает без него, мы переписали часть путей
    # напирмер login/ - https://riptutorial.com/django/example/29948/using-django-allauth:
    # path('', include('allauth.urls')),  # дубляж какой-то с urls.py проекта, отключая для теста
    path('upgradeuser/', upgrade_me, name='upgrade'),  # расширение прав users
    ]
