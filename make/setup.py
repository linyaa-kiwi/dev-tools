#!/usr/bin/env python3

import glob
import os
from distutils.core import setup

setup(
    name = 'chadv-dev-tools',
    version = '0.1',
    author = 'Chad Versace',
    author_email = 'chad@kiwitree.net',
    url = 'http://github.com/chadversary/chadv-dev-tools',
    packages = ['chadv_dev_tools'],
    package_dir = {'': 'lib'},
)
