from django.apps import AppConfig
from django.core.management import call_command


class PagesStaticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages_static'

    def ready(self):
        call_command('collectstatic', verbosity=0, interactive=False)
