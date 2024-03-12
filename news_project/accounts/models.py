from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

# Create your models here.
from django.shortcuts import render
from django.template import Context

from django.core.mail import EmailMultiAlternatives, mail_managers, mail_admins
from django.template.loader import get_template


class BaseRegisterForm(UserCreationForm):
    """Форма регистрации нового юзера"""
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    @property
    def save(self):  # request не было в рабочей версии, тестирую
        """Сохрание нового user в БД, присвоение низших прав доступа при регистрации.
        Отправка приветствия на почту нового пользователя"""
        user = super(BaseRegisterForm, self).save()
        common_group = Group.objects.get(name='common')  # в name группа по умолчанию
        common_group.user_set.add(user)

        # настройка отправки приветствий новым users:
        """выберите форму отправки письма 
        1- текст в теле данной функции, 
        2- текст в .txt файле:"""
        sendmail = 2

        if sendmail == 1:
            subject = 'Добро пожаловать на наш новостной портал!'  # тема письма
            text = f'{user.username}, вы успешно зарегистрировались!'
            html = (
                f'<b>{user.username}</b>, вы успешно зарегистрировались на '
                f'<a href="http://127.0.0.1:8000/appnews">сайте</a>!'
            )
            msg = EmailMultiAlternatives(  # настройка для отправки html или если это не поддерживается почтой - text
                subject=subject,
                body=text,
                from_email=None,  # берет по умолчанию из settings
                to=[user.email]
            )
            msg.attach_alternative(html, "text/html")
            msg.send()

        if sendmail == 2:
            subject = 'Добро пожаловать на наш новостной портал!'
            text = f'{user.username}, вы успешно зарегистрировались!'
            html = get_template('accounts/email/email_confirmation_message.html').render()  # интеерсное расширение .txt
            msg = EmailMultiAlternatives(  # настройка для вариантной отправки html или если не поддерживается почтой - text
                subject=subject,
                body=text,
                from_email=None,
                to=[user.email]
            )
            msg.attach_alternative(html, "text/html")
            msg.send()

        # отправка уведомлений менеджерам сайта и ниже админам:
        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user

    class Meta:
        """Заполняемые поля при регистрации"""
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)
