#!/usr/bin/python
# Copyright (c) 2009-2011 Technische Universitaet Muenchen, Informatik Lehrstuhl IX.
# Author: Alexis Maldonado Herrera <maldonad at in.tum.de>, Federico Ruiz-Ugalde <ruizf at in.tum.de>
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

import yarp
yarp.Network.init()
cstyle=yarp.ContactStyle()
cstyle.persistent=True
import time
__yarp_binary="yarp"

class ArcosYarpPort(object):
    def __init__(self):
        self._port=yarp.BufferedPortBottle()

    def open(self, name):
        self._port.open(name)

    def read(self, blocking=True):
        return(self._port.read(blocking))

    def write(self, forceStrict=False):
        return(self._port.write(forceStrict))

    def writeStrict(self):
        return(self.write(forceStrict=True))

class ArcosYarpConnectionPair(object):
    def __init__(self, name1, name2, connected_state=False):
        self._connected_state=connected_state
        ##TODO: hash compare

class ArcosYarp(object):
    """ A class for yarp port management.

    The user can:
    1) create new yarp ports
    2) request new yarp port connections
    3) check weather such connections are alive

    The class will automatically:
    1) Maintain a list of port connections that were requested in the current module
    2) Provide a status port that will accept the following commands:
       a) get current requested connections: get_connections
       b) all connections ready? (indicates if all connections are currently made): isready
    """

    def __init__(self, ports_name_prefix="/0", module_name_prefix=""):
        """ Create an Arcoslab yarp object

        ports_name_prefix: used as a namespace for running a complete system
        module_name_prefix: used as base name for all ports in this module
        """
        self._ports_name_prefix=ports_name_prefix
        self._module_name_prefix=module_name_prefix
        self._connections={}
        self._ports=[]
        #create a connection status port
        self._create_con_status_port()

    def _create_con_status_port(self):
        self._con_status_port=yarp.BufferedPortBottle()
        port_name=self._ports_name_prefix+self._module_name_prefix+"/con_status"
        self._con_status_port.setStrict(True)
        self._con_status_port.open(port_name)

    def _del_con_status_port(self):
        self._con_status_port.close()
        del self._con_status_port

    def create_yarp_port(self, name, input_port=True, strict=True, full_name=False):
        """ Create a yarp port """
        port = yarp.BufferedPortBottle()
        if not full_name:
            port_name=self._ports_name_prefix+self._module_name_prefix+name
        else:
            port_name=name
        if strict:
            port.setStrict(True)
        port.open(port_name)
        self._ports.append((port, input_port, port_name))
        return(port)

    def update_connections_state(self):
        for connection in self._connections:
            state=yarp.Network.isConnected(connection[0], connection[1])
            print "For connection: ", connection, " State: ", state
            self._connections[connection][0]=state

    def is_ready(self):
        self.update_connections_state()
        ready=True
        for state, necessary in self._connections.values():
            if necessary:
                if state==False:
                    ready=False
                    break
        #ready=all(self._connections.values())
        if ready:
            print "All connections ready"
        else:
            print "Not all connections ready"
        return(ready)

    def update(self):
        bottle=self._con_status_port.read(False)
        if bottle:
            cmd=bottle.get(0).toString()
            outbottle=self._con_status_port.prepare()
            outbottle.clear()
            if cmd=="isready":
                ready=self.is_ready()
                print "Requested yarp ready state: ", ready
                if ready:
                    outbottle.addString("ready")
                else:
                    outbottle.addString("not_ready")
            elif cmd=="get_connections":
                for connection in self._connections:
                    conbottle=outbottle.addList()
                    conbottle.addString(connection[0])
                    conbottle.addString(connection[1])
                    conbottle.addString(str(self._connections[connection]))
            else:
                print "Unknown command, returning Error"
                outbottle.addString("Error")
            self._con_status_port.writeStrict()

    def connect(self, local_port, remote_module, remote_name, necessary=True):
        cstyle=yarp.ContactStyle()
        cstyle.persistent=True
        for port_entry in self._ports:
            if port_entry[0]==local_port:
                break
        if port_entry[1]:
            #input port
            yarp.Network.connect(self._ports_name_prefix+remote_module+remote_name, port_entry[2], cstyle)
            self._connections[(self._ports_name_prefix+remote_module+remote_name, port_entry[2])]=[False, necessary]
        else:
            #output port
            yarp.Network.connect(port_entry[2], self._ports_name_prefix+remote_module+remote_name, cstyle)
            self._connections[(port_entry[2], self._ports_name_prefix+remote_module+remote_name)]=[False, necessary]
        ## TODO: connections convert to own class to allow hash compares but also maintain connection state

    def __del__(self):
        #must delete all yarp ports
        self._del_con_status_port()
        while len(self._ports):
            port_entry=self._ports.pop()
            port_entry[0].close()
            del port_entry[0]

def change_ps_name(name):
    """Change process name as used by ps(1) and killall(1)."""
    try:
        import ctypes
         
        libc = ctypes.CDLL('libc.so.6')
        libc.prctl(15, name, 0, 0, 0)
    except:
        pass
     

def new_port(portname, direction, otherport, carrier='tcp', timeout=20.0):
    ''' returns a new yarp port, and connects it
    '''
    
    port = yarp.BufferedPortBottle()
    port.open(portname)
    if (direction == 'in'):
        yarp_connect_blocking(otherport,portname, timeout, carrier)
    elif (direction == 'out'):
        yarp_connect_blocking(portname,otherport, timeout, carrier)
    elif (direction == 'both'):
        yarp_connect_blocking(portname,otherport, timeout, carrier)
        yarp_connect_blocking(otherport,portname, timeout, carrier)
    else:
        print("new_port() error. Specify: in/out/both")

    return(port)



def yarp_queryname_blocking(port,timeout):
    startTime=time.time()

    trying=True
    msg_counter=0

    while (trying):
        if (yarp.Network.queryName(port).isValid()):
            #We found the name, now we ping it

            #Let's use the yarp companion program to ping
            #To see what it is doing internally, check: /yarp2/src/libYARP_OS/src/Companion.cpp (Function: int Companion::cmdPing)
            import subprocess
            devnull=open("/dev/null")
            pinger=subprocess.Popen([__yarp_binary,"ping",port],stdout=devnull) #Sending stdout to bitheaven (yarp ping is a bit too verbose)
            devnull.close()
            ret=pinger.wait()

            if (ret==0): #ping was acknowledged
                trying=False
                return(True)

            if (ret==1):
                #it did not answer
                print "Port did not answer ping. Process busy, or maybe you should call 'yarp clean'? (%s)--------------"%(port)

        else:
            if(msg_counter == 0):
                print "Waiting for %s" %(port)

        if ((time.time()-startTime) > timeout):
            trying=False
            print("yarp_queryname_blocking: TIMEOUT. Couldn't find port %s" %(port))
            return(False)

        time.sleep(0.1)
        msg_counter = (msg_counter + 1) % 10

def yarp_connect_blocking(srcPort,dstPort,timeout=20.0, carrier='tcp'):
    print "Connecting %s to %s" % (srcPort, dstPort)
    startTime = time.time()
    try:
        found_src = yarp_queryname_blocking(srcPort, (timeout-(time.time()-startTime)))
        found_dst = yarp_queryname_blocking(dstPort, (timeout-(time.time()-startTime)))

        if (found_src and found_dst):
            yarp.Network.connect(srcPort, dstPort, carrier)
            if carrier == 'mcast':
                #Repeat connect after a sec
                time.sleep(0.5)
                yarp.Network.connect(srcPort, dstPort, carrier)
            time.sleep(0.5)
            yarp.Network.connect(srcPort, dstPort, cstyle)
            return(True)
        else:
            print("yarp_connect_blocking: TIMEOUT")
            return(False)

    except KeyboardInterrupt:
        print "yarp_connect_blocking: KeyboardInterrupt -> not connecting ports!"
        raise

import types

def recur(bottle,ilist):
    for item in ilist:
        if type(item)==types.FloatType:
            bottle.addDouble(item)
        elif type(item)==types.IntType:
            bottle.addInt(item)
        elif type(item)==types.StringType:
            bottle.addString(item)
        elif type(item)==types.ListType:
            bottlelist=bottle.addList()
            recur(bottlelist,item)
        else:
            print "Data type not allowed"

def sendListPort(yarpPort,ilist):
    bottle=yarpPort.prepare()
    bottle.clear()
    recur(bottle,ilist)
    #map(bottle.addDouble,list)
    yarpPort.write()

def yarp_write(dest_port, ilist, portname="/test"):
  port=new_port(portname, 'out', dest_port)
  sendListPort(port,ilist)

def write_bottle_lists(yarp_port, list_of_lists):
    main_bottle=yarp_port.prepare()
    main_bottle.clear()
    for ilist in list_of_lists:
        bottle=main_bottle.addList()
        map(bottle.addDouble, ilist)
    yarp_port.write()

def write_narray_port(yarp_port,narray):
    bottle=yarp_port.prepare()
    bottle.clear()
    map(bottle.addDouble,narray)
    yarp_port.write()

def readListPort(yarpPort,blocking=False):
    bottle=yarpPort.read(blocking)
    if bottle:
        return map(yarp.Value.asDouble,map(bottle.get,range(bottle.size())))
    else:
        return False

def yarpListofDoublesToList(yarplist):
    return map(yarp.Value.asDouble,map(yarplist.get,range(yarplist.size())))

def yarpListToList(yarplist):
    result=[]
    for i in map(yarplist.get,range(yarplist.size())):
        if i.isDouble():
            result.append(i.asDouble())
        if i.isInt():
            result.append(i.asInt())
        if i.isString():
            result.append(i.toString())
        if i.isList():
            result.append(yarpListToList(i))
    return result

def listToKdlFrame(list):
    import PyKDL
    kdlframe=PyKDL.Frame()
    if len(list)!=16:
        return False
    else:
        for i in range(4):
            for j in range(4):
                if i<3 and j<3:
                    kdlframe.M[i,j]=list[j+i*4]
                elif j==3 and i<3:
                    kdlframe.p[i]=list[j+i*4]
        return kdlframe

def kdlFrameToList(kdlframe):
    list=[]
    for i in range(4):
        for j in range(4):
            if i<3 and j<3:
                list.append(kdlframe.M[i,j])
            elif j==3 and i<3:
                list.append(kdlframe.p[i])
            elif i==3 and j<3:
                list.append(0)
            else:
                list.append(1)
    return list

def kdl_vector_to_list(kdlvector):
    list=[]
    for i in xrange(3):
        list.append(kdlvector[i])
    return(list)

def bottle_to_list(bottle):
    result=[]
    yarp_value_list=map(bottle.get,range(bottle.size()))
    for i in yarp_value_list:
        if i.isList():
            result.append(bottle_to_list(i.asList()))
        if i.isDouble():
            result.append(i.asDouble())
        if i.isInt():
            result.append(i.asInt())
        if i.isString():
            result.append(i.toString())
    return(result)

def main():

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("-c", "--connect", dest="ports_to_connect", 
        help="connect the two ports, separated by a colon (:) (PORTS).", metavar="PORTS", default= "")
    parser.add_option("-t", "--timeout", dest="timeout", 
        help="Timeout in seconds for the connect option (TIMEOUT)", metavar="TIMEOUT", default= "20")
    parser.add_option("-r", "--read-bottle", dest="port_to_read_from", 
        help="Read a bottle from port PORT", metavar="PORT", default= "")
    parser.add_option("-a", "--carrier", dest="carrier",
        help="Carrier to use: tcp/udp/mcast", metavar="CARRIER", default='tcp')

    (options, args) = parser.parse_args()
    if(options.port_to_read_from != ""):
        input=yarp.BufferedPortBottle()
        input.open("...")
        yarp.Network.connect(options.port_to_read_from, input.getName().c_str())
        b_in = input.read()
        print b_in.toString()
        input.close()

    


    try:

        #The normal yarp format: yarp connect port1 port2
        if (len(args)==3):
            if (args[0]=="connect"):
                options.ports_to_connect=args[1]+"%"+args[2]

        if (options.ports_to_connect != ""):
            ports=options.ports_to_connect.split("%")
            if (len(ports) != 2):
                print "Error: Need two ports to connect. Example: sourceport:destport"
                #raise NameError('Portnames missing')
                return(False)

            print "Connecting %s to %s." %(ports[0],ports[1])
            ret = yarp_connect_blocking(ports[0],ports[1],float(options.timeout), options.carrier)
            if (ret):
                print "Success!"
            else:
                print "Failed"

            return(ret)

    except Exception, e:
        print "Exception! %r" %(e)
        print "__yarp_binary = %r"%(__yarp_binary)
        return(False)



if __name__ == "__main__":
    main()


