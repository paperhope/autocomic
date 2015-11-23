#!/usr/bin/env python

from distutils.core import setup

setup(name='Autocomicftp',
      version='0.1',
      description='Flask app for autocomic',
      author='Håvard Futsæter',
      author_email='futsaeter@gmail.com',
      packages=['autocomicftp'],
      install_requires = [
          "requests",
          ]
          
     )
