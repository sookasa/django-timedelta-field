__version__ = "0.5.2"

try:
    from fields import TimedeltaField
    from helpers import divide, multiply, modulo, parse, nice_repr, percentage, decimal_percentage
except ImportError:
    pass