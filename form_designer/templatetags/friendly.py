from django import template
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import yesno

# Returns a more "human-friendly" representation of value than repr()
def friendly(value): 
    if type(value) is QuerySet:
        qs = value
        value = []
        for object in qs:
            value.append(object.__unicode__())
    if type(value) is list:
        value = ", ".join(value)
    if type(value) is bool:
        value = yesno(value, u"%s,%s" % (_('yes'), _('no')),)
    return value

register = template.Library()
register.filter(friendly)