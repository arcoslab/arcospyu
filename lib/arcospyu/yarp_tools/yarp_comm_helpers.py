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


