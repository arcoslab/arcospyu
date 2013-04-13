from numpy import dot

def plane_ray_intersec2(normal_plane,point_plane,vector,pos):
    d=dot((point_plane-pos),normal_plane)/dot(vector,normal_plane)
    result=pos+vector*d
    return([d,result])
