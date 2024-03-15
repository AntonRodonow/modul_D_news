from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
import datetime as DT
from datetime import timedelta
from backports.zoneinfo import ZoneInfo

# from celery import shared_task
# import time

from news_project.settings import SERVER_EMAIL, SITE_URL, TIME_ZONE  # подчеркивает, но работает, через appnews не ищет
# можно from django.conf import settings и дальше пеменные или from django.conf.global_settings import SERVER_EMAIL


# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")# end celery test
#     return 'life'
#
#

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


# задача celery and redis на еженедельную отправку писем:
# @shared_task
# def weekly_digest_celery():
#     categories = Category.objects.all()
#     today = DT.datetime.today()
#     week = timedelta(days=7)
#
#     print('today', today)
#
#     for category in categories:
#         category_subscribers = category.subscribers.all()
#         print('category_subscribers', category_subscribers)
#         category_subscribers_emails = []
#         for subscriber in category_subscribers:
#             category_subscribers_emails.append(subscriber.email)
#         print('category_subscribers', category_subscribers_emails)
#
#         weekly_posts_in_category = []
#         posts_in_category = Post.objects.all().filter(postCategory=f'{category.id}')
#
#         for post in posts_in_category:
#             print('today = ', today)
#             time_delta = DT.datetime.now() - post.dateCreation
#             print('time_delta', time_delta)
#             # days_delta = today - post.dateCreation
#
#
#             if time_delta < week:
#                 weekly_posts_in_category.append(post)
#
#         print(f'ID: {category.id}')
#         # print(category)# может из за этого не пашет
#         print(f'Кол-во публикаций: {len(weekly_posts_in_category)}')
#         print(category_subscribers_emails)
#         print(weekly_posts_in_category)
#         print('----------------   ---------------')
#         print('----------------   ---------------')
#         print('----------------   ---------------')
#
#         if category_subscribers_emails:
#             msg = EmailMultiAlternatives(
#                 subject=f'Weekly digest for subscribed category "{category}" from News Portal.',
#                 body=f'Привет! Еженедельная подборка публикаций в выбранной категории "{category}"',
#                 from_email=SERVER_EMAIL,
#                 to=category_subscribers_emails,
#             )
#
#             # получаем наш html
#             html_content = render_to_string(
#                 'weekly_notify_celery.html',
#                 {
#                     'notify': weekly_posts_in_category,
#                     'category': category,
#                 }
#             )
#
#             msg.attach_alternative(html_content, "text/html")  # добавляем html
#
#             msg.send()  # отсылаем
#         else:
#             continue
#
# # celery-redis задача на отправку при добавлении новости
# @shared_task
# def notify_subscribers(sub_name, sub_email, title, category, pub_time, pk):
#     post = Post.objects.get(id=pk)
#     subject = f'{sub_name}, новая публикация в разделе {category} - {title}. Дата выпуска статьи: {pub_time}.'
#
#     msg=EmailMultiAlternatives(
#         subject=subject,
#         body=f'Привет {sub_name}, новая публикация - {title}, в разделе {category}',
#         from_email=SERVER_EMAIL,
#         to=[f'{sub_email}'],
#     )
#     html_content = render_to_string(
#         'post_celery.html',
#         {
#             'post': post,
#             'user': sub_name,
#         }
#     )
#     msg.attach_alternative(html_content, "text/html")  # добавляем html
#     msg.send()  # отсылаем
