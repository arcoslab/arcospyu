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

import sys, termios, os,select, time

class Raw_key():
    def __init__(self):
        self.fd=sys.stdin.fileno()
        self.old=termios.tcgetattr(self.fd)
        new=termios.tcgetattr(self.fd)
        new[3]= new[3] & ~termios.ICANON & ~termios.ECHO
        new[6][termios.VMIN]=0
        new[6][termios.VTIME]=0
        termios.tcsetattr(self.fd,termios.TCSANOW,new)


    def new_data(self,timeout):
        #return select.select([sys.stdin],[],[],0)==([sys.stdin],[],[])
        return select.select([self.fd],[],[],timeout)==([self.fd],[],[])

    def get_chars(self,timeout=0):
        out=[]
        if self.new_data(timeout):
            out.append(os.read(self.fd,1))
        while self.new_data(0.0):
            out.append(os.read(self.fd,1))
            
        return(out)

    def get_num_chars(self,timeout=0):
        return(map(ord,self.get_chars(timeout)))

    def __del__(self):
        termios.tcsetattr(self.fd,termios.TCSAFLUSH,self.old)

class Keys():
    RIGHT_ARROW=[27, 91, 67]
    LEFT_ARROW=[27, 91, 68]
    UP_ARROW=[27, 91, 65]
    DOWN_ARROW=[27, 91, 66]
    d=[100]
    f=[102]
    g=[103]
    ENTER=[10]
    

def is_key(char_list,key):
    for i in xrange(len(char_list)-len(key)+1):
        if char_list[i:i+len(key)]==key:
            return(True)
    return(False)
        
        
