#!/usr/bin/env python
# Copyright (c) 2013
# Author: Federico Ruiz-Ugalde <memeruiz at gmail.com>
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

from subprocess import Popen
from time import time, sleep
import signal
import arcospyu.dprint
from arcospyu.dprint import iprint, dprint, eprint
#from arcospyu.dprint import Dprint
#d=Dprint()
#dprint=d.dprint
import sys, os
from arcospyu.print_colors import Pcolors as c

def preexec(): # Don't forward signals.
    os.setpgrp()

class MyPopen(Popen):
    def __init__(self, cargs, *args):
        Popen.__init__(self, cargs, *args, preexec_fn = preexec)
        self.args = cargs

    def wait2(self,sec):
        self.poll()
        inittime=time()
        while self.returncode == None:
            self.poll()
            sleep(0.1)
            elapsed=time()-inittime
            if elapsed > sec:
                return()

    def wait_and_kill(self, sec):
        self.wait2(sec)
        if self.returncode == None:
            eprint(self.args[0]+" TERM signal didn't worked, escalating to KILL")
            self.send_signal(signal.SIGKILL)

    def term_wait_kill(self, sec):
        self.poll()
        if self.returncode == None:
            dprint("Sending signal ", signal.SIGTERM, " to subprocess ", self.args[0])
            self.send_signal(signal.SIGTERM)
            self.wait_and_kill(sec)

    def send_signal2(self, sig):
        self.poll()
        if self.returncode == None:
            dprint("Sending signal ", sig, " to subprocess ", self.args[0])
            self.send_signal(sig)
