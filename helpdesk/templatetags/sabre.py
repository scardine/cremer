from django import template
import re

register = template.Library()

@register.filter
def get_type(value):
    return value.__class__.__name__


@register.filter
def is_type(value, name):
    return value.__class__.__name__ == name

@register.filter
def mklabel(counter, name):
    return u"{0} #{1}".format(name, counter)

@register.filter
def humanize(label):
    return re.sub(r'(@*)([A-Z0-9]+)', r' \2', label)
