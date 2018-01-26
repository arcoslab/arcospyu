# -*- coding: utf-8 -*-
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

from __future__ import print_function
from arcospyu.print_colors import Pcolors as c
import inspect as ins


class Dprint(object):
    INFO = 0
    DEBUG = 1
    WARN = 2
    ERROR = 3
    CALL_LEVEL_FIRST_FILE = -1
    CALL_LEVEL_LAST_FILE = 2

    def __init__(self, level=INFO, longfilename=False):
        self.level = level
        self.longfilename = longfilename

    def set_level(self, level):
        self.level = level

    def pfile(self, call_level=CALL_LEVEL_FIRST_FILE):
        filename = ins.getfile(
            ins.getouterframes(ins.currentframe())[call_level][0])
        if not self.longfilename:
            return (filename.split('/')[-1])

    def iprint(self, *args):
        if self.level <= 0:
            print('[' + self.pfile() + ']', end=' ')
            for arg in args:
                print(arg, end=' ')
            print()

    def dprint(self, *args):
        if self.level <= 1:
            print(c.GREEN + '[' + self.pfile() + ']', end=' ')
            for arg in args:
                print(arg, end=' ')
            print(c.END)

    def dcprint(self, *args):
        if self.level <= 1:
            print(c.GREEN + '[' + self.pfile(
                call_level=self.CALL_LEVEL_LAST_FILE) + ']', end=' ')
            for arg in args:
                print(arg, end=' ')
            print(c.END)

    def wprint(self, *args):
        if self.level <= 2:
            print(c.YELLOW + '[' + self.pfile() + ']', end=' ')
            for arg in args:
                print(arg, end=' ')
            print(c.END)

    def eprint(self, *args):
        if self.level <= 3:
            print(c.RED + '[' + self.pfile() + ']', end=' ')
            for arg in args:
                print(arg, end=' ')
            print(c.END)
