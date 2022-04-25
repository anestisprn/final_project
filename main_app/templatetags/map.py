from django import template

register = template.Library()

@register.filter
def map(value):
    return value.replace(",","/")