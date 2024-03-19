import time

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Post, Category, PostCategory
import datetime as DT
from datetime import timedelta

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # с применением python ver > 3.9 эта библиотека встроенная

from news_project.settings import SERVER_EMAIL, SITE_URL  # подчеркивает, но работает, через appnews не ищет
# можно from django.conf import settings и дальше пеменные или from django.conf.global_settings import SERVER_EMAIL


def weekly_digest():
    """Отправка еженедельной рассылки подписчикам о постах послденей недели в подписанных категориях.
    Отправляется отдельное письмо на каждую категорию"""
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
            time_delta = DT.datetime.now(ZoneInfo('Europe/Moscow')) - post.dateCreation

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
@shared_task
def hello(request, n=3):
    print("Hello, world!")  # end celery test
    for i in range(n):
        time.sleep(n)
        print(i)
    return HttpResponse('Hello!')


# задачи celery and redis на еженедельную отправку писем:
@shared_task
def weekly_digest_celery():
    categories = Category.objects.all()
    week = timedelta(days=7)
    for category in categories:
        category_subscribers = category.subscribers.all()
        category_subscribers_emails = []

        for subscriber in category_subscribers:
            category_subscribers_emails.append(subscriber.email)

        weekly_posts_in_category = []
        posts_in_category = Post.objects.all().filter(postCategory=f'{category.id}')

        for post in posts_in_category:
            time_delta = DT.datetime.now(ZoneInfo('Europe/Moscow')) - post.dateCreation

            if time_delta < week:
                weekly_posts_in_category.append(post)

        if category_subscribers_emails:
            msg = EmailMultiAlternatives(
                subject=f'Weekly digest for subscribed category "{category}" from News Portal.',
                body=f'Привет! Еженедельная подборка публикаций в выбранной категории "{category}"',
                from_email=SERVER_EMAIL,
                to=category_subscribers_emails,
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


# рассылка после создания новости через celery and redis
@shared_task
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    all_email_to_subscribers = None
    if kwargs['action'] == 'post_add':
        for category in instance.postArticleCategory.all():  # если мы можем добавлять к нашему посту несколько категорий, это будет оптимальным
            subemail = set(User.objects.filter(categories__name=category).values_list('email', flat=True))  # если оставить __in и туда попадет только один элемент, он не проитерируется (одна категория) - вылетит ошибка
            all_email_to_subscribers = list(subemail)

    html_content = render_to_string('appnews/subscriber_post_created_email.html', {
        'text': instance.preview,
        'link': f'{SITE_URL}/appnews/{instance.id}',
        'author': instance.author,
    })

    msg = EmailMultiAlternatives(
        subject=instance.title,
        body='',
        from_email=SERVER_EMAIL,
        to=all_email_to_subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
