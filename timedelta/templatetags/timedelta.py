from django import template
register = template.Library()

# Don't really like using relative imports, but no choice here!
from ..helpers import nice_repr

@register.filter(name='timedelta')
def timedelta(value, display="long"):
    return nice_repr(value, display)