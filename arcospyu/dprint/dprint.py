#!/usr/bin/env python
# Copyright (c) 2013 Federico Ruiz-Ugalde
# Author: Federico Ruiz Ugalde <memeruiz at gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

class Dprint(object):
    INFO=0
    DEBUG=1
    WARN=2
    ERROR=3

    def __init__(self, level=INFO):
        self.level=level

    def set_level(self, level):
        self.level=level

    def iprint(self, *args):
        if self.level<=0:
            print "["+__file__+"]",
            for arg in args:
                print arg,
            print

    def dprint(self, *args):
        if self.level<=1:
            print "["+__file__+"]",
            for arg in args:
                print arg,
            print

    def wprint(self, *args):
        if self.level<=2:
            print "["+__file__+"]",
            for arg in args:
                print arg,
            print

    def eprint(self, *args):
        if self.level<=3:
            print "["+__file__+"]",
            for arg in args:
                print arg,
            print
