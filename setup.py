#!/usr/bin/env python

from setuptools import setup

setup(name='Autocomic',
      version='0.1',
      description='Autocomic library',
      author='Håvard Futsæter',
      author_email='futsaeter@gmail.com',
      packages=['autocomic'],
      install_requires = [
          "requests",
          "pillow"
          ]
          
     )
