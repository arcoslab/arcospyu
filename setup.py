#!/usr/bin/env python

from distutils.core import setup


setup(name='arcospyu',
      version='1.0',
      description='Arcoslab python utils',
      author='Federico Ruiz Ugalde',
      author_email='memeruiz@gmail.com',
      url='http://www.arcoslab.org/',
      packages=['arcospyu', 'arcospyu.computer_graphics', 'arcospyu.config_parser', 'arcospyu.control', 'arcospyu.dprint', 'arcospyu.kdl_helpers', 'arcospyu.mypopen', 'arcospyu.numeric', 'arcospyu.print_colors', 'arcospyu.rawkey', 'arcospyu.pmanager', 'arcospyu.lafik', 'arcospyu.yarp_tools'],
      scripts=['arcospyu/yarp_tools/bar_vis']
     )
