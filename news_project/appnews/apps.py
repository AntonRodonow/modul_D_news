# import redis
from django.apps import AppConfig


class AppnewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appnews'

    def ready(self):
        from . import signals
        # import appnews.signals # либо так
        from .tasks import weekly_digest
