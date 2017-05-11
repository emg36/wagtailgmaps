import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# all the real work has been done by springload https://github.com/springload/wagtailgmaps

setup(
    name='wagtailgmaps',
    version='0.3',
    packages=['wagtailgmaps'],
    include_package_data=True,
    license='BSD License',
    description='Google Maps widget for address fields in Wagtail',
    long_description=README,
    url='https://github.com/emg36/wagtailgmaps/',
    author='Jordi J. Tablada, Elliot G',
    author_email='jordi@springload.co.nz, elliot@make.nz',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['django-overextends'],
)
