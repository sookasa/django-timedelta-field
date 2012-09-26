from django import template
register = template.Library()

# Don't really like using relative imports, but no choice here!
from ..helpers import nice_repr, iso8601_repr, total_seconds as _total_seconds

@register.filter(name='timedelta')
def timedelta(value, display="long"):
    return nice_repr(value, display)

@register.filter(name='iso8601')
def iso8601(value):
    return iso8601_repr(value)

@register.filter(name='total_seconds')
def total_seconds(value):
    return _total_seconds(value)

@register.filter(name='total_seconds_sort')
def total_seconds(value, places=10):
    return ("%0" + str(places) + "i") % _total_seconds(value)

