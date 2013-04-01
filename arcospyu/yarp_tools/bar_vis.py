#!/usr/bin/python
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

# simple.py

import sys
import yarp
from PyQt4 import QtGui,QtCore
from subprocess import Popen
#import configParse

import signal
def signal_handler(signum, frame):
    yarp.Network.fini()
    app.exit(0)



#config,args=configParse.configParse(sys.argv)


class LevelIndicator(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.frame=QtGui.QFrame()
#        self.frame.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.value=0
        self.max=99
        self.min=0
        self.paintX=self.width()-2*self.frame.frameWidth()
        self.setAutoFillBackground(True)
    def setRange(self,min,max):
        if (min>max):
            min=max
        self.min=min
        self.max=max
        self.update()
    def setMinimum(self,min):
        if min>max:
            min=max
        self.min=min
        self.update()
    def setMaximum(self,max):
        if min>max:
            max=min
        self.max=max
        self.update()
    def setValue(self,value):
        if value<min:
            value=min
        if value>max:
            value=max
        if value==self.value:
            return
        self.value=value
        self.update()
    def paintEvent(event):
        self.frame.resize(self.size())
        self.paintX=self.width()-2*self.frame.frameWidth()
        self.painter=QtGui.QPainter(self)
        self.painter.setPen(QtCore.Qt.NoPen)
        self.painter.setBrush(QColor(155,155,255))
        self.painter.drawRect(self.xtrans(0),0,self.xtrans(self.value)-self.xtrans(0),self.height()-2*self.frame.frameWidth()+1)
        self.painter.setPen(QtCore.Qt.red)
        self.painter.drawLine(self.xtrans(0),0,self.xtrans(0),self.height()-2*self.frame.frameWidth())
        self.painter.setPen(QtCore.Qt.black)
        self.painter.drawText(2,(self.height()-2*self.frame.frameWidth())-1,str(self.value))
    def xtrans(self,x):
        return (x*self.paintX/(self.max-self.min))+(abs(self.min)*self.paintX/(self.max-self.min))
        


class Main(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        yarp.Network.init()
        self.inPort=yarp.BufferedPortBottle()
        self.inPort.open(portbasename+"/bar/in")
        self.setWindowTitle('%s arm joints' % portbasename)
#        ok=QtGui.QPushButton("OK")
#        cancel=QtGui.QPushButton("Cancel")
#        level=LevelIndicator(self)
#        level.setValue(10)
        self.hbox=QtGui.QHBoxLayout()
#        hbox.addStretch(1)
#        self.hbox.addWidget(ok)
#        self.hbox.addWidget(cancel)
#        self.hbox.addWidget(level)
        self.setLayout(self.hbox)
        self.resize(300,150)
        self.timer=QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(False)
        self.timer.start()
#        lcd = QtGui.QLCDNumber(self)
#        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
#        self.hbox.addWidget(lcd)
#        self.hbox.addWidget(slider)
#        self.connect(slider,  QtCore.SIGNAL('valueChanged(int)'), lcd, QtCore.SLOT('display(int)') )
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.signalTest)
        self.inSize=0
        self.lcds=[]
        self.max=100
        self.min=-100

    def __del__(self):
        if yarp:
            yarp.Network.fini()
    def signalTest(self):
        inbottle=self.inPort.read(False)
        if inbottle:
            isnum=[]
            newSize=0
            for i in range(inbottle.size()):
                if inbottle.get(i).isDouble() or inbottle.get(i).isInt():
                    isnum.append(True)
                    newSize=newSize+1
                else:
                    isnum.append(False)
 #           print "Old number of numbers: ", self.inSize, " Number of numbers detected: ", newSize
            if newSize!=self.inSize:
                for i in self.lcds:
                    i.hide()
                    #disconnect signal
                    self.hbox.removeWidget(i)
                    del(i)
                self.lcds=[]
                for i in range(newSize):
                    self.lcds.append(QtGui.QProgressBar(self))
                    self.hbox.addWidget(self.lcds[-1])
                    self.lcds[-1].setMaximum(self.max)
                    self.lcds[-1].setMinimum(self.min)
                    self.lcds[-1].setOrientation(QtCore.Qt.Vertical)
                    self.lcds[-1].setFormat('%v')
                    QtCore.QObject.connect(self,QtCore.SIGNAL(''.join(['test',str(i),'(int)'])), self.lcds[-1], QtCore.SLOT('setValue(int)'))
                self.inSize=newSize
            count=0
            for i,x in enumerate(isnum):
                if x:
                    number=inbottle.get(i).asDouble()
                    if number>self.max:
                        number=self.max
                    if number<self.min:
                        number=self.min
#                    if (number>(self.max-5.0)) or (number<(self.min+5.0)):
#                        Popen(["beep","-f",str(count*100+100)])
                    self.emit(QtCore.SIGNAL(''.join(['test',str(count),'(int)'])),int(number))
#                    print "Number: ", number
                    count=count+1
                
        

import optparse
import sys
sim=False
parser=optparse.OptionParser("usage: %prog [options]")
parser.add_option("-b", "--portbasename", dest="portbasename", default="/bar_vis", type="string", help="Port base name")
(options, args)= parser.parse_args(sys.argv[1:])
portbasename=options.portbasename

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

app = QtGui.QApplication(sys.argv)

main=Main()
main.show()

sys.exit(app.exec_())
