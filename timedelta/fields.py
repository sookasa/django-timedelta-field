from django.db import models
from django.core.exceptions import ValidationError

from collections import defaultdict
import datetime

from .helpers import parse
from .forms import TimedeltaFormField

# TODO: Figure out why django admin thinks fields of this type have changed every time an object is saved.

class TimedeltaField(models.Field):
    """
    Store a datetime.timedelta as an INTERVAL in postgres, or a 
    CHAR(20) in other database backends.
    """
    _south_introspects = True
    
    description = "A datetime.timedelta object"
    
    def __init__(self, *args, **kwargs):
        self._min_value = kwargs.pop('min_value', None)
        self._max_value = kwargs.pop('max_value', None)
        super(TimedeltaField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        if (value is None) or isinstance(value, datetime.timedelta):
            return value
        if isinstance(value, int):
            return datetime.timedelta(seconds=value)
        if value == "":
            if self.null:
                return None
            else:
                return datetime.timedelta(0)
        return parse(value)
    
    def get_prep_value(self, value):
        if self.null and value == "":
            return None
        if (value is None) or isinstance(value, str):
            return value
        return str(value).replace(',', '')
        
    def get_db_prep_value(self, value, connection=None, prepared=None):
        return self.get_prep_value(value)
        
    def formfield(self, *args, **kwargs):
        defaults = {'form_class':TimedeltaFormField}
        defaults.update(kwargs)
        return super(TimedeltaField, self).formfield(*args, **defaults)
    
    def validate(self, value, model_instance):
        super(TimedeltaField, self).validate(value, model_instance)
        if self._min_value is not None:
            if self._min_value > value:
                raise ValidationError('Less than minimum allowed value')
        if self._max_value is not None:
            if self._max_value < value:
                raise ValidationError('More than maximum allowed value')
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return unicode(value)
    
    def get_default(self):
        """
        Needed to rewrite this, as the parent class turns this value into a
        unicode string. That sux pretty deep.
        """
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.get_prep_value(self.default)
        if not self.empty_strings_allowed or (self.null):
            return None
        return ""
        
    def db_type(self, connection):
        return 'interval'

    def deconstruct(self):
        name, path, args, kwargs = super(TimedeltaField, self).deconstruct()
        if self._min_value is not None:
            kwargs['min_value'] = self._min_value
        if self._max_value is not None:
            kwargs['max_value'] = self._max_value
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name):
        super(TimedeltaField, self).contribute_to_class(cls, name)
        setattr(cls, name, CastOnAssignDescriptor(self))


class CastOnAssignDescriptor(object):
    """
    A property descriptor which ensures that `field.to_python()` is called on _every_ assignment to the field.
    This used to be provided by the `django.db.models.subclassing.Creator` class, which in turn
    was used by the deprecated-in-Django-1.10 `SubfieldBase` class, hence the reimplementation here.
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)
