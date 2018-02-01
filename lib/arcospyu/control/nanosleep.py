# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2006 Lovely Systems and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED 'AS IS' AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
#
# The following code was adapted for inclusion into the OID5 project by
# Alexis Maldonado Herrera <maldonad at cs.tum.edu> in 2008

import ctypes
try:
    libc = ctypes.CDLL('libc.so.6')
except OSError:
    libc = None
    raise ImportError


class timespec(ctypes.Structure):
    _fields_ = [('secs', ctypes.c_long), ('nsecs', ctypes.c_long)]


libc.nanosleep.argtypes = [ctypes.POINTER(timespec), ctypes.POINTER(timespec)]


def nanosleep(sec, nsec):
    sleeptime = timespec()
    sleeptime.secs = sec
    sleeptime.nsecs = nsec
    remaining = timespec()
    libc.nanosleep(sleeptime, remaining)
    return (remaining.secs, remaining.nsecs)
