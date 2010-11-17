from django.db import models

import datetime
from collections import defaultdict
import re

from helpers import nice_repr, parse
from forms import TimedeltaFormField

SECS_PER_DAY = 60*60*24

# TODO: Figure out why django admin thinks fields of this type have changed every time an object is saved.

class TimedeltaField(models.Field):
    """
    Store a datetime.timedelta as an integer.
    
    We don't subclass models.IntegerField, as that would then use the
    AdminIntegerWidget or whatever in the admin, and we want to use
    our custom widget.
    """
    __metaclass__ = models.SubfieldBase
    _south_introspects = True
    
    description = "A datetime.timedelta object"
    
    def to_python(self, value):
        if (value is None) or isinstance(value, datetime.timedelta):
            return value
        if isinstance(value, int):
            return datetime.timedelta(seconds=value)
        if value == "":
            return datetime.timedelta(0)
        return parse(value)
    
    def get_prep_value(self, value):
        if (value is None) or isinstance(value, (str, unicode)):
            return value
        return str(value).replace(',', '')
        
    def get_db_prep_value(self, value, connection, prepared=None):
        return self.get_prep_value(value)
        
    def formfield(self, *args, **kwargs):
        defaults = {'form_class':TimedeltaFormField}
        defaults.update(kwargs)
        return super(TimedeltaField, self).formfield(*args, **defaults)
    
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
        """
        Postgres allows us to store stuff as an INTERVAL type. This is 
        useful, and we can then use database logic to do tests.
        """
        if connection.settings_dict['ENGINE'] == "django.db.backends.postgresql_psycopg2":
            return 'interval'
        else:
            return 'char(20)'

