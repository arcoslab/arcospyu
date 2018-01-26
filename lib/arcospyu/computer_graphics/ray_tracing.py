#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from numpy import dot, array
from numpy.linalg import norm
from arcospyu.computer_graphics.pluecker_test import (
    polygon_pluecker_test, plane_ray_intersection)
from arcospyu.robot_tools.robot_trans import homo_matrix


def plane_ray_intersec2(normal_plane, point_plane, vector, pos):
    d = dot((point_plane - pos), normal_plane) / dot(vector, normal_plane)
    result = pos + vector * d
    return ([d, result])


def most_far_away_face_from_point(
        crossing_faces_local, crossing_faces_reference_frame, point):
    dist = -1
    final_face = -1
    for face in crossing_faces_local:
        touch_point_local = crossing_faces_local[face][2][1]
        touch_point = dot(
            crossing_faces_reference_frame,
            homo_matrix(trans=touch_point_local))[:3, 3]
        print 'Touch point', face, touch_point
        cur_dist = norm(touch_point - point)
        if dist < 0.:
            dist = cur_dist
            final_touch_point = touch_point
            final_face = face
        else:
            if cur_dist > dist:
                dist = cur_dist
                final_touch_point = touch_point
                final_face = face
    return (final_touch_point, final_face)


def find_crossing_faces(vector, vector_pos, vertices_faces, planes):
    crossing_faces = {}
    for face in vertices_faces:
        temp = array(
            polygon_pluecker_test(
                vertices_faces[face], vector_pos, vector / norm(vector)))
        #        print 'pluecker test', face, temp
        crossing_face = False
        if all(temp > 0.) or all(temp < 0.):
            #            print 'Finger will cross face:', face
            crossing_face = True
        elif all(temp >= 0.) or all(temp <= 0.):
            #            print 'not positive'
            # if the zeros are only two and are next to each other then it
            # crosses the face
            i = 0
            j = 0
            while i < len(temp) - j:
                num = temp[i]
                #                print 'num', num
                if num == 0. and not crossing_face:
                    #                    print 'zero'
                    crossing_face = True  # we suppose beforehand
                    i += 1
                    if i == len(temp):
                        num = temp[0]
                    else:
                        num = temp[i]
                    i += 1
                    if num == 0.:
                        # print 'crossing face, two zeros'
                        pass
                    else:
                        # print 'crossing face, one zero'
                        if i == 2:
                            # print 'Don't check for last item'
                            j = 1
                elif num == 0. and crossing_face:
                    crossing_face = False  # we rectify wrong previews assumption # noqa
                    break
                else:
                    i += 1
        if crossing_face:
            # calculate where is crossing the face
            vertices = vertices_faces[face]
            # intersection=triangle_ray_intersection(vertices[0],vertices[1],
            #                                       vertices[2],vector_pos,vector)
            # intersection=plane_ray_intersection(array(planes[face][0]),
            #                                    array(planes[face][1]),
            #                                    vector_pos,vector)
            intersection = plane_ray_intersec2(
                array(planes[face][0]), array(planes[face][1]), vector,
                vector_pos)
            intersection[0] *= norm(vector)
            print 'intersection', intersection
            crossing_faces[face] = [vertices_faces[face], temp, intersection]
    print 'crossing_faces', crossing_faces
    return (crossing_faces)
