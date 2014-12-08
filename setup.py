#!/usr/bin/env python

from distutils.core import setup

setup(name='Kivy3',
      version='0.1',
      description='Kivy extensions for 3D graphics',
      author='Niko Skrypnik',
      author_email='nskrypnik@gmail.com',
      packages=['kivy3', 'kivy3.core', 'kivy3.extras', 'kivy3.loaders', 'kivy3.math', 'kivy3.objects', 'kivy3.scenes'],
      requires=['kivy', ]
)
