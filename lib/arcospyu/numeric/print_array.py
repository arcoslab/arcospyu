# -*- coding: utf-8 -*-
# Copyright (c) 2009 Technische Universitaet Muenchen, Informatik Lehrstuhl IX.
# Author: Federico Ruiz-Ugalde
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


def print_array(name, data, newline=True, total_digits=4, decimals=3):
    pattern = '%' + str(total_digits) + '.' + str(decimals) + 'f'
    print name, '[',
    for i in data:
        print(pattern % i),
    if newline:
        print ']'
    else:
        print ']',
