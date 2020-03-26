---------------------------------------------
Ionic and Django Rest API CRUD Generator
---------------------------------------------

Ionic and Django API Rest CRUD generator, will create automatically all the code needed to have a ready to Go Django Rest Framework API and Ionic API services ! No more boring and repetitive tasks each time you will have a new project.

---------------------
Django Rest Framework
---------------------
This library will parse your models (in your model.py file) and will automatically create files inside a directory named {{app}}_crud (where app is the name of your django app):

* `api_views.py` : The Django Rest framework API file.
* `serializers.py` : The Django Rest framework serializers file
* `api_urls.py` : The Django Rest framework url file.

For each model the following urls will be created:

 url(r'^{{ model }}/$', {{ model }}ListView.as_view()),

 url(r'^{{ model }}/(?P<pk>[0-9A-Fa-f-]+)/$', {{ model }}DetailView.as_view()),

The first url is to get or create a model
The second url is to get, update, delete a model

**Please note** that the primary key of your models must be UUID Fields
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
---------------
Ionic
---------------
This library will create :

* `ionic_apiservice.service.ts` : The Ionic API Service file which will create for each model, methods to get, find, update, delete the model. It will also create some common methods
* `ionic_entities.ts` : The Ionic entity class file for each model.



---------------

|python| |pypi| |license| |travis| |django| |drf|

---------------

* `Installation`_
* `Usage`_
* `License`_

---------------

============
Installation
============

Install with pip:

.. code-block:: bash

    $ pip install ionicdjangocrudgenerator

or Clone the repo and install manually:

.. code-block:: bash

    $ git clone https://github.com/csurbier/ionicdjangocrudgenerator.git
    $ cd ionicdjangocrudgenerator
    $ python setup.py install

To use the library, add it your INSTALLED_APPS.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rest_framework',
        'ionicdjangocrudgenerator',
        ...
    )

*Note*: In order to use the API classes, you must have the rest framework configuration in your settings.

.. code-block:: python

    REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
       'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

-----------------

=====
Usage
=====

To use run the following command, where ``app`` is the application to generate an API for.

.. code-block:: bash

   $ python manage.py generateCrud {app}

**Example:** Generate everything for the app ``backoffice``

.. code-block:: bash

    $ python manage.py generateCrud backoffice

-------------------

=======
License
=======

MIT License.
