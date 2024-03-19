from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory

from news_project.settings import SITE_URL, SERVER_EMAIL  # подчеркивает, но работает, через appnews не ищет


def send_notification(preview, pk, title, all_email_to_subscribers, author):
    """Отправка о новых публикациях подписчикам на почту. Сама отправка"""
    html_content = render_to_string('appnews/subscriber_post_created_email.html', {
        'text': preview,
        'link': f'{SITE_URL}/appnews/{pk}',
        'author': author,
    })

    print("тест send_notification")
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=SERVER_EMAIL,
        to=all_email_to_subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)  # Sender - Класс для которой создан экземпляр. Промежуточный класс модели, описывающий ManyToManyField. Этот класс создается автоматически при определении поля «многие ко многим»; вы можете получить к нему доступ, используя through атрибут в поле многие-ко-многим.
def notify_managers_post(sender, instance, **kwargs):  # название метода добровольно, created не нужен, ошибка с ним; instance - Фактический экземпляр только что созданной модели.
    """Отправка о новых публикациях подписчикам на почту. Подготовка к отправке"""
    all_email_to_subscribers = None  # : list[str] = None
    if kwargs['action'] == 'post_add':
        for category in instance.postArticleCategory.all():  # если мы можем добавлять к нашему посту несколько категорий, это будет оптимальным
            subemail = set(User.objects.filter(categories__name=category).values_list('email', flat=True))  # если оставить __in и туда попадет только один элемент, он не проитерируется (одна категория) - вылетит ошибка
            all_email_to_subscribers = list(subemail)
            print(subemail, "subemail")  # откуда берется первый email в виде пустой строки, стоит разобраться.
            # for user in category.subscribers.all():  # вторая возможная реализация
            #     if user.email not in all_email_to_subscribers:
            #         all_email_to_subscribers.append(user.email)

    send_notification(instance.preview, instance.id, instance.title, all_email_to_subscribers,
                      instance.author)


# # для теста
# @receiver(post_save, sender=Post)
# def news_created(instance, **kwargs):
#     print('Создана новость', instance)
