#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from os import path

from setuptools import setup, find_packages


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='hwtBuildsystem',
      version='0.1',
      description='buildsystem for for HWToolkit (hwt, the fpga devel. library)',
      long_description=long_description,
      url='https://github.com/Nic30/hwtBuildsystem',
      author='Michal Orsak',
      author_email='Nic30original@gmail.com',
      install_requires=[
        'pexpect', # CLI app io
        'hwt>=3.8', # core library of HWToolkit
      ],
      license='MIT',
      packages = find_packages(),
      zip_safe=False)
