#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def read(filename):
    """
    Read a file relative to setup.py location.
    """
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, filename)) as fd:
        return fd.read()


def find_version(filename):
    """
    Find package version in file.
    """
    import re
    content = read(filename)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def find_requirements(filename):
    """
    Find requirements in file.
    """
    import string
    content = read(filename)
    requirements = []
    for line in content.splitlines():
        line = line.strip()
        if line and line[:1] in string.ascii_letters:
            requirements.append(line)
    return requirements


setup(
    name='arcospyu',
    version=find_version('lib/arcospyu/__init__.py'),
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    scripts=['arcospyu/yarp_tools/bar_vis'],

    # Dependencies
    install_requires=find_requirements('requirements.txt'),

    # Metadata
    author='Federico Ruiz Ugalde',
    author_email='memeruiz@gmail.com',
    description='Arcoslab python utils',
    # long_description=read('README.rst'),
    url='http://www.arcoslab.org/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: GNU GPL v3',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ])
