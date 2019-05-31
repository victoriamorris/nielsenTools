#!/usr/bin/env python
# -*- coding: utf8 -*-

"""setup.py file for nielsenTools."""

# Import required modules
from distutils.core import setup
import py2exe

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'

# Version
version = '1.0.0'

# Long description
long_description = ''

# List requirements.
# All other requirements should all be contained in the standard library
requirements = [
    'py2exe',
    'regex',
    'pyperclip',
    'sqlite3',
    'csv',
]

# Setup
setup(
    console=[
        'bin/nielsen2marc_products.py',
        'bin/nielsen2marc_organisations.py',
        'bin/nielsen_isbn_analysis.py',
        'bin/nielsen2marc_clusters.py',
    ],
    zipfile=None,
    options={
        'py2exe': {
            'bundle_files': 0,
        }
    },
    name='nielsenTools',
    version=version,
    author='Victoria Morris',
    url='',
    license='MIT',
    description='Tools for working with files from Nielsen.',
    long_description=long_description,
    packages=['nielsenTools'],
    scripts=[
        'bin/nielsen2marc_products.py',
        'bin/nielsen2marc_organisations.py',
        'bin/nielsen_isbn_analysis.py',
        'bin/nielsen2marc_clusters.py',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python'
    ],
    requires=requirements
)
