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
        print out   
        return(out)

    def get_num_chars(self,timeout=0):
        return(map(ord,self.get_chars(timeout)))

    def __del__(self):
        termios.tcsetattr(self.fd,termios.TCSAFLUSH,self.old)

class Keys():
    #this is ASCII
    UP_ARROW=   [27, 91, 65]
    DOWN_ARROW= [27, 91, 66]
    RIGHT_ARROW=[27, 91, 67]
    LEFT_ARROW= [27, 91, 68]
    number0=[48]
    number1=[49]
    number2=[51]
    number3=[52]
    number4=[53]
    number5=[54]
    number6=[55]
    number7=[56]
    number8=[57]
    number9=[58]
    cap_a=[65]
    cap_b=[66]
    cap_c=[67]
    cap_d=[68]
    cap_e=[69]
    cap_f=[70]
    cap_g=[71]
    cap_h=[72]
    cap_i=[73]
    cap_j=[74]
    cap_k=[75]
    cap_l=[76]
    cap_m=[77]
    cap_n=[78]
    cap_o=[79]
    cap_p=[80]
    cap_q=[81]
    cap_r=[82]
    cap_s=[83]
    cap_t=[84]
    cap_u=[85]
    cap_v=[86]
    cap_w=[87]
    cap_x=[88]
    cap_y=[89]
    cap_z=[90]
    a=[97]
    b=[98]
    c=[99]
    d=[100]
    e=[101]
    f=[102]
    g=[103]
    h=[104]
    i=[105]
    j=[106]
    k=[107]
    l=[108]
    m=[109]
    n=[110]
    o=[111]
    p=[112]
    q=[113]
    r=[114]
    s=[115]
    t=[116]
    u=[117]
    v=[118]
    w=[119]
    x=[120]
    y=[121]
    z=[122]
    ENTER=[10]
    

def is_key(char_list,key):
    for i in xrange(len(char_list)-len(key)+1):
        if char_list[i:i+len(key)]==key:
            return(True)
    return(False)


