from django import template

# Returns a more "human-friendly" representation of value than repr()
def friendly(value): 
    if type(value) is list:
        value = ", ".join(value)
    return value

register = template.Library()
register.filter(friendly)