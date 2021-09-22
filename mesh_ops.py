import bpy
import math
import random
from functools import lru_cache

DEFAULT_POS = [0, 0, 0]
DEFAULT_TOP_POS = [0, 0, 1]
DEFAULT_EUC = [0, 0, 0]
DEFAULT_SCALE = [1, 1, 1]
DEFAULT_RAD = 1

class Point():
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Point: ({self.x}, {self.y}, {self.z})"

    def __eq__(self, o: object) -> bool:
        if(type(o) != Point):
            return False
        return self.x == o.x and self.y == o.y and self.z == o.z
class Object_Metadata():
    def __init__(self, name = "Temp", pos = DEFAULT_POS, euc = DEFAULT_EUC, scale = DEFAULT_SCALE) -> None:
        self.name = name
        self.position = pos
        self.rotation = euc
        self.scale = scale
    
    def __repr__(self):
        return f"{self.name}: {self.position}, {self.rotation}, {self.scale}"
    
    def __eq__(self, other):
        if(type(other) != Object_Metadata):
            return False
        return self.id == other.id
    
    def pos(self):
        return (self.x, self.y, self.z)

def add_mesh(name = "Test", verts = [], faces = [], edges=[], col_name="Collection"):    
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    
    #print(verts)
    #print(faces)
    #print(edges)
    mesh.from_pydata(verts, edges, faces)
    scene = bpy.context.scene
    scene.collection.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return obj

def mutate_mesh(o_md = Object_Metadata()):
    bpy.context.object.location = o_md.position
    euler = [i/180.0*math.pi for i in o_md.rotation]
    bpy.context.object.rotation_euler = euler
    bpy.context.object.scale = o_md.scale

@lru_cache
def rad_to_point(deg, radius=1, height=0, rotation=0):
    rad = deg/180.0*math.pi
    rotation = rotation/180.0*math.pi
    x = math.sin(rad) * radius
    y = math.cos(rad) * radius
    z = height - math.sin(rotation)*y
    y = math.cos(rotation)*y
    return Point(x, y, z)

def leaf_gen(name = "Leaf", definition = 20, width = 1):
    pass

def frond_gen(name = "Frond", num_edges = 8, base_radius = 0.2, length = 1, gravity = 0.1, leaf_density = 1, width_multiplier = 1, length_multiplier = 1):
    
    sub_stem_gen(name, num_edges, base_radius*.2, length, length/4.0, gravity, length/4.0, False, 0)
    obj = bpy.data.objects[0]
    return obj
    


def sub_stem_gen(name = "Stem", num_edges = 8, base_radius=.2, vert_vel=2, hor_vel=1, gravity=.1, vel_cutoff = -.4, random_bool = False, seed = 0):
    #values to return
    

    if(seed == 0):
        random.seed()
    else:
        random.seed(seed)
    bpy.ops.object.select_all(action='DESELECT')
    if vert_vel == 0:
        vet_vel = .001
    point_list = []
    cylinder_list = []
    y_loc = 0
    z_loc = 0
    temp_vel = vert_vel
    count = 0
    rot = 0
    top_rad = base_radius

    # brute force increment values
    while temp_vel > vel_cutoff:
        temp_vel -= gravity
        count+=1
    if(vel_cutoff < 0):
        max_rot = 180*-vel_cutoff/vert_vel
    else:
        max_rot = 90-(90*vel_cutoff/vert_vel)
    rot_increment = max_rot/(count+1)
    scale_decrement = base_radius/(count+1)
    while vert_vel > vel_cutoff:

        # point calculations
        point_list.append(Point(0, y_loc, z_loc))
        temp = [0, y_loc, z_loc]
        y_loc += hor_vel
        z_loc += vert_vel
        vert_vel -= gravity
        base_rad = top_rad
        top_rad = (top_rad - scale_decrement) if top_rad - scale_decrement > 0 else 0
        temp_rot = rot
        rot +=rot_increment
        top_temp = [0-temp[0], y_loc-temp[1], z_loc-temp[2]]
        
        # stem cylinders
        cyl = cylinder_gen("Cylinder", num_edges, top_temp, top_rad, base_rad, rot, temp_rot, Object_Metadata("Cylinder", temp, DEFAULT_EUC, DEFAULT_SCALE))
        cyl.select_set(False)
        cylinder_list.append(cyl)


    for cyl in cylinder_list:
        cyl.select_set(True)
    bpy.ops.object.join()
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.context.scene.cursor.rotation_euler = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return point_list, scale_decrement

def stem_gen(name = "Stem", num_edges = 8, base_radius=.2, vert_vel=2, hor_vel=1, gravity=.1, vel_cutoff = -.4, random_bool = False, seed = 0):
    
    point_list, scale_dec = sub_stem_gen(name, num_edges, base_radius, vert_vel, hor_vel, gravity, vel_cutoff, random_bool, seed)

    # fronds
    for i, point in enumerate(point_list[:-1]):
        base_radius -= scale_dec
        temp_point = [point.x, point.y, point.z]
        next_point = [point_list[i+1].x, point_list[i+1].y, point_list[i+1].z]
        frond_point = [v + (next_point[i] - v)/2.0 for i, v in enumerate(temp_point)]
        frond_point[0] = base_radius * .9
        frond_right = frond_gen("Frond_R", num_edges, base_radius, 1, .1, 1, 1, 1)
        mutate_mesh(Object_Metadata("Frond_R", frond_point, [120, 180, 90], DEFAULT_SCALE))
        frond_right.select_set(False)
        frond_point[0] = -frond_point[0]
        frond_left = frond_gen("Frond_L", num_edges, base_radius, 1, .1, 1, 1, 1)
        mutate_mesh(Object_Metadata("Frond_L", frond_point, [-90, 0, 90], DEFAULT_SCALE))
        frond_left.select_set(False)

def generate_circle(num_edges, local_pos, radius, rotation):
    sym_flag = False
    if(num_edges % 2 == 1):
        num_edges -= 1
    if(num_edges % 4 == 0):
        sym_flag = True
    q1, q2, q3, q4 = [], [], [], []
    q2e, q4e = [], []
    degree_offset = 360/num_edges
    q1.append(rad_to_point(0, radius, local_pos[2], rotation))
    q3.append(rad_to_point(0, -radius, local_pos[2], rotation))
    if(sym_flag == True):
        q2e.append(Point(radius, 0, local_pos[2]))
        q4e.append(Point(-radius, 0, local_pos[2]))
    for i in range(0, math.ceil(num_edges/4.0)-1):
        curr_deg = (i+1)*degree_offset
        q1p = rad_to_point(curr_deg, radius, local_pos[2], rotation)
        q1.append(q1p)
        q2.append(Point(q1p.x, -q1p.y, 2*local_pos[2] - q1p.z))
        q3.append(Point(-q1p.x, -q1p.y, 2*local_pos[2] - q1p.z))
        q4.append(Point(-q1p.x, q1p.y, q1p.z))
    combined = q1 + q2e + q2[::-1] + q3 + q4e + q4[::-1]
    combined = [(i.x + local_pos[0], i.y + local_pos[1], i.z) for i in combined]
    return combined

def cylinder_gen(name = "Cylinder", num_edges = 4, top_local_pos = DEFAULT_TOP_POS, top_radius = 1, bottom_radius = 1, top_rotation = 0, bottom_rotation = 0, object_metadata = Object_Metadata()):
    faces = []
    verts = [] 
    bottom = generate_circle(num_edges, DEFAULT_POS, bottom_radius, bottom_rotation)
    top = generate_circle(num_edges, top_local_pos, top_radius, top_rotation)
    #print(len(bottom))
    #print(len(top))
    faces = [[i for i in range(len(bottom))]]
    faces += [[i + len(bottom) for i in range(len(top))]]
    faces += [[i, i+1 if i+1 != len(bottom) else 0, i+len(bottom) + 1 if i+1 != len(bottom) else len(bottom), i+len(bottom)] for i in range(len(bottom))]
    verts = bottom
    verts.extend(top)
    cyl = add_mesh(name, verts, faces)
    mutate_mesh(o_md=object_metadata)
    return cyl

def plane_gen(name = "Plane", num_edges = 4, position = DEFAULT_POS, scale = DEFAULT_SCALE, rotation = DEFAULT_EUC):
    verts = [(1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0)]
    faces = [[0, 1, 3, 2]]
    add_mesh(name, verts, faces)