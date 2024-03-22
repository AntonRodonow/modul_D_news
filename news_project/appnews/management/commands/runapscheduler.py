import logging

from appnews.tasks import weekly_digest  # если подчеркивает красным выставить Mark Directory -> Sorce Root

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from django.core.management.base import BaseCommand

from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# from django.conf import settings as django_settings # крутой способ загрузить что-то из settings.py
logger = logging.getLogger(__name__)


def my_job():
    """Еженедельные рассылки по пятницам в 18:00. кодом python manage.py runapscheduler."""
    weekly_digest()


# функция, которая будет удалять неактуальные задачи:
def delete_old_job_executions(max_age=604_800):  # аргумент max_age в секундах
    """Удаление неактуальных задач из БД (Отправка еженедельных рассылок)."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler. python manage.py runapscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone='Europe/Moscow')
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику:
        scheduler.add_job(
            my_job,
            # # Еженедльная отправка по пятницам (можно цифрой 5), врмея цифрой или строкой, 00 по умолчанию:
            trigger=CronTrigger(day_of_week='fri', hour=18, minute='00'),
            # trigger=CronTrigger(day_of_week='thu', hour=17, minute='40'),  # стока для тестирования-отладки
            id="my_job",
            max_instances=10,
            replace_existing=True,
        )

        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
