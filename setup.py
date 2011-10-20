from distutils.core import setup

setup(
    name = "django-timedeltafield",
    version = "0.5",
    description = "TimedeltaField for django models",
    url = "http://hg.schinckel.net/django-timedelta-field/",
    author = "Matthew Schinckel",
    author_email = "matt@schinckel.net",
    packages = [
        "timedelta",
    ],
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
)
