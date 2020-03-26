from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def entity_filter(app_name,modelname):
    from django.apps import apps
    model = apps.get_model(app_name,modelname)
    all_fields = model._meta.get_fields()
    list_string=""
    for field in all_fields:
        list_string+=field.name+":any;"+"\n"
    return mark_safe(list_string)

@register.simple_tag
def fields_filter(app_name,modelname):
    from django.apps import apps
    model = apps.get_model(app_name,modelname)
    all_fields = model._meta.get_fields()
    list_string="["
    for field in all_fields:
        list_string+="'"+field.name+"',"
    list_string.rstrip(',')
    list_string=list_string.rstrip(',')+"]"
    return mark_safe(list_string)
