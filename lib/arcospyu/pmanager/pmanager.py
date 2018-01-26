#!/usr/bin/env python
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

from arcospyu.mypopen import MyPopen
from arcospyu.dprint import iprint, dprint, eprint
from time import sleep
import signal
import os


def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


class PManager(object):
    def __init__(self, processes_args=[]):
        self.processes_args = processes_args
        self.processes = []
        self.processes_name_pos = []

    def start(self):
        for process_args in self.processes_args:
            filename = which(process_args[0])
            if filename and os.path.exists(filename) and os.access(filename,
                                                                   os.X_OK):
                dprint('Starting process: ', process_args[0])
                self.processes.append(MyPopen([filename] + process_args[1:]))
                self.processes[-1].args = process_args
            else:
                eprint(
                    'Executable', process_args[0],
                    ' not found, not starting process')
            # sleep(3)

    def monitor(self):
        stop = False
        while not stop:
            for process in self.processes:
                process.poll()
                if process.returncode is not None:
                    eprint(
                        'Process: ', process.args[0],
                        ' died! Closing all processes')
                    stop = True
            sleep(0.5)
            # dprint('Looping')
        if stop:
            self.stop()

    def stop(self, sec=10):
        iprint('Sending signal ', signal.SIGTERM, ' to subprocesses')
        [process.send_signal2(signal.SIGTERM) for process in self.processes]
        iprint('Waiting processes to terminate')
        for process in self.processes:
            process.wait_and_kill(sec)
            iprint('Process: ', process.args[0], ' terminated')
        iprint('All processes terminated!')
