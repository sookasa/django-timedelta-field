from unittest import TestCase
import datetime
from forms import TimedeltaFormField
from widgets import TimedeltaWidget

class TimedeltaWidgetTest(TestCase):
    def test_render(self):
        """
        >>> t = TimedeltaWidget()
        >>> t.render('', datetime.timedelta(days=1), {})
        u'<input type="text" name="" value="1 day" />'
        >>> t.render('', datetime.timedelta(days=0), {})
        u'<input type="text" name="" />'
        >>> t.render('', datetime.timedelta(seconds=1), {})
        u'<input type="text" name="" value="1 second" />'
        >>> t.render('', datetime.timedelta(seconds=10), {})
        u'<input type="text" name="" value="10 seconds" />'
        >>> t.render('', datetime.timedelta(seconds=30), {})
        u'<input type="text" name="" value="30 seconds" />'
        >>> t.render('', datetime.timedelta(seconds=60), {})
        u'<input type="text" name="" value="1 minute" />'
        >>> t.render('', datetime.timedelta(seconds=150), {})
        u'<input type="text" name="" value="2 minutes, 30 seconds" />'
        >>> t.render('', datetime.timedelta(seconds=1800), {})
        u'<input type="text" name="" value="30 minutes" />'
        >>> t.render('', datetime.timedelta(seconds=3600), {})
        u'<input type="text" name="" value="1 hour" />'
        >>> t.render('', datetime.timedelta(seconds=3601), {})
        u'<input type="text" name="" value="1 hour, 1 second" />'
        >>> t.render('', datetime.timedelta(seconds=19800), {})
        u'<input type="text" name="" value="5 hours, 30 minutes" />'
        >>> t.render('', datetime.timedelta(seconds=91800), {})
        u'<input type="text" name="" value="1 day, 1 hour, 30 minutes" />'
        >>> t.render('', datetime.timedelta(seconds=302400), {})
        u'<input type="text" name="" value="3 days, 12 hours" />'
        """

class TimedeltaFormFieldTest(TestCase):
    def test_clean(self):
        """
        >>> t = TimedeltaFormField()
        >>> t.clean('1 day')
        datetime.timedelta(1)
        >>> t.clean('1 days')
        datetime.timedelta(1)
        >>> t.clean('1 second')
        datetime.timedelta(0, 1)
        >>> t.clean('1 sec')
        datetime.timedelta(0, 1)
        >>> t.clean('10 seconds')
        datetime.timedelta(0, 10)
        >>> t.clean('30 seconds')
        datetime.timedelta(0, 30)
        >>> t.clean('1 minute, 30 seconds')
        datetime.timedelta(0, 90)
        >>> t.clean('2.5 minutes')
        datetime.timedelta(0, 150)
        >>> t.clean('2 minutes, 30 seconds')
        datetime.timedelta(0, 150)
        >>> t.clean('.5 hours')
        datetime.timedelta(0, 1800)
        >>> t.clean('30 minutes')
        datetime.timedelta(0, 1800)
        >>> t.clean('1 hour')
        datetime.timedelta(0, 3600)
        >>> t.clean('5.5 hours')
        datetime.timedelta(0, 19800)
        >>> t.clean('1 day, 1 hour, 30 mins')
        datetime.timedelta(1, 5400)
        >>> t.clean('8 min')
        datetime.timedelta(0, 480)
        >>> t.clean('3 days, 12 hours')
        datetime.timedelta(3, 43200)
        >>> t.clean('3.5 day')
        datetime.timedelta(3, 43200)
        >>> t.clean('1 week')
        datetime.timedelta(7)
        >>> t.clean('2 weeks, 2 days')
        datetime.timedelta(16)
        """