#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='duration',
    version='1.1.0',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    license='BSD License',
    description='python time duration conversion module',
    long_description=README,
    url='https://github.com/paramono/duration',
    author='Alexander Paramonov',
    author_email='alex@paramono.com',
    classifiers=[
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
