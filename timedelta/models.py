"""
This is in the models.py file so I can run doctests on it!
"""

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
    d = re.match(r'((?P<days>\d+) days )?(?P<hours>\d+):'
                 r'(?P<minutes>\d+):(?P<seconds>\d+)',
                 str(string))
    if d: 
        d = d.groupdict(0)
    else:
        # TODO: Test this, and make it prettier...
        d = re.match(
                     r'((?P<weeks>\d+)\W*w((ee)?k(s)?)(,)?\W*)?'
                     r'((?P<days>\d+)\W*d(ay(s)?)?(,)?\W*)?'
                     r'((?P<hours>\d+)\W*h(ou)?r(s)?(,)?\W*)?'
                     r'((?P<minutes>\d+)\W*m(in(ute)?)?(s)?(,)?\W*)?'
                     r'((?P<seconds>\d+)\W*s(ec(ond)?(s)?)?)?\W*',
                     str(string)).groupdict()
    return datetime.timedelta(**dict(( (k, int(v)) for k,v in d.items() 
        if v is not None )))