#!/usr/bin/env python3

"""
Copyright 2018 Nick Everett
All Rights Reserved.
Licensed under the GNU General Public License v3.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at
https://www.gnu.org/licenses/gpl-3.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""


import io
import os
import ltocheck
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.rst')

setup(
    name='ltocheck',
    version=ltocheck.__version__,
    url='https://github.com/nickever/ltocheck',
    license='GNU General Public License v3.0',
    author='Nick Everett',
    author_email='njeverett@gmail.com',
    description='Command line interface tool to compare a master csv with an LTO csv',
    long_description=long_description,
    keywords='ltocheck csv lto tape compare',
    py_modules=['ltocheck'],
    entry_points={
        'console_scripts': [
            'ltocheck=ltocheck:main',
        ],
    },
    platforms='macOS',
    install_requires=['google-api-python-client'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'License :: OSI Approved :: '
        'GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Networking'])