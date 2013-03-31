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

from arcospyu.mypopen import MyPopen
from arcospyu.dprint import iprint, dprint, eprint
from time import sleep
import signal

class PManager(object):
    def __init__(self, processes_args=[]):
        self.processes_args=processes_args
        self.processes=[]

    def start(self):
        for process_args in self.processes_args:
            dprint("Starting process: ", process_args[0])
            self.processes.append(MyPopen(process_args))
            self.processes[-1].args=process_args
            sleep(1)

    def monitor(self):
        stop=False
        while not stop:
            for process in self.processes:
                process.poll()
                if process.returncode != None:
                    eprint("Process: ", process.args[0], " died! Closing all processes")
                    stop=True
            sleep(0.5)
            dprint("Looping")
        if stop:
            self.stop()

    def stop(self, sec=10):
        iprint("Sending signal ", signal.SIGTERM, " to subprocesses")
        [process.send_signal2(signal.SIGTERM) for process in self.processes]
        iprint("Waiting processes to terminate")
        for process in self.processes:
            process.wait_and_kill(sec)
            iprint("Process: ", process.args[0], " terminated")
        iprint("All processes terminated!")
