from django.template import Template, Context
import os.path

from ionicdjangocrudgenerator.templates.django.serializer import SERIALIZER
from ionicdjangocrudgenerator.templates.django.apiview import API_URL, API_VIEW
from ionicdjangocrudgenerator.templates.ionic.apiservice import API_SERVICE,ENTITY


__all__ = ['DjangoAPIGenerator', 'IonicGenerator']


class DjangoBaseGenerator(object):

    def __init__(self, app_config):
        self.app_config = app_config
        self.app = app_config.models_module
        self.name = app_config.name
        self.serializer_template = Template(SERIALIZER)
        self.models = self.get_model_names()
        self.serializers = self.get_serializer_names()

    def generate_serializers(self):
        content = self.serializer_content()
        filename = 'serializers.py'
        if self.write_file(content, filename):
            return 'created %s' % filename
        else:
            return 'Cancelled %s' % filename

    def generate_api(self):
        content = self.api_content()
        filename = 'api_views.py'
        if self.write_file(content, filename):
            return 'created %s' % filename
        else:
            return 'API cancelled'

    def generate_urls(self):
        content = self.url_content()
        filename = 'api_urls.py'
        if self.write_file(content, filename):
            return 'created %s' % filename
        else:
            return 'Url cancelled'

    def serializer_content(self):
        context = Context({'app': self.name, 'models': self.models})
        return self.serializer_template.render(context)

    def api_content(self):
        context = Context({'app': self.name, 'models': self.models, 'serializers': self.serializers})
        return self.api_template.render(context)

    def url_content(self):
        context = Context({'app': self.name, 'models': self.models})
        return self.url_template.render(context)

    def get_model_names(self):
        return [m.__name__ for m in self.app_config.get_models()]

    def get_serializer_names(self):
        return [m + 'Serializer' for m in self.models]

    def write_file(self, content, filename):
        directory = os.path.dirname(self.app.__file__) + "_crud"
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        name = os.path.join(directory, filename)
        print("name %s"%name)
        if os.path.exists(name):
            msg = "Are you sure you want to overwrite %s? (y/n): " % filename
            prompt = input  # python3
            response = prompt(msg)
            if response != "y":
                return False
        new_file = open(name, 'w+')
        new_file.write(content)
        new_file.close()
        return True

class IonicBaseGenerator(object):
    
    def __init__(self, app_config):
        self.app_config = app_config
        self.app = app_config.models_module
        self.name = app_config.name
        self.models = self.get_model_names()


    def generate_service(self):
        content = self.view_content()
        filename = 'ionic_apiservice.service.ts'
        if self.write_file(content, filename):
            return '  - created %s' % filename
        else:
            return 'Ionic service generation cancelled'

    def generate_entities(self):
        content = self.entity_content()
        filename = 'ionic_entities.ts'
        if self.write_file(content, filename):
            return '  - created %s' % filename
        else:
            return 'Ionic entities generation cancelled'

    def view_content(self):
        context = Context({'app': self.name, 'models': self.models})
        return self.api_template.render(context)

    def entity_content(self):
        context = Context({'app': self.name, 'models': self.models})
        return self.entities_template.render(context)


    def get_model_names(self):
        return [m.__name__ for m in self.app_config.get_models()]



    def write_file(self, content, filename):
        directory = os.path.dirname(self.app.__file__)+"_crud"
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        name = os.path.join(directory, filename)
        if os.path.exists(name):
            msg = "Are you sure you want to overwrite %s? (y/n): " % filename
            prompt = input  # python3
            response = prompt(msg)
            if response != "y":
                return False
        new_file = open(name, 'w+')
        new_file.write(content)
        new_file.close()
        return True

class DjangoAPIGenerator(DjangoBaseGenerator):

    def __init__(self, app_config):
        super(DjangoAPIGenerator, self).__init__(app_config)
        self.api_template = Template(API_VIEW)
        self.url_template = Template(API_URL)


class IonicGenerator(IonicBaseGenerator):

    def __init__(self, app_config):
        super(IonicGenerator, self).__init__(app_config)
        self.api_template = Template(API_SERVICE)
        self.entities_template = Template(ENTITY)
         

 