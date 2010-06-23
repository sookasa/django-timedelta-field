from distutils.core import setup

setup(
    name = "timedelta",
    version = "0.2",
    description = "TimedeltaField for django models",
    url = "http://bitbucket.org/schinckel/django-timedelta-field/",
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
