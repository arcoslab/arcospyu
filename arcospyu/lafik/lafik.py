#!/usr/bin/env python

# Author: Alexis Maldonado Herrera <maldonad at cs.tum.edu>, Federico Ruiz-Ugalde <ruizf at in.tum.de>, Ingo Kresse <kresse at in.tum.de>, Jonathan Kleinehellefort <kleinehe at cs.tum.edu>
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

# Lafik: Limits aware forward and inverse kinematics. Lafik is based on orocos-kdl and it tries to calculate inverse and forward
# kinematics taking into account joint limits. When one or more joints are getting near to a mechanical limit the inverse
# kinematics solution starts to use less and less this particular joints, and tries to use more and more the other joints to
# complete the task. It doesn't reconfigure completely the articulator to solve the problem, therefore is a local solution.

import sys
from PyKDL import *
from math import pi
from numpy import array
from numpy import identity
from arcospyu.numeric.print_array import print_array
from numpy import dot
from numpy.linalg import LinAlgError
from numpy.linalg import pinv
task_dim=6

def normalize_angle(angle):
    from math import atan2, sin, cos
    return (atan2(sin(angle),cos(angle)))

class RJoint(object):

    def __init__(self, robot, i):
        self.robot = robot
        self.i = i

    def _get_kdlframe(self):
        kdlframe = Frame()
        self.robot.fk_solver.JntToCart(self.robot.jnt_pos, kdlframe, self.i)
        return kdlframe

    kdlframe = property(_get_kdlframe)


    def _get_static_transform(self):
        return self.robot.segments[self.i].pose(0)

    static_transform = property(_get_static_transform)

    def _get_value(self):
        return self.robot.jnt_pos[self.i]

    def _set_value(self, value):
        self.robot.jnt_pos[self.i] = value

    value = property(_get_value, _set_value)

class Lafik(object):
    def __init__(self,config, tool=None):
        self.config = config
        self.segments = self.config.arm_segments
        self.joint_limits = self.config.arm_extralimits

        self.chain = Chain()
        for segment in self.segments:
            self.chain.addSegment(segment)
        if tool != None:
            self.chain.addSegment(Segment(Joint(Joint.None), tool))

        self.nJoints = self.chain.getNrOfJoints()
        self.jnt_pos = JntArray(self.nJoints)
        self.jnt_posOld = JntArray(self.nJoints)
        self.qdotSign = [0] * self.nJoints

        self.fk_solver = ChainFkSolverPos_recursive(self.chain)
        self.jac_solver = ChainJntToJacSolver(self.chain)      
        self.ikv_solver = ChainIkSolverVel_wdls(self.chain)
        self.ikv_solver.setLambda(self.config.ik_lambda)
        #self.ikv_solver.setWeightTS(config.ik_weightTS)
        #self.ikv_solver.setWeightJS(config.ik_weightJS) 

        self.ikv_solver_norot = ChainIkSolverVel_wdls(self.chain)
        self.ikv_solver_norot.setLambda(self.config.ik_lambda)

        #w = config.ik_weightTS
        #self.ikv_solver_norot.setWeightTS((w[0], w[1], w[2], 0.0, 0.0, 0.0))
        self.tweights=identity(task_dim)
        self.jweights=identity(self.nJoints)

        self.ik_solver = ChainIkSolverPos_NR(self.chain,
                                             self.fk_solver,
                                             self.ikv_solver)
        self.joints = [RJoint(self, i)
                       for i in range(self.nJoints)]
        self._torques = [0.0] * self.nJoints
        self.forces= array([0.0] * 6)
        self._qdot_list = array([0.0] * self.nJoints)
        self._jac = Jacobian(self.nJoints)
        


    def _get_qdot(self):
        return(self._qdot_list)
    def _set_qdot(self,qdot):
        self._qdot_list=qdot
    qdot=property(_get_qdot,_set_qdot)
    def calculate_vel(self):
        jac_temp=array([[self._jac[m,n] for n in range(self.nJoints)] for m in range(6)])
        return(dot(jac_temp,self._qdot_list))
    def __iter__(self):
        return iter(self.joints)

    def __getitem__(self, i):
        return self.joints[i]

    def _get_kdlframe(self):
        kdlframe = Frame()
        self.fk_solver.JntToCart(self.jnt_pos, kdlframe)

        return kdlframe

    kdlframe = property(_get_kdlframe)

    def _get_frame(self):
        kdlframe = self._get_kdlframe()
        frame = []
        for i in range(16):
            row = int(i/4)
            column = int(i - row*4)
            if row < 3:
                if column != 3:
                    frame.append(kdlframe.M[row,column])
                else:
                    frame.append(kdlframe.p[row])
            elif column == 3:
                frame.append(1)
            else:
                frame.append(0) 
        return frame

    frame = property(_get_frame)

    def _get_numJnts(self):
        return self.jnt_pos.rows()

    numJnts = property(_get_numJnts)

    def _get_jntsList(self):
        list=[]
        for i in range(self.jnt_pos.rows()):
            list.append(self.jnt_pos[i])
        return(list)
    def _set_jntsList(self,qin):
        if (len(qin) <= self.jnt_pos.rows() ):
            self.jnt_posOld=JntArray(self.jnt_pos)
            for i in range(len(qin)):
                self.jnt_pos[i]=qin[i]
            for i in range( self.jnt_pos.rows()-len(qin) ):
                j=len(qin)+i
                print "Warning: Setting joint %d to 0" %(j)
                self.jnt_pos[j]=0;
            #self.qdotSign=self.estimqDotSign(self.jntToList(self.jnt_pos),self.jntToList(self.jnt_posOld))
            self.updateJntLimits()
            #self.update_joint_weights(self.qdotSign)
            return True
        else:
            print "Error: Wrong number of joint angles"
            return False

    def estimqDotSign(self,qnew,qold):
        result=[]
        for i,j in zip(qnew,qold):
            if i>j: #positive
                result.append(1)
            elif i<j: #negative
                result.append(-1)
            else:
                result.append(0)
        return result

    def updateJntLimits(self):
        self.joint_limits=self.config.updateJntLimits(self.jnt_pos)


    def distToCenter(self,minmax,x):
        '''Takes a list with the minimun value and the maximum value and
        the current position and returns the normalized distance from the current position
        to the center of the whole range'''
        drange=abs(minmax[1]-minmax[0])
        center=min(minmax)+drange/2
        if drange==0:
            return 1.0
        else:
            return (x-center)/(drange/2)

    jntsList = property(_get_jntsList, _set_jntsList)


    def try_move(self, kdlframe):
        jnt_pos = JntArray(self.jnt_pos)
        if self.ik_solver.CartToJnt(jnt_pos, kdlframe, jnt_pos) == 0:
            self.jnt_pos = jnt_pos
            return True
        else:
            return False


    def try_move_limits(self, frame, block_x=False, forced_first=None):

        print('try_move_limits')
        #initialize joint values for search from sane values
        init_joint_pos = self.config.initial_joint_pos

        for i in range (len(init_joint_pos)):
            self.jnt_pos[i]=init_joint_pos[i]

        q_out = JntArray(self.jnt_pos)

        delta_q = JntArray(self.jnt_pos.rows())

        
        if block_x:
            # FIXME: only load this when necessary
            import base_coll_check
            base_coll = base_coll_check.CollDetector()
            base_coll.update_grid()
            last_ok_base_movement = (0.0, 0.0, 0.0)
            
            #check if we are crashing at 0.0, 0.0, 0.0, then move back
            #max_move_back = 0.40
            #delta_move_back = -0.05
            #start_base_movement = [0.0, 0.0, 0.0]
            
            #while (base_coll.check_coll(*start_base_movement)):
            #    start_base_movement = [start_base_movement[0] + delta_move_back, start_base_movement[1], start_base_movement[2]]
            #    if abs(start_base_movement[0]) > max_move_back:
            #        continue
            
            #while :
            #    last_ok_base_movement = (q_out[0], q_out[1], q_out[2])
        
        maxiter = 600
        eps = 0.005
        f = Frame()
        searching = True

        iter = 0
        while(searching):
            iter += 1

            self.fk_solver.JntToCart(q_out, f)
            delta_twist = diff(f, frame)

            change = 0.0
            for i  in range(self.nJoints):
                change += abs(delta_twist[i])

            if (abs(change) < eps):
                print "Iter = %r" %(iter)
                for i in range(self.nJoints):
                    q_out[i] = normalize_angle( q_out[i] )

                searching = False
                self.jnt_pos = q_out
                return True

            self.ikv_solver.CartToJnt(q_out, delta_twist, delta_q);
            Add(q_out, delta_q, q_out);


            
            #Clamp to the limits
            q_list = [q_out[i] for i in range(self.numJnts)]
            self.joint_limits = self.config.updateJntLimits(q_list) #Dynamic limits for J5/J6 of arm (wrist)

            for i in range(len(self.joint_limits)):
                if (q_out[i] < self.joint_limits[i][0]):
                    q_out[i] = self.joint_limits[i][0]
                elif (q_out[i] > self.joint_limits[i][1]):
                    q_out[i] = self.joint_limits[i][1]
                    
            
            
            #FIXME: rename block_x, now uses the base_collision_check
            if block_x:
                coll = base_coll.check_coll(q_out[0], q_out[1], q_out[2])
                #avoid movement to the front
                #if q_out[0] > 0.0:
                #    q_out[0] = 0.0
                if not coll:
                    last_ok_base_movement = (q_out[0], q_out[1], q_out[2])
                else:  #FIXME: Interpolate between new and old position
                    q_out[0] = last_ok_base_movement[0]
                    q_out[1] = last_ok_base_movement[1]
                    q_out[2] = last_ok_base_movement[2]

            if forced_first is not None:
                q_out[0] = forced_first[0]
                q_out[1] = forced_first[1]
                q_out[2] = forced_first[2]





            #Algorithm has converged:
            #print "Delta_twist: " + str(delta_twist.vel)
            #print "Eps: %f"%(eps)
            #print "Delta_q: "+str(delta_q)


            if (iter > maxiter):
                print "IK: Did not converge"
                return False




    def jac(self):
        j = Jacobian(self.nJoints)
        self.jac_solver.JntToJac(self.jnt_pos, j)
        return j

    def jac_list(self):
        j = self.jac()
        return [[j[m,n] for n in range(self.nJoints)] for m in range(6)]
    def update_jac(self):
        self.jac_solver.JntToJac(self.jnt_pos,self._jac)

    def set_jweights(self,weights):
        if weights.shape == (self.nJoints,self.nJoints):
            self.jweights = weights
        else:
            print "ERROR: set_jweights, wrong length"

    def set_tweights(self,weights):
        if weights.shape == (task_dim,task_dim):
            self.tweights = weights

    def getIKV(self, velxyz, velrot):

        jnt_pos = self.jnt_pos

        tw = Twist()
        tw[0] = velxyz[0]
        tw[1] = velxyz[1]
        tw[2] = velxyz[2]
        tw[3] = velrot[0]
        tw[4] = velrot[1]
        tw[5] = velrot[2]

        qdot = JntArray(self.chain.getNrOfJoints())
        #weight matrix with 1 in diagonal to make use of all the joints.
        jweights = identity(self.nJoints)
        self.ikv_solver.setWeightTS(self.tweights.tolist())
        self.ikv_solver.setWeightJS(jweights.tolist())
        if (self.ikv_solver.CartToJnt(jnt_pos, tw, qdot) == 0):
            #Adjust Joint matrix weight according to distance to joint limit
#            print "Joints: ", map(lambda x: x*360.0/(2*pi),self.jntsList)
            #print "Limits: ", self.joint_limits
            weightDiag = []
            for q,l,s,qdot_desired in zip(self.jntsList, self.joint_limits, self.qdotSign,qdot):
                dist = self.distToCenter(l,q)
                #print "Distance: ", dist, " qdotSign: ", i[2]
                jointSlowDown = 0.6
                m = -1 / (1 - jointSlowDown)
                if abs(dist) < jointSlowDown:
                    jointWeight = 1.0
                elif ((dist > 0) and (qdot_desired < 0)) or ((dist < 0) and (qdot_desired > 0)):
                    jointWeight = 1.0
                #elif (s==0 and ((dist>0 and qdot_desired<0) or (dist<0 and qdot_desired>0))):
                #    jointWeight=1.0
                else:
                    jointWeight = 1.0 + m * (abs(dist) - jointSlowDown)
                    if jointWeight < 0:
                        jointWeight = 0.0
                weightDiag.append(jointWeight)
            jweights = array(self.jweights)
            jws = self.update_joint_weights([qdot[i] for i in xrange(self.nJoints)])
            #print_array("Weights for cable: ", jws.tolist())
            for i in xrange(self.nJoints):
                jweights[i][i] = jweights[i][i] * weightDiag[i] * jws[i]
            #weightMatrix[3][3]=0.00000001
            #print_array("Weights for limits: ", weightDiag) #, "matrix: ", weightMatrix
            #print_array( "Weights:", [jweights[i][i] for i in xrange(self.nJoints)])
            #print
            if self.config.disable_smart_joint_limit_avoidance:
                for i in range(6):
                    qdot[i] *= min(weightDiag)
                return self.jntToList(qdot)
            else:
                self.ikv_solver.setWeightJS(jweights.tolist())
                if (self.ikv_solver.CartToJnt(jnt_pos,tw,qdot) == 0):
                    self.qdotSign = [qdot[i] for i in xrange(self.nJoints)]
                    return self.jntToList(qdot)
                else:
                    return False
        else:
            return False

    def try_qdot_norot(self,velxyz):

        jnt_pos = self.jnt_pos

        tw = Twist()
        tw[0] = velxyz[0]
        tw[1] = velxyz[1]
        tw[2] = velxyz[2]

        qdot = JntArray(self.chain.getNrOfJoints())
        if (self.ikv_solver_norot.CartToJnt(jnt_pos,tw,qdot) == 0):
            return self.jntToList(qdot)
        else:
            return False

    def update_joint_weights(self,qdot):
        return self.config.update_joint_weights(self.jntsList,qdot)

    def jntToList(self,jnt):
        l = []
        for i in range(jnt.rows()):
            l.append(jnt[i])
        return(l)

    def get_limits(self):
        self.updateJntLimits()
        return self.joint_limits

    def _get_torques(self):
        return self._torques

    def _set_torques(self,torques):
        self._torques = torques

    torques = property(_get_torques,_set_torques)

    def calculate_forces(self):
        jac_temp = array([[self._jac[m,n] for n in range(self.nJoints)] for m in range(6)])
#        print "Jac:", jac_temp
#        print "Jac pinv:", pinv(jac_temp.T)
        new_forces = True
        try:
            forces = dot(pinv(jac_temp.T), array(self.torques))
        except LinAlgError:
            new_forces = False
            pass
        else:
            self.forces = forces
        return(self.forces,new_forces)

    def calc_torques(self,force):
        jac_temp = array([[self._jac[m,n] for n in range(self.nJoints)] for m in range(6)])
        return(dot(jac_temp.T,force))

__all__ = ['Lafik']

def main():
    import sys, yarp, configParse
    (config, args) = configParse.configParse(sys.argv)

    if len(args) == 1 and (args[0] == 'pfk' or args[0] == 'ik'):
        basename = '/'+args[0]
    else:
        print 'usage: ./robot.py [pfk|ik]'
        sys.exit()

    port_in  = yarp.BufferedPortBottle()
    port_in.open(basename+'/in')

    port_out = yarp.BufferedPortBottle()
    port_out.open(basename+'/out')

    if basename == '/ik':
        # add extra port
        port_qin = yarp.BufferedPortBottle()
        port_qin.open(basename+'/qin')

    r = Lafik(config)

    while True:
        bottle = port_in.read(True)
        data_in = [bottle.get(i).asDouble() for i in range(bottle.size())]

        if basename == '/pfk':
            r.jntsList = data_in
            data_out = r.frame
        elif basename == '/ik':
            qin = port_qin.read(False)
            r.jntsList = [qin.get(i).asDouble() for i in range(qin.size())]
            data_out = r.getIKV(data_in[0:3], data_in[3:6])

        bottle = port_out.prepare()
        bottle.clear()
        for i in range(len(data_out)):
            bottle.addDouble(data_out[i])
        port_out.write()
    print "quitting"

if __name__ == "__main__":
    main()
