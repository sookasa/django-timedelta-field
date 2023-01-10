from django import forms
from django.utils.translation import gettext_lazy as _

import datetime
from collections import defaultdict

from .widgets import TimedeltaWidget
from .helpers import parse

class TimedeltaFormField(forms.Field):
    
    default_error_messages = {
        'invalid':_('Enter a valid time span: e.g. "3 days, 4 hours, 2 minutes"')
    }
    
    def __init__(self, *args, **kwargs):
        defaults = {'widget':TimedeltaWidget}
        defaults.update(kwargs)
        super(TimedeltaFormField, self).__init__(*args, **defaults)
        
    def clean(self, value):
        """
        This doesn't really need to be here: it should be tested in
        parse()...
        
        >>> t = TimedeltaFormField()
        >>> t.clean('1 day')
        datetime.timedelta(days=1)
        >>> t.clean('1 day, 0:00:00')
        datetime.timedelta(days=1)
        >>> t.clean('1 day, 8:42:42.342')
        datetime.timedelta(days=1, seconds=31362, microseconds=342000)
        >>> t.clean('3 days, 8:42:42.342161')
        datetime.timedelta(days=3, seconds=31362, microseconds=342161)
        >>> try:
        ...  t.clean('3 days, 8:42:42.3.42161')
        ... except forms.ValidationError as arg:
        ...  print(arg.messages[0])
        Enter a valid time span: e.g. "3 days, 4 hours, 2 minutes"
        >>> t.clean('5 day, 8:42:42')
        datetime.timedelta(days=5, seconds=31362)
        >>> t.clean('1 days')
        datetime.timedelta(days=1)
        >>> t.clean('1 second')
        datetime.timedelta(seconds=1)
        >>> t.clean('1 sec')
        datetime.timedelta(seconds=1)
        >>> t.clean('10 seconds')
        datetime.timedelta(seconds=10)
        >>> t.clean('30 seconds')
        datetime.timedelta(seconds=30)
        >>> t.clean('1 minute, 30 seconds')
        datetime.timedelta(seconds=90)
        >>> t.clean('2.5 minutes')
        datetime.timedelta(seconds=150)
        >>> t.clean('2 minutes, 30 seconds')
        datetime.timedelta(seconds=150)
        >>> t.clean('.5 hours')
        datetime.timedelta(seconds=1800)
        >>> t.clean('30 minutes')
        datetime.timedelta(seconds=1800)
        >>> t.clean('1 hour')
        datetime.timedelta(seconds=3600)
        >>> t.clean('5.5 hours')
        datetime.timedelta(seconds=19800)
        >>> t.clean('1 day, 1 hour, 30 mins')
        datetime.timedelta(days=1, seconds=5400)
        >>> t.clean('8 min')
        datetime.timedelta(seconds=480)
        >>> t.clean('3 days, 12 hours')
        datetime.timedelta(days=3, seconds=43200)
        >>> t.clean('3.5 day')
        datetime.timedelta(days=3, seconds=43200)
        >>> t.clean('1 week')
        datetime.timedelta(days=7)
        >>> t.clean('2 weeks, 2 days')
        datetime.timedelta(days=16)
        >>> try:
        ...  t.clean('2 we\xe8k, 2 days')
        ... except forms.ValidationError as arg:
        ...  print(arg.messages[0])
        Enter a valid time span: e.g. "3 days, 4 hours, 2 minutes"
        """
        
        super(TimedeltaFormField, self).clean(value)
        if value == '' and not self.required:
            return ''
        try:
            return parse(value)
        except TypeError:
            raise forms.ValidationError(self.error_messages['invalid'])

class TimedeltaChoicesField(TimedeltaFormField):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        defaults = {'widget':forms.Select(choices=choices)}
        defaults.update(kwargs)
        super(TimedeltaChoicesField, self).__init__(*args, **defaults)
