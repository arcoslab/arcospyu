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
