from numpy import array, identity, dot, pi, cos, sin
from numpy.linalg import norm
from numpy.random import normal


def add_noise_to_pose(pose, dist_noise=0.02, angle_noise=5.0*pi/180.0):
    noise_pose=identity(4)
    noise_pose[:3,3]=normal(loc=pose[:3,3], scale=dist_noise, size=(3))
    random_angles=normal(loc=0.,scale=angle_noise, size=(3))
    noise_pose[:3,:3]=dot(pose[:3,:3],rpy_to_rot_matrix(random_angles))
    return(noise_pose)


def homo_matrix(rot_m=identity(3),trans=array([0.]*3)):
    m=identity(4)
    m[:3,:3]=rot_m
    m[:3,3]=trans
    return(m)


def rot_z(angle):
    return(array([[cos(angle), -sin(angle), 0.],
                  [sin(angle), cos(angle),0.],
                  [0.,0.,1.]]))

def rot_x(angle):
    return(array([[1., 0., 0.],
                  [0., cos(angle), -sin(angle)],
                  [0., sin(angle), cos(angle)]]))

def rot_y(angle):
    return(array([[cos(angle), 0, sin(angle)],
                  [0., 1., 0.],
                  [-sin(angle), 0., cos(angle)]]))


def random_homo_matrix(center_pos=array([0.]*3), noise_level=array([0.02,0.02,0.02,5.0*pi/180.0,5.0*pi/180.0,5.0*pi/180.0])):
    #incomplete function, not finished
    out_matrix=identity(4)
    out_matrix[:3,3]=normal(loc=array(center_pos), scale=noise_level[:3], size=(3))
    random_angles=normal(loc=array(center_angles),scale=noise_level[2])
    table_object_normal=-array(self.box_planes[self.table_object_face][0])
    print "table normal", table_object_normal
    random_rot_frame=identity(4)
    random_rot_frame[:2,3]=0*array([0.0,0.01]) #camera offset error
    random_rot_frame[:3,:3]=rot_vector_angle(table_object_normal, random_z_angle)
    self.box_pose_out=dot(self.box_pose_out, random_rot_frame)

