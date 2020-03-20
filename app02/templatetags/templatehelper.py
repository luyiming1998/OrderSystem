from django import template
register=template.Library()
@register.filter
def mult(value, value2):
    return round((float(value) * value2), 2)