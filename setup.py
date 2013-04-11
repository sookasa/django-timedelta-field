import os.path
from setuptools import setup

setup(
    name = "django-timedeltafield",
    version = open(os.path.join(os.path.dirname(__file__), 'timedelta', 'VERSION')).read().strip(),
    description = "TimedeltaField for django models",
    long_description = open("README").read(),
    url = "http://hg.schinckel.net/django-timedelta-field/",
    author = "Matthew Schinckel",
    author_email = "matt@schinckel.net",
    packages = [
        "timedelta",
        "timedelta.templatetags",
    ],
    package_data = {'timedelta': ['VERSION']},
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    test_suite='tests.main',
)
