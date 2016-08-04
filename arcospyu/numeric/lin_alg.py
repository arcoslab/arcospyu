#!/usr/bin/env python
# Copyright (c) 2013 Federico Ruiz Ugalde
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

from numpy import sign, cross, arccos, arcsin, array, cos, sin, tan, arctan2, pi
from numpy.linalg import norm

def angle_from_a_to_b(a,b):
    s=sign(cross(a,b))
    #print "s", s
    if s==0.:
        s=1.
    return(arccos(min(dot(a,b),1.))*s)


def vector_saturation(vector_min, vector_max, vector):
    angle_min_max=arccos(dot(vector_min,vector_max)/(norm(vector_min)*norm(vector_max)))
    angle_max=arccos(dot(vector,vector_max)/(norm(vector)*norm(vector_max)))
    angle_min=arccos(dot(vector,vector_min)/(norm(vector)*norm(vector_min)))
    print "angles", angle_min_max, angle_max, angle_min
    if (angle_max > angle_min_max) or (angle_min > angle_min_max):
        print "limiting"
        if angle_max < angle_min:
            return(vector_max)
        else:
            return(vector_min)
    return(vector)

def vector_saturation2(vector1, vector2, vector_test):
    #saturates the direction
    vector1n=vector1/norm(vector1)
    vector2n=vector2/norm(vector2)
    if norm(vector_test) > 0.00000001:
        vector_testn=vector_test/norm(vector_test)
    else:
        vector_testn=array([1.0,0.,0.])
    #print "vector1n", vector1n, "vector2n", vector2n, "vector test", vector_testn
    proj_vector1n=dot(vector_testn,vector1n)
    proj_vector2n=dot(vector_testn,vector2n)
    #if proj_vector1n<0. or proj_vector2n<0.:
    #    print "input vector not in the expected direction", proj_vector1n, proj_vector2n
        #return(array([0.,0.,0.]))
    if proj_vector1n<=proj_vector2n:
        # test is done using vector1n
        proj_vector2n_in_1n=dot(vector1n,vector2n)
        if proj_vector1n<proj_vector2n_in_1n:
            print "Vector outside vector2n", vector2n
            return(vector2n)
        else:
            return(vector_testn)
    else:
        #test using vector2n
        proj_vector1n_in_2n=dot(vector2n,vector1n)
        if proj_vector2n<proj_vector1n_in_2n:
            print "Vector outside vector1n", vector1n
            return(vector1n)
        else:
            return(vector_testn)

