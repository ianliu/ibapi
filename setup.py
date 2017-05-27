#!/usr/bin/env python

from distutils.core import setup

setup(
    name='ibapi',
    version='0.1.0',
    description='Python library for interfacing with internet banking websites',
    packages=['ibapi'],
    install_requires=[
        'requests',
        'selenium',
        'lxml',
    ],
)
