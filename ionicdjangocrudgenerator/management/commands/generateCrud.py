import sys

from django.core.management.base import AppCommand, CommandError
from ionicdjangocrudgenerator.crudgenerator import *
import django


class Command(AppCommand):
    help = 'Create Django Rest Framework API (Views,Serializers,urls) and Ionic API services (C.R.U.D)'

    args = "[appname]"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        

    def handle_app_config(self, app_config, **options):
        if app_config.models_module is None:
            raise CommandError('You must provide an app to generate files')

        if sys.version_info[0] != 3 or sys.version_info[1] < 5:
            raise CommandError('Python 3.5 or newer is required')

        if django.VERSION[1] >= 11 or django.VERSION[0] in [2, 3]:
            pass
        else:
            raise CommandError('Only compatible with Django 1.11, 2.2, or 3.0')

        djangoGenerator = DjangoAPIGenerator(app_config)
        
        djangoGenerator.generate_serializers()
        djangoGenerator.generate_api()
        djangoGenerator.generate_urls()

        ionicGenerator = IonicGenerator(app_config)
        ionicGenerator.generate_service()
        ionicGenerator.generate_entities()
       
