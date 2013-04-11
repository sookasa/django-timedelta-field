from unittest import TestCase
import datetime
import doctest

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import six

from .fields import TimedeltaField
import timedelta.helpers
import timedelta.forms
import timedelta.widgets

class MinMaxTestModel(models.Model):
    min = TimedeltaField(min_value=datetime.timedelta(1))
    max = TimedeltaField(max_value=datetime.timedelta(1))
    minmax = TimedeltaField(min_value=datetime.timedelta(1), max_value=datetime.timedelta(7))
    
class TimedeltaModelFieldTest(TestCase):
    def test_validate(self):
        test = MinMaxTestModel(
            min=datetime.timedelta(1),
            max=datetime.timedelta(1),
            minmax=datetime.timedelta(1)
        )
        test.full_clean() # This should have met validation requirements.
        
        test.min = datetime.timedelta(hours=23)
        self.assertRaises(ValidationError, test.full_clean)
        
        test.min = datetime.timedelta(hours=25)
        test.full_clean()
        
        test.max = datetime.timedelta(11)
        self.assertRaises(ValidationError, test.full_clean)
        
        test.max = datetime.timedelta(hours=20)
        test.full_clean()
        
        test.minmax = datetime.timedelta(0)
        self.assertRaises(ValidationError, test.full_clean)
        test.minmax = datetime.timedelta(22)
        self.assertRaises(ValidationError, test.full_clean)
        test.minmax = datetime.timedelta(6, hours=23, minutes=59, seconds=59)
        test.full_clean()
    
    def test_load_from_db(self):
        obj = MinMaxTestModel.objects.create(min='2 days', max='2 minutes', minmax='3 days')
        self.assertEquals(datetime.timedelta(2), obj.min)
        self.assertEquals(datetime.timedelta(0, 120), obj.max)
        self.assertEquals(datetime.timedelta(3), obj.minmax)
        
        obj = MinMaxTestModel.objects.get()
        self.assertEquals(datetime.timedelta(2), obj.min)
        self.assertEquals(datetime.timedelta(0, 120), obj.max)
        self.assertEquals(datetime.timedelta(3), obj.minmax)

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(timedelta.helpers))
    tests.addTests(doctest.DocTestSuite(timedelta.forms))
    return tests
