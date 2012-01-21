from django import template
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import yesno

register = template.Library()

# Returns a more "human-friendly" representation of value than repr()
def friendly(value, null_value=None): 
    if value is None and not (null_value is None):
        return null_value
    if type(value) is QuerySet:
        qs = value
        value = []        
        for object in qs:
            value.append(object.__unicode__())
    if type(value) is list:
        value = ", ".join(value)
    if type(value) is bool:
        value = yesno(value, u"%s,%s" % (_('yes'), _('no')),)
    if hasattr(value, 'url'):
        value = value.url
    if not isinstance(value, basestring):
        value = unicode(value)
    return value

register.filter(friendly)