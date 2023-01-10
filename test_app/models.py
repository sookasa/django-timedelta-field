
from django.db import models
from timedelta_field.fields import TimedeltaField
import datetime


class MinMaxTestModel(models.Model):
    min = TimedeltaField(min_value=datetime.timedelta(1))
    max = TimedeltaField(max_value=datetime.timedelta(1))
    minmax = TimedeltaField(min_value=datetime.timedelta(1), max_value=datetime.timedelta(7))
