from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


# Create your models here.
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    def save(self):
        user = super(BaseRegisterForm, self).save()
        common_group = Group.objects.get(name='common')  # в name группа по умолчанию
        common_group.user_set.add(user)
        return user

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)
