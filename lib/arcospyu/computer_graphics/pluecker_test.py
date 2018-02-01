# -*- coding: utf-8 -*-
# Copyright (c) 2009 Technische Universitaet Muenchen, Informatik Lehrstuhl IX.
# Author: Federico Ruiz-Ugalde <ruizf at in.tum.de>
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

# Some theory about this can be found here:
# http://www.cgafaq.info/wiki/Plucker_Coordinates also on the wikipedia of
# course

from __future__ import print_function
import numpy as n


def rayIsParallelNormal(vertexA, vertexB, vertexC, rayD, epsilon=1e-10):
    N = n.cross(vertexB - vertexA, vertexC - vertexA)
    test = n.cross(rayD, N)
    test2 = n.inner(test, test)
    if (test2 > -epsilon and test2 < epsilon):
        return 0  # ray and normal are parallel
    else:
        return 1  # are not parallel


def plane_ray_intersection(plane_normal, point_in_plane, ray_pos, ray_dir):
    u2 = n.cross(ray_dir, ray_pos)
    u1 = ray_dir
    d = n.dot(plane_normal, point_in_plane)
    return ((n.cross(u2, plane_normal) - d * u1) / n.dot(u1, plane_normal))


def triangle_ray_intersection(vertexA, vertexB, vertexC, rayPos, rayD):
    e1 = n.array(vertexB - vertexA)
    e2 = n.array(vertexC - vertexA)
    T = n.array(rayPos - vertexA)
    P = n.array(n.cross(rayD, e2))
    Q = n.array(n.cross(T, e1))
    X = (1.0 / (n.inner(P, e1))) * n.array(
        [n.inner(Q, e2), n.inner(P, T),
         n.inner(Q, rayD)])
    return X  # t,u,v


def trianglePlueckerTest(
        vertexA, vertexB, vertexC, rayPos, rayD, epsilon=1e-10):
    e0 = n.array(
        (vertexA - vertexB).tolist() + (n.cross(vertexA, vertexB)).tolist())
    e1 = n.array(
        (vertexC - vertexA).tolist() + (n.cross(vertexC, vertexA)).tolist())
    e2 = n.array(
        (vertexB - vertexC).tolist() + (n.cross(vertexB, vertexC)).tolist())
    R = n.array([(n.cross(rayD, rayPos)).tolist() + rayD.tolist()])
    t0 = n.inner(e0, R)
    t1 = n.inner(e1, R)
    t2 = n.inner(e2, R)
    print('t0: ', t0)  # If zero, means is touching line B-A
    print('t1: ', t1)  # If zero, means, is touching line C-A
    print('t2: ', t2)  # If zero, measn, is touching line C-B

    # if the signs are all the same it means the ray passes through the
    # triangle if any t0 is 0 or near 0 it means the ray passes throught the
    # line or is parallel to the line (passes through the line in infinity)

    if ((t0 > 0 and t1 > 0 and t2 > 0) or (t0 < 0 and t1 < 0 and t2 < 0)):
        print('Inside')
        return 1
    elif ((t0 > -epsilon and t0 < epsilon) or (t1 > -epsilon and t1 < epsilon)
          or (t2 > -epsilon and t2 < epsilon)):
        print('On line')
        return 0
    else:
        print('Outside')
        return -1


def polygon_pluecker_test(vertex_list, ray_pos, ray_dir, epsilon=1e-10):
    pluecker_list = []
    for i, vertexi in enumerate(vertex_list):
        if i < len(vertex_list) - 1:
            vertexj = vertex_list[i + 1]
        else:
            vertexj = vertex_list[0]
        pluecker_list.append(
            n.concatenate((vertexj - vertexi, n.cross(vertexj, vertexi))))
    R = n.concatenate((n.cross(ray_dir, ray_pos), ray_dir))
    ts = []
    for pluecker in pluecker_list:
        ts.append(n.inner(pluecker, R))
    return (ts)


# A=n.array([0.1,0.1,0.1])
# B=n.array([0.1,0.3,0.1])
# C=n.array([0.1,0.3,0.3])
# rayPos=n.array([0.4,0.22,0.2])
# rayD=n.array([-1,0,0])
# segments=visual.curve(pos=[A,B,C,A],radius=0.01)
# ray=visual.arrow(pos=rayPos,axis=rayD,shaftwidth=0.003,headwidth=0.007,fixedwidth=1)
# t.trianglePlueckerTest(A,B,C,rayPos,rayD)
# ray.pos=rayPos
