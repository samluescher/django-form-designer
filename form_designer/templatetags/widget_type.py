from django import template
register = template.Library()

@register.filter('field_type')
def field_type(obj):
    return obj.__class__.__name__
