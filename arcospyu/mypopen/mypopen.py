from subprocess import Popen
from time import time, sleep
import signal
from arcospyu.dprint import Dprint
d=Dprint()
dprint=d.dprint
import sys
#sys.path.append("../python/print_colors")
from arcospyu.print_colors import Pcolors as c

class MyPopen(Popen):
    def __init__(self, cargs, *args):
        Popen.__init__(self, cargs, *args)
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
            dprint(self.args[0]+c.FAIL+" TERM signal didn't worked, escalating to KILL"+c.ENDC)
            self.send_signal(signal.SIGKILL)
