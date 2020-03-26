
__all__ = ['API_VIEW', 'API_URL']


API_URL = """from django.conf.urls import include, url
from api_views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns = [
{% for model in models %}
  url(r'^{{ model|lower }}/(?P<pk>[0-9A-Fa-f-]+)/$', {{ model }}DetailView.as_view()),
  url(r'^{{ model|lower }}/$', {{ model }}ListView.as_view()),
{% endfor %}
]
"""


API_VIEW = """from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, serializers
from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from {{ app }}.serializers import {{ serializers|join:', ' }}
from {{ app }}.models import {{ models|join:', ' }}
{% load crudcustomtags %}

{% for model in models %}

class {{ model }}ListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = {{ model }}.objects.all()
    serializer_class = {{ model }}Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {% fields_filter app model %}
     
 
class {{ model }}DetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = {{model}}.objects.all()
    serializer_class = {{model}}Serializer
    
{% endfor %}"""
