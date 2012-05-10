import os

__version__ = open(os.path.join(os.path.dirname(__file__), "VERSION")).read().strip()

try:
    from fields import TimedeltaField
    from helpers import (
        divide, multiply, modulo, 
        parse, nice_repr, 
        percentage, decimal_percentage,
        total_seconds
    )
except ImportError:
    pass