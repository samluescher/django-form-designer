from django.conf import settings
from form_designer import defaults

def get(key):
    if hasattr(settings, key):
        return getattr(settings, key)
    else:
        return getattr(defaults, key)
