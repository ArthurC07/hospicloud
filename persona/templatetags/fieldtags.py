# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='field_type')
def field_type(value):
    return value.field.__class__.__name__


@register.filter(name='widget_type')
def widget_type(value):
    return value.field.widget.__class__.__name__
