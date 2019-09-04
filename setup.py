#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import find_packages
from setuptools import setup

setup(
    name='APIAutomation',
    version='0.2',
    packages=find_packages(),
    description='Automate API',
    long_description='Automate API',
    url='http://localhost',
    license='MIT',
    author='Anupam Mundale',
    author_email='mundleanupam@gmail.com',
    install_requires=['requests', 'pyyaml'],
    extras_require={
        ':python_version == "2.7"': ['future'],
    },
    tests_require=['pytest', 'mock', 'vcrpy'],
    keywords=['lyft', 'api', 'sdk', 'rides', 'library'],
)