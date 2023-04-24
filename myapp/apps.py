from django.apps import AppConfig
from myapp.migration.init import get_path
from myapp.migration.run import run


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    # def ready(self):
    #     run()
