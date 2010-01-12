from django import template
from django.db.models.query import QuerySet

# Returns a more "human-friendly" representation of value than repr()
def friendly(value): 
    if type(value) is QuerySet:
        qs = value
        value = []
        for object in qs:
            value.append(object.__unicode__())
    if type(value) is list:
        value = ", ".join(value)
    return value

register = template.Library()
register.filter(friendly)