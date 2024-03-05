"""
Django settings for news_project project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1suie7kx43xwm@np$ipd)aji957yn0119gzkobaa@j@$5)9%o9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'localhost:<port_number>', ]  # '127.0.0.1', 'localhost' - было пусто. Нужно для гугл авторизации


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # провека уровня доступа авторизованного пользователя на какое-либо действие, дает класс User, необходим для регистрации по др. аккаунтов
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',  # необходим также для рег по др. аккаунтов
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # нужны для рег по др. аккаунтам:
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',

    # мои приложения:
    'appnews',
    'accounts',

    # загруженные устанавливаемые пакеты:
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    "allauth.account.middleware.AccountMiddleware",  # нужен для рег по др. аккаунтам
]

SITE_ID = 1  # дает запрос на сопоставление сайтов (список возможных сайтов), по мимо прочего, при ошибках, отсутствыие SITE_ID не вызовет сбой в работе сайта

ROOT_URLCONF = 'news_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # os.path.join(BASE_DIR, 'templates')
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Для регистрации с др. ресурсов AUTHENTICATION_BACKENDS (гугл,яндекс аккаунтов):
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Для регистрации через почту
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'   # поменял none на mandatory. Обычно на почту отправляется подтверждение
# аккаунта, после подтверждения которого восстанавливается полная функциональность учётной записи "none"(без подтвержд)
ACCOUNT_FORMS = {'signup': 'account.models.BaseRegisterForm'}  # вообще работала форма регистрации и без этой записи


WSGI_APPLICATION = 'news_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'  # TIME_ZONE = 'Europe/Moscow' или 'UTC' - в базе данных абсолюное время (нулевой пояс), а TIME_ZONE показывает относительное время (Московское)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # переопределение по умолчанию праймори ки во всем проекте

LOGIN_URL = '/accounts/login/'  # ссылка на страницу входа, а вот нужен ли первый слеш???? Нужен, это говорит об абсолютном пути, без него этим путем дописыватся существующий
LOGIN_REDIRECT_URL = '/appnews/'  # после входа автоперенаправление на страницу с новостями
LOGOUT_REDIRECT_URL = '/appnews/'  # соответственно при выходе из аккаунта
