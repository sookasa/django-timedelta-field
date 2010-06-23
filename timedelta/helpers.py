
import re
import datetime

def nice_repr(timedelta, display="long"):
    """
    Turns a datetime.timedelta object into a nice string repr.
    
    display can be "minimal", "short" or "long" [default].
    
    >>> from datetime import timedelta as td
    >>> nice_repr(td(days=1, hours=2, minutes=3, seconds=4))
    '1 day, 2 hours, 3 minutes, 4 seconds'
    >>> nice_repr(td(days=1, seconds=1), "minimal")
    '1d, 1s'
    """
    
    result = ""
    
    weeks = timedelta.days / 7
    days = timedelta.days % 7
    hours = timedelta.seconds / 3600
    minutes = (timedelta.seconds % 3600) / 60
    seconds = timedelta.seconds % 60
    
    if display == 'minimal':
        words = ["w", "d", "h", "m", "s"]
    elif display == 'short':
        words = [" wks", " days", " hrs", " min", " sec"]
    else:
        words = [" weeks", " days", " hours", " minutes", " seconds"]
    
    values = [weeks, days, hours, minutes, seconds]
    
    for i in range(4):
        if values[i]:
            if values[i] == 1 and len(words[i]) > 1:
                result += "%i%s, " % (values[i], words[i].rstrip('s'))
            else:
                result += "%i%s, " % (values[i], words[i])
    
    return result[:-2]

def parse(string):
    """
    Parse a string into a timedelta object.
    """
    # This is the format we sometimes get from Postgres.
    d = re.match(r'((?P<days>\d+) days )?(?P<hours>\d+):'
                 r'(?P<minutes>\d+):(?P<seconds>\d+)',
                 str(string))
    if d: 
        d = d.groupdict(0)
    else:
        # This is the more flexible format
        d = re.match(
                     r'^((?P<weeks>\d+)\W*w((ee)?k(s)?)(,)?\W*)?'
                     r'((?P<days>\d+)\W*d(ay(s)?)?(,)?\W*)?'
                     r'((?P<hours>\d+)\W*h(ou)?r(s)?(,)?\W*)?'
                     r'((?P<minutes>\d+)\W*m(in(ute)?)?(s)?(,)?\W*)?'
                     r'((?P<seconds>\d+)\W*s(ec(ond)?(s)?)?)?\W*$',
                     str(string)).groupdict()
    
    if not d:
        raise ValueError("%s is not a valid time interval" % string)
    
    return datetime.timedelta(**dict(( (k, int(v)) for k,v in d.items() 
        if v is not None )))


def divide(obj1, obj2, float=False):
    """
    Allows for the division of timedeltas by other timedeltas.
    
    >>> divide(datetime.timedelta(1), datetime.timedelta(hours=6))
    4
    >>> divide(datetime.timedelta(2), datetime.timedelta(3))
    0
    """
    assert isinstance(obj1, datetime.timedelta)
    assert isinstance(obj2, datetime.timedelta)
    
    sec1 = obj1.days * 86400 + obj1.seconds
    sec2 = obj2.days * 86400 + obj2.seconds
    if float:
        sec1 *= 1.0
    return sec1 / sec2

def percentage(obj1, obj2):
    """
    >>> percentage(datetime.timedelta(2), datetime.timedelta(4))
    50.0
    """
    return divide(obj1 * 100, obj2, float=True)

def multiply(obj, val):
    """
    Allows for the multiplication of timedeltas by float values.
    """
    
    assert isinstance(obj, datetime.timedelta)
    
    sec = obj.days * 86400 + obj.seconds
    sec *= val
    return datetime.timedelta(seconds=sec)


def round_to_nearest(obj, timedelta):
    """
    The obj is rounded to the nearest whole number of timedeltas.
    
    obj can be a timedelta, datetime or time object.
    
    >>> td = datetime.timedelta(minutes=30)
    >>> round_to_nearest(datetime.timedelta(minutes=0), td)
    datetime.timedelta(0)
    >>> round_to_nearest(datetime.timedelta(minutes=14), td)
    datetime.timedelta(0)
    >>> round_to_nearest(datetime.timedelta(minutes=15), td)
    datetime.timedelta(0, 1800)
    >>> round_to_nearest(datetime.timedelta(minutes=29), td)
    datetime.timedelta(0, 1800)
    >>> round_to_nearest(datetime.timedelta(minutes=30), td)
    datetime.timedelta(0, 1800)
    >>> round_to_nearest(datetime.timedelta(minutes=42), td)
    datetime.timedelta(0, 1800)
    >>> round_to_nearest(datetime.timedelta(hours=7, minutes=22), td)
    datetime.timedelta(0, 27000)
    
    >>> td = datetime.timedelta(minutes=15)
    >>> round_to_nearest(datetime.timedelta(minutes=0), td)
    datetime.timedelta(0)
    >>> round_to_nearest(datetime.timedelta(minutes=14), td)
    datetime.timedelta(0, 900)
    >>> round_to_nearest(datetime.timedelta(minutes=15), td)
    datetime.timedelta(0, 900)
    >>> round_to_nearest(datetime.timedelta(minutes=29), td)
    datetime.timedelta(0, 1800)
    >>> round_to_nearest(datetime.timedelta(minutes=30), td)
    datetime.timedelta(0, 1800)
    >>> round_to_nearest(datetime.timedelta(minutes=42), td)
    datetime.timedelta(0, 2700)
    >>> round_to_nearest(datetime.timedelta(hours=7, minutes=22), td)
    datetime.timedelta(0, 26100)
    
    >>> td = datetime.timedelta(minutes=30)
    >>> round_to_nearest(datetime.datetime(2010,1,1,9,22), td)
    datetime.datetime(2010, 1, 1, 9, 30)
    >>> round_to_nearest(datetime.datetime(2010,1,1,9,32), td)
    datetime.datetime(2010, 1, 1, 9, 30)
    >>> round_to_nearest(datetime.datetime(2010,1,1,9,42), td)
    datetime.datetime(2010, 1, 1, 9, 30)
    
    >>> round_to_nearest(datetime.time(0,20), td)
    datetime.time(0, 30)
    """
    
    time_only = False
    if isinstance(obj, datetime.timedelta):
        counter = datetime.timedelta(0)
    elif isinstance(obj, datetime.datetime):
        counter = datetime.datetime.combine(obj.date(), datetime.time(0, tzinfo=obj.tzinfo))
    elif isinstance(obj, datetime.time):
        counter = datetime.datetime.combine(datetime.date.today(obj.tzinfo), datetime.time(0, tzinfo=obj.tzinfo))
        obj = datetime.datetime.combine(datetime.date.today(), obj)
        time_only = True
    
    diff = abs(obj - counter)
    while counter < obj:
        old_diff = diff
        counter += timedelta
        diff = abs(obj - counter)
    
    if counter == obj:
        result = obj
    elif diff <= old_diff:
        result = counter
    else:
        result = counter - timedelta
    
    if time_only:
        return result.time()
    else:
        return result

