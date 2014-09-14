from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
from django.template import Node, TemplateSyntaxError
import urllib
import hashlib
import httplib
import json

from django.core.cache import cache


register = template.Library()


@register.filter(name='add_html_attr')
def add_html_attr(field, attr_dict):
    attrs = json.loads(attr_dict)
    return field.as_widget(attrs=attrs)


from django.forms import CheckboxInput


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__
