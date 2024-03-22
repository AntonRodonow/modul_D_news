# import time
import datetime as dt
from datetime import timedelta

from celery import shared_task

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
# from django.http import HttpResponse
from django.template.loader import render_to_string

from news_project.settings import SERVER_EMAIL, SITE_URL  # подчеркивает, но работает, через appnews не ищет
# можно from django.conf import settings и дальше пеменные или from django.conf.global_settings import SERVER_EMAIL

from .models import Category, Post, PostCategory
# from .signals import notify_managers_post

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # с применением python ver > 3.9 эта библиотека встроенная


def weekly_digest():
    """Отправка еженедельной рассылки подписчикам о постах послденей недели в подписанных категориях.
    Отправляется отдельное письмо на каждую категорию."""
    categories = Category.objects.all()
    week = timedelta(days=7)
    for category in categories:
        category_subscribers = category.subscribers.all()
        category_subscribers_emails = []  # список подписчиков для каждой отдельной категории

        for subscriber in category_subscribers:
            category_subscribers_emails.append(subscriber.email)

        weekly_posts_in_category = []  # список постов в каждой отдельно категории за неделю
        posts_in_category = Post.objects.all().filter(postArticleCategory=f'{category.id}')

        for post in posts_in_category:
            time_delta = dt.datetime.now(ZoneInfo('Europe/Moscow')) - post.dateCreation

            if time_delta < week:
                weekly_posts_in_category.append(post)
        print('----------------   ---------------')
        print('----------------   ---------------')
        print('----------------   ---------------')
        print(f'ID: {category.id}-{category}')
        print(f'Кол-во публикаций: {len(weekly_posts_in_category)}')
        print(category_subscribers_emails, 'print(category_subscribers_emails)')
        print(weekly_posts_in_category, 'print(weekly_posts_in_category)')
        print('----------------   ---------------')
        print('----------------   ---------------')
        print('----------------   ---------------')

        # отправка реализована внутри цикла по категориям:
        if category_subscribers_emails:
            msg = EmailMultiAlternatives(
                subject=f'Weekly digest for subscribed category "{category}" from News Portal.',
                body=f'Привет! Еженедельная подборка публикаций в выбранной категории "{category}"',
                from_email=SERVER_EMAIL,
                to=set(category_subscribers_emails),
            )

            html_content = render_to_string(
                'weekly_notify.html',
                {
                    'digest': set(weekly_posts_in_category),
                    'category': category,
                    'SITE_URL': SITE_URL,
                }
            )

            msg.attach_alternative(html_content, "text/html")

            msg.send()
        else:
            continue


# рабодта celery and radis:
# @shared_task
# def hello(request, n=3):
#     print("Hello, world!")  # end celery test
#     for i in range(n):
#         time.sleep(n)
#         print(i)
#     return HttpResponse('Hello!')


# задачи celery and redis на еженедельную отправку писем. Назначается в celery.py:
@shared_task
def weekly_digest_celery():
    print('weekly_digest_celery')
    weekly_digest()


# Рассылка после создания новости через celery and redis. Моя попытка реализация, работает
@shared_task
@receiver(m2m_changed, sender=PostCategory)  # Sender - Класс для которой создан экземпляр. Промежуточный класс модели, описывающий ManyToManyField. Этот класс создается автоматически при определении поля «многие ко многим»; вы можете получить к нему доступ, используя through атрибут в поле многие-ко-многим.
def notify_managers_post_celery(sender, instance, **kwargs):  # название метода добровольно, created не нужен, ошибка с ним; instance - Фактический экземпляр только что созданной модели.
    """Отправка о новых публикациях подписчикам на почту. Подготовка к отправке."""
    all_email_to_subscribers = None  # : list[str] = None
    if kwargs['action'] == 'post_add':
        for category in instance.postArticleCategory.all():  # если мы можем добавлять к нашему посту несколько категорий, это будет оптимальным
            subemail = set(User.objects.filter(categories__name=category).values_list('email', flat=True))  # если оставить __in и туда попадет только один элемент, он не проитерируется (одна категория) - вылетит ошибка
            all_email_to_subscribers = list(subemail)

    html_content = render_to_string('appnews/subscriber_post_created_email.html', {
        'text': instance.preview,
        'link': f'{SITE_URL}/appnews/{instance.id}',
        'author': instance.author,
    })

    print("тест send_notification")
    msg = EmailMultiAlternatives(
        subject=instance.title,
        body='',
        from_email=SERVER_EMAIL,
        to=all_email_to_subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
