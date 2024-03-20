import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')  # устанавливаем переменную окружения
# по умолчанию DJANGO_SETTINGS_MODULE для программы командной строки celery

appCelery = Celery('news_project')
appCelery.config_from_object('django.conf:settings', namespace='CELERY')  # настройка celery из файла настроек проекта

appCelery.autodiscover_tasks()  # автоматическое отслоеживание зачач по декоратору в файлах tasks.py


appCelery.conf.beat_schedule = {
    'news_every_monday_8am_for_subscribers': {
        'task': 'appnews.tasks.weekly_digest_celery',
        # 'schedule': crontab(hour='8', minute='0', day_of_week='monday'),
        'schedule': crontab(hour='17', minute='11', day_of_week='tuesday'),
        'args': (),
    },
}

# тестирование отложенных задач для команды celery --app news_project beat -l info .Со сбросом задачи в args в сек
# appCelery.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'appnews.tasks.hello',
#         'schedule': 5,
#         'args': (5,),
#     },
# }
