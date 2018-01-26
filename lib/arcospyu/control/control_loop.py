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
import time


class Controlloop(object):
    def __init__(self, freq):
        self.freq = freq
        self.period = 1. / freq
        self.cont = True
        self.count = 0
        self.localtime = 0.
        self.time_scale = 1.0

    def set_time_scale(self, scale):
        self.time_scale = scale

    def set_params(self, params):
        """Put the variables used by process here"""
        pass

    def process(self):
        """Do stuff, set cont to False to stop processing"""
        pass

    def end(self):
        """Do final stuff"""
        pass

    def loop(self, **params):
        self.set_params(params)
        init_time = time.time() * self.time_scale
        self.next_time = init_time
        while self.cont:
            self.process()
            self.count += 1
            self.localtime += self.period
            self.next_time = self.next_time + 1. / self.freq
            wait_time = self.next_time - time.time() * self.time_scale
            if wait_time > 0.:
                time.sleep(wait_time)
            else:
                pass
                print('Warning: Cycle too slow', -wait_time, 'Seconds late')
        self.end()
