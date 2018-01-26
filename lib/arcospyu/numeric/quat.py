# -*- coding: utf-8 -*-
# util/quat.py -- quaternions as a way to represent 3D rotations
#
# Copyright 2008, 2009 Jonathan Kleinehellefort <jk@molb.org>
#
# This file is part of plangrasp.
#
# Plangrasp is free software: you can redistribute it and/or modify it
# under the  terms of the GNU  General Public License  as published by
# the Free  Software Foundation, either  version 3 of the  License, or
# (at your option) any later version.
#
# Plangrasp is  distributed in  the hope that  it will be  useful, but
# WITHOUT  ANY   WARRANTY;  without  even  the   implied  warranty  of
# MERCHANTABILITY or  FITNESS FOR A  PARTICULAR PURPOSE.  See  the GNU
# General Public License for more  details. You should have received a
# copy of  the GNU  General Public License  along with  plangrasp.  If
# not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

__all__ = ['norm', 'qinv', 'qmul', 'qrot', 'qnull']

from numpy import array, cross, dot, hstack, repeat, empty
import numpy.random as random
from math import sin, cos, sqrt, acos, pi

qnull = array([0.0, 0.0, 0.0, 1.0])


def norm(q):
    return sqrt(dot(q, q))


def qinv(q):
    """Quaternion inverse"""
    return conj(q) / dot(q, q)


_conj_array = array([-1.0, -1.0, -1.0, 1.0])


def conj(q):
    """Quaternion conjugation"""
    return q * _conj_array


def qmul(q, p):
    """Quaternion multiplication"""
    qs, qv = q[3], q[:3]
    ps, pv = p[3], p[:3]
    return hstack([qs * pv + ps * qv + cross(qv, pv), [qs * ps - dot(qv, pv)]])


def qmul_accumulate(qs_):
    qs = qs_.copy()
    for i in xrange(1, len(qs)):
        qs[i] = qmul(qs[i - 1], qs[i])
    return qs


def qrot(q, v):
    """Rotate vector by quaternion"""
    print 'QROT', q, v
    return qmul(qmul(q, hstack((v, [0]))), qinv(q))[:3]


def dist(q, p):
    return 1.0 - abs(dot(q, p))


def to_angle_and_axis(q):
    return 2.0 * acos(min(1.0, max(-1.0, q[3]))), q[:3]


def from_angle_and_axis(a, v):
    q = empty(4, dtype=float)
    q[:3] = v / norm(v) * sin(.5 * a)
    q[3] = cos(.5 * a)
    return q


# def to_matrix(q, r=array([0.0, 0.0, 0.0])):
#     i, j, k, w = q
#     x, y, z = r
#     return array([[1.0-2.0*(j*j+k*k), 2.0*(i*j+k*w), 2.0*(i*k-j*w),   x],
#                   [2.0*(i*j-k*w), 1.0-2.0*(i*i+k*k), 2.0*(j*k+i*w),   y],
#                   [2.0*(i*k+j*w), 2.0*(j*k-i*w), 1.0-2.0*(i*i+j*j),   z],
#                   [              0.0,           0.0,           0.0, 1.0]])


def to_matrix_fixed(q, r=array([0.0, 0.0, 0.0])):
    i, j, k, w = q
    x, y, z = r
    return array(
        [
            [
                1.0 - 2.0 * (j * j + k * k), 2.0 * (i * j - k * w),
                2.0 * (i * k + j * w), x
            ], [
                2.0 * (i * j + k * w), 1.0 - 2.0 * (i * i + k * k),
                2.0 * (j * k - i * w), y
            ], [
                2.0 * (i * k - j * w), 2.0 * (j * k + i * w),
                1.0 - 2.0 * (i * i + j * j), z
            ], [0.0, 0.0, 0.0, 1.0]
        ])


def r_from_matrix(m):
    return array([m[0, 3], m[1, 3], m[2, 3]])


def from_matrix(m):
    t = 1 + m[0, 0] + m[1, 1] + m[2, 2]
    if t > 0.00000001:
        s = 2.0 * sqrt(t)
        q = array(
            [
                (m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s,
                (m[1, 0] - m[0, 1]) / s, 0.25 * s
            ])
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = 2.0 * sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2])
        q = array(
            [
                0.25 * s, (m[1, 0] + m[0, 1]) / s, (m[0, 2] + m[2, 0]) / s,
                (m[2, 1] - m[1, 2]) / s
            ])
    elif m[1, 1] > m[2, 2]:
        s = 2.0 * sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2])
        q = array(
            [
                (m[1, 0] + m[0, 1]) / s, 0.25 * s, (m[2, 1] + m[1, 2]) / s,
                (m[0, 2] - m[2, 0]) / s
            ])
    else:
        s = 2.0 * sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1])
        q = array(
            [
                (m[0, 2] + m[2, 0]) / s, (m[2, 1] + m[1, 2]) / s, 0.25 * s,
                (m[1, 0] - m[0, 1]) / s
            ])
    return q / norm(q)


def rand():
    """Return uniformly sampled random rotation quaternions."""
    # see also interpolate() for reference
    s = random.rand()
    sigma1 = sqrt(1 - s)
    sigma2 = sqrt(s)
    theta1 = 2 * pi * random.rand()
    theta2 = 2 * pi * random.rand()
    x = sin(theta1) * sigma1
    y = cos(theta1) * sigma1
    z = sin(theta2) * sigma2
    w = cos(theta2) * sigma2
    return array([x, y, z, w])


def interpolate(f, q, p):
    # slerp interpolation as found in:
    # James J. Kuffner: Effective Sampling and Distance Metrics for 3D
    # Rigid Body Pat Planning, In Proc. ICRA 2004
    l = dot(q, p)
    if l < 0.0:
        # quats are point in opposite dirs, so flip p and l
        p = -p
        l = -l
    if abs(1 - l) < 0.001:  # arbitrary guess for epsilon
        # quats are almost the same... do linear interpolation
        r = 1 - f
        s = f
    else:
        # do spherical interpolation for better accuracy in normal case
        alpha = acos(l)
        gamma = 1.0 / sin(alpha)
        r = sin((1 - f) * alpha) * gamma
        s = sin(f * alpha) * gamma
    res = r * q + s * p
    return res / norm(res)
