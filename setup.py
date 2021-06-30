#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages


setup(name='hwtBuildsystem',
      version='0.1',
      description='buildsystem for for HWToolkit (fpga devel. tools)',
      url='https://github.com/Nic30/hwtBuildsystem',
      author='Michal Orsak',
      author_email='michal.o.socials@gmail.com',
      install_requires=[
        'pexpect', # CLI app io
        'hwt', # core library of HWToolkit
      ],
      license='MIT',
      packages = find_packages(),
      zip_safe=False)
