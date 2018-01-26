# -*- coding: utf-8 -*-
# Copyright (c) 2009 Technische Universitaet Muenchen, Informatik Lehrstuhl IX.
# Authors: Alexis Maldonado Herrera <maldonad at cs.tum.edu> Federico Ruiz Ugalde <memeruiz@gmail.com> # noqa
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

from numpy import array, identity
import PyKDL
# from arcospyu.dprint import eprint


def frame_to_list(f):
    temp = []
    for i in range(3):
        for j in range(4):
            temp.append(f[i, j])
    temp += [0., 0., 0., 1.]
    # eprint('frame to list', temp)
    return (temp)


def narray_to_kdlframe(narray):
    kdlframe = PyKDL.Frame()
    for i in xrange(4):
        for j in xrange(4):
            if i < 3 and j < 3:
                kdlframe.M[i, j] = narray[i, j]
            elif j == 3 and i < 3:
                kdlframe.p[i] = narray[i, j]
    return kdlframe


def kdlframe_to_narray(kdlframe):
    narray = identity(4)
    for i in xrange(4):
        for j in xrange(4):
            if i < 3 and j < 3:
                narray[i, j] = kdlframe.M[i, j]
            elif j == 3 and i < 3:
                narray[i, j] = kdlframe.p[i]
    return narray


def narray_to_kdltwist(narray):
    twist = PyKDL.Twist(
        PyKDL.Vector(narray[0], narray[1], narray[2]),
        PyKDL.Vector(narray[3], narray[4], narray[5]))
    return (twist)


def kdltwist_to_narray(kdltwist):
    return (array([kdltwist[i] for i in xrange(6)]))


def kdl_rot_mat_to_narray(kdl_rot_mat):
    rot = identity(3)
    for r in xrange(3):
        for c in xrange(3):
            rot[r, c] = kdl_rot_mat[r, c]
    return (rot)


def rot_vector_angle(vector, angle):
    kdl_vector = PyKDL.Vector(vector[0], vector[1], vector[2])
    return (kdl_rot_mat_to_narray(PyKDL.Rotation.Rot(kdl_vector, angle)))


def kdl_rot_vector_angle(vector, angle):
    kdl_vector = PyKDL.Vector(vector[0], vector[1], vector[2])
    return (PyKDL.Rotation.Rot(kdl_vector, angle))


def my_adddelta(frame, twist, dt):
    return (
        kdlframe_to_narray(
            PyKDL.addDelta(
                narray_to_kdlframe(frame), narray_to_kdltwist(twist), dt)))


def my_diff(frame1, frame2, dt):
    return (
        kdltwist_to_narray(
            PyKDL.diff(
                narray_to_kdlframe(frame1), narray_to_kdlframe(frame2), dt)))


def my_get_euler_zyx(rot_mat):
    rot_mat_kdl = PyKDL.Rotation()
    for r in xrange(3):
        for c in xrange(3):
            rot_mat_kdl[r, c] = rot_mat[r, c]
    return (array(rot_mat_kdl.GetEulerZYX()))


def rpy_to_rot_matrix(roll_pitch_yaw):
    kdl_matrix = PyKDL.Rotation.RPY(
        roll_pitch_yaw[0], roll_pitch_yaw[1], roll_pitch_yaw[2])
    return (kdl_rot_mat_to_narray(kdl_matrix))
