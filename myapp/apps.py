from django.apps import AppConfig
from time import sleep


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        print("Ready")
        # sleep(10)
