#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Federico Ruiz Ugalde
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

from scipy.signal import iirfilter, lfilter, lfiltic
from numpy import array


class Filter_vector():
    def __init__(self, dim=3, order=2, freq=0.7, y=[], x=[]):
        self.dim = dim
        self.filters = []
        for i in xrange(dim):
            if len(y) > 0:
                self.filters.append(
                    Filter(order=order, freq=freq, y=y[i], x=x[i]))
            else:
                self.filters.append(Filter(order=order, freq=freq))

    def filter(self, data):
        return (
            array(
                [
                    self.filters[i].filter(array([data[i]]))[0]
                    for i in xrange(self.dim)
                ]))


class Filter():
    def __init__(self, order=2, freq=0.7, y=[], x=[]):
        self.b, self.a = iirfilter(order, freq, btype='lowpass')
        if len(y) > 0:
            print 'here'
            self.z = lfiltic(self.b, self.a, y)
        else:
            self.z = array([0.] * order)
        self.z = lfiltic(self.b, self.a, y, x=x)

    def filter(self, raw_data):
        print 'Raw', array(raw_data)
        y, self.z = lfilter(self.b, self.a, raw_data, zi=self.z, axis=0)
        return (y)
