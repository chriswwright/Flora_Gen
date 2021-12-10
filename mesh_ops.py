import bpy
import mathutils
import math
import random
import time
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

class Stick_Node():
    def __init__(self, iterations = 0, position = DEFAULT_POS, locked = False, angle = 0, offset = 0):
        self.iterations = iterations
        self.position = position
        self.locked = locked
        self.angle = angle
        self.offset = offset

def apply_values(o_md = Object_Metadata()):
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    mutate_mesh(o_md = o_md)

def add_mesh(name = "Test", verts = [], faces = [], edges=[], col_name="Collection"):    
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
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
def rad_to_point(deg, radius=1, height=0, rotation=0, rotate_axis = 0):
    rad = deg/180.0*math.pi
    rotation = rotation/180.0*math.pi
    if(rotate_axis == 0):
        x = math.sin(rad) * radius
        y = math.cos(rad) * radius
        z = height - math.sin(rotation)*y
        y = math.cos(rotation)*y
    else:
        x = math.sin(rad) * radius
        y = math.cos(rad) * radius
        z = height + math.sin(rotation)*x
        x = math.cos(rotation)*x
    return Point(x, y, z)

def sub_stem_gen(name = "Stem", num_edges = 8, base_radius=.2, vert_vel=2, hor_vel=1, gravity=.1, vel_cutoff = -.4, random_bool = False, seed = 0, random_weight=0.5, drift_bool = False, drift = 0, left = False):
    # if seed == 0:
    #     seed = time.time()
    # random.seed(seed)
    if(drift_bool == False):
        drift = 0
    drift = (drift if drift < 0 else -drift)
    if(left == False):
        drift = -drift
    bpy.ops.object.select_all(action='DESELECT')
    if vert_vel == 0:
        vert_vel = .001
    if(random_bool == True):
      vert_vel = vert_vel*(1+((random.random()-0.5)*0.25)*random_weight)
      hor_vel = hor_vel*(1+((random.random()-0.5)*0.25)*random_weight)
      gravity = gravity*(1+((random.random()-0.5)*0.25)*random_weight)
      vel_cutoff = vel_cutoff + (random.random()*.1*random_weight-.05)
    point_list = []
    cylinder_list = []
    y_loc = 0
    z_loc = 0
    temp_vel = vert_vel
    count = 0
    rot = 0
    top_rad = base_radius
    x_drift = 0
    drift_off = 0
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
    drift_inc = drift/(count+1)
    while vert_vel > vel_cutoff:
        # point calculations
        point_list.append(Point(x_drift, y_loc, z_loc))
        temp = [x_drift, y_loc, z_loc]
        drift_off += drift_inc
        x_drift += drift_off
        y_loc += hor_vel
        z_loc += vert_vel
        vert_vel -= gravity
        base_rad = top_rad
        top_rad = (top_rad - scale_decrement) if top_rad - scale_decrement > 0 else 0
        temp_rot = rot
        rot +=rot_increment
        top_temp = [x_drift-temp[0], y_loc-temp[1], z_loc-temp[2]]
        
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

    return point_list

def sub_curve_gen(name = "Grass_Frond", num_edges = 8, base_radius=.2, vert_vel=2, hor_vel=1, gravity=.1, vel_cutoff = -.4, degree_max = 20, random_bool = False, seed = 0, random_weight=0.5, drift_bool = False, drift = 0, left = False):
    # if seed == 0:
    #     seed = time.time()
    # random.seed(seed)
    if(drift_bool == False):
        drift = 0
    drift = (drift if drift < 0 else -drift)
    if(left == False):
        drift = -drift
    bpy.ops.object.select_all(action='DESELECT')
    if vert_vel == 0:
        vert_vel = .001
    if(random_bool == True):
      vert_vel = vert_vel*(1+((random.random()-0.5)*0.25)*random_weight)
      hor_vel = hor_vel*(1+((random.random()-0.5)*0.25)*random_weight)
      gravity = gravity*(1+((random.random()-0.5)*0.25)*random_weight)
      vel_cutoff = vel_cutoff + (random.random()*.1*random_weight-.05)
    point_list = []
    cylinder_list = []
    y_loc = 0
    z_loc = 0
    temp_vel = vert_vel
    count = 0
    rot = 0
    top_rad = base_radius
    x_drift = 0
    drift_off = 0
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
    drift_inc = drift/(count+1)
    while vert_vel > vel_cutoff:
        # point calculations
        point_list.append(Point(x_drift, y_loc, z_loc))
        temp = [x_drift, y_loc, z_loc]
        drift_off += drift_inc
        x_drift += drift_off
        y_loc += hor_vel
        z_loc += vert_vel
        vert_vel -= gravity
        base_rad = top_rad
        top_rad = (top_rad - scale_decrement) if top_rad - scale_decrement > 0 else 0
        temp_rot = rot
        rot +=rot_increment
        top_temp = [x_drift-temp[0], y_loc-temp[1], z_loc-temp[2]]
        
        # stem cylinders
        cyl = curve_gen("Cylinder", num_edges, top_temp, top_rad, base_rad, rot, temp_rot, degree_max, Object_Metadata("Cylinder", temp, DEFAULT_EUC, DEFAULT_SCALE))
        cyl.select_set(False)
        cylinder_list.append(cyl)

    for cyl in cylinder_list:
        cyl.select_set(True)
    bpy.ops.object.join()
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.context.scene.cursor.rotation_euler = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return point_list

def leaf_gen(name = "Leaf", step_res = 1.0, length = 1, gravity = .1, width = .2, random_bool = False, seed = 0):
    if(random_bool == True):
        random.seed(seed)
    vel_cutoff = 0
    velocity = length*width
    gravity = gravity*width
    hor_vol = length/(4*step_res)
    offset = length/4.0
    position = [0, offset]
    verts = [(0, -offset, 0), (0, offset, 0)]
    top =[]
    bottom = []
    while(velocity > vel_cutoff):
        position[1] += velocity/step_res
        velocity -= gravity/step_res
        position[0] += hor_vol
        top.append((position[0], position[1], 0))
        bottom.append((position[0], -position[1], 0))
    gravity /= 2.0
    while(position[1] > 0):
        position[1] += velocity/step_res
        velocity -= gravity/step_res
        position[0] += hor_vol
        top.append((position[0], max(position[1], 0), 0))
        bottom.append((position[0], min(-position[1], 0) ,0))       
    delta = .05
    for i, pos in enumerate(top[:]):
        if i > len(top)-4:
           top[i] = (pos[0], pos[1]+delta*top[0][0], 0)
           bottom[i] = (pos[0], -pos[1]+delta*top[0][0], 0)
           delta += .05
    verts = verts + top + bottom[::-1]
    face = [i for i in range(len(verts))]
    faces = [face]
    leaf = add_mesh(name, verts, faces)
    return leaf

def fern_gen(name = "Fern", num_edges = 8, base_radius=.2, vert_vel=2, hor_vel=1, gravity=.1, vel_cutoff = -.4, frond_len = 1, resolution = 1.0, random_bool = False, seed = 0, random_weight = 1.0, drift_bool = False, drift_weight = 0.0, fern_radius = 1.0, num_stalks = 3, reseed = True):
    bpy.ops.object.select_all(action='DESELECT')   
    if seed == 0:
        seed = time.time()
    if(reseed == True):
        random.seed(seed)
    stem_list = []
    cur_deg = 0
    for i in range(0, num_stalks):
        z_rot = (cur_deg + (0 if random_bool == False else (random.random()-.5)*60/num_stalks))
        extension = (fern_radius + (0 if random_bool == False else (random.random()-0.5)*fern_radius))
        degree_inc = 360/num_stalks + (0 if random_bool == False else (random.random() - .5)*20)
        cur_deg += degree_inc
        obj = stem_gen(name = "Stem", num_edges=num_edges, base_radius=base_radius, vert_vel=vert_vel, hor_vel=hor_vel, gravity=gravity, vel_cutoff=vel_cutoff, frond_len=frond_len, resolution=resolution, random_bool=random_bool, seed=seed, random_weight=random_weight, drift_bool=drift_bool, drift_weight=drift_weight)
        bpy.context.object.location = [-math.sin(z_rot/180*math.pi) * extension, math.cos(z_rot/180*math.pi) * extension, 0]
        bpy.ops.transform.rotate(value=z_rot/180*math.pi + (0 if random_bool == False else (random.random()-.5)*random_weight), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        stem_list.append(obj)
        obj.select_set(False)
    for stem in stem_list:
        stem.select_set(True)
    bpy.ops.object.join()
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.context.scene.cursor.rotation_euler = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    obj = bpy.context.selected_objects[0]
    return obj

def frond_gen(name = "Frond", num_edges = 8, base_radius = 0.2, length = 1, gravity = 0.1, leaf_density = 1, leaf_width = 0.2, leaf_len = 0.5, length_multiplier = 1, resolution = 1, random_bool = False, seed = 0, random_weight = 1.0, drift_bool = False, drift_weight = 0, left = False):
    if(seed == 0):
        seed = time.time
        random.seed(seed)
    bpy.ops.object.select_all(action='DESELECT')
    base_radius*=.2+(random.random()-.5)*.1
    drift = (0 if not drift_bool else (random.random()*drift_weight))
    point_list = sub_stem_gen(name, num_edges, base_radius, length, length/4.0, .1, length/4.0, random_bool, seed, random_weight, drift_bool, drift, left)
    if(len(bpy.context.selected_objects) == 0):
        return None
    obj = bpy.context.selected_objects[0]
    # leaves
    leaf_list = []
    scale_dec = base_radius/(max(len(point_list)-1, 1))
    leaf_len_dec = leaf_len/(max(len(point_list)-1, 1))*.5
    rot_inc = 45/(max(len(point_list) - 1, 1))
    rot = 0
    for i, point in enumerate(point_list[:-1]):
        base_radius -= scale_dec
        leaf_len -= leaf_len_dec
        if(random_bool == True):
            leaf_point = [(base_radius * .9) + point_list[i+1].x, (point.y + (random.random()*.5+.75)*(point_list[i+1].y-point.y)/2.0), point.z+ (random.random()*.5+.75)*(point_list[i+1].z-point.z)/2.0]
        else:
            leaf_point = [base_radius * .9 + point_list[i+1].x, (point.y + (point_list[i+1].y-point.y)/2.0), point.z+ (point_list[i+1].z-point.z)/2.0]
        leaf = leaf_gen("Leaf", float(resolution), leaf_len, .1, width=leaf_width)
        mutate_mesh(Object_Metadata("Leaf", leaf_point, [80-rot, 0, 0], DEFAULT_SCALE))
        leaf_list.append(leaf)
        leaf.select_set(False)
        leaf_point[0] = leaf_point[0]-(base_radius*1.8)
        leaf = leaf_gen("Leaf", float(resolution), leaf_len, .1, width=leaf_width)
        mutate_mesh(Object_Metadata("Leaf", leaf_point, [-80+rot, 0, 180], DEFAULT_SCALE))
        leaf_list.append(leaf)
        leaf.select_set(False)
        rot+=rot_inc
    obj.select_set(True)
    for leaf in leaf_list:
        leaf.select_set(True)
    bpy.ops.object.join()
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.context.scene.cursor.rotation_euler = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    obj = bpy.context.selected_objects[0]
    return obj

def stem_gen(name = "Stem", num_edges = 8, base_radius=.2, vert_vel=2, hor_vel=1, gravity=.1, vel_cutoff = -.4, frond_len = 1, resolution = 1.0, random_bool = False, seed = 0, random_weight = 1.0, drift_bool = False, drift_weight = 0.0):
    if seed == 0:
        seed = time.time()
        random.seed(seed)
    bpy.ops.object.select_all(action='DESELECT')
    point_list = sub_stem_gen(name, num_edges, base_radius, vert_vel, hor_vel, gravity, vel_cutoff, random_bool, seed, random_weight*5, drift_bool, drift_weight, (True if random.random() > .5 else False))
    obj = bpy.context.selected_objects[0]
    
    # fronds
    fronds = []
    scale_dec = base_radius/(len(point_list)-1)
    frond_dec = frond_len/(len(point_list)-1)*.5
    frond_dec_control = frond_len/len(point_list)/len(point_list)
    width_scale = len(point_list)*.01
    frond_len *= 1+width_scale
    if(vel_cutoff < 0):
        max_rot = 180*-vel_cutoff/vert_vel
    else:
        max_rot = 90-(90*vel_cutoff/vert_vel)
    rot_inc = max_rot/(len(point_list)-1)
    curr_rot = rot_inc*2
    for i, point in enumerate(point_list[2:-1]):
        frond_len -= frond_dec
        base_radius -= scale_dec
        temp_point = [point.x, point.y, point.z]
        next_point = [point_list[i+1].x, point_list[i+1].y, point_list[i+1].z]
        frond_point = [v + (next_point[i] - v)/2.0 for i, v in enumerate(temp_point)]
        frond_point[0] += base_radius * .9
        frond_right = frond_gen("Frond_R", num_edges, base_radius, frond_len, gravity, 1, 0.2*frond_len, 0.5*frond_len, 1, resolution, random_bool, seed, random_weight, drift_bool, drift_weight)
        if(frond_right == None):
            curr_rot+=rot_inc
            continue
        mutate_mesh(Object_Metadata("Frond_R", frond_point, [40, curr_rot-60, 90], DEFAULT_SCALE))
        frond_right.select_set(False)
        frond_point[0] -= base_radius * 1.8
        frond_left = frond_gen("Frond_L", num_edges, base_radius, frond_len, gravity, 1, 0.2*frond_len, 0.5*frond_len, 1, resolution, random_bool, seed, random_weight, drift_bool, drift_weight, True)
        if(frond_left == None):
            curr_rot+=rot_inc
            continue
        mutate_mesh(Object_Metadata("Frond_L", frond_point, [40, 60-curr_rot, -90], DEFAULT_SCALE))
        frond_left.select_set(False)
        fronds.append(frond_left)
        fronds.append(frond_right)
        curr_rot+=rot_inc
        frond_dec += frond_dec_control

    obj.select_set(True)
    for frond in fronds:
        frond.select_set(True)
    bpy.ops.object.join()
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.context.scene.cursor.rotation_euler = (0.0, 0.0, 0.0)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_interior_faces()
    bpy.ops.mesh.delete(type='ONLY_FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    obj = bpy.context.selected_objects[0]
    return obj

def generate_circle(num_edges, local_pos, radius, rotation, rotate_axis):
    sym_flag = False
    if(num_edges % 2 == 1):
        num_edges -= 1
    if(num_edges % 4 == 0):
        sym_flag = True
    q1, q2, q3, q4 = [], [], [], []
    q2e, q4e = [], []
    degree_offset = 360/num_edges
    if(rotate_axis == 0):
        q1.append(rad_to_point(0, radius, local_pos[2], rotation, rotate_axis))
        q3.append(rad_to_point(180, radius, local_pos[2], rotation, rotate_axis))
        if(sym_flag == True):
            q2e.append(rad_to_point(90, radius, local_pos[2], rotation, rotate_axis))
            q4e.append(rad_to_point(270, radius, local_pos[2], rotation, rotate_axis))
        for i in range(0, math.ceil(num_edges/4.0)-1):
            curr_deg = (i+1)*degree_offset
            q1p = rad_to_point(curr_deg, radius, local_pos[2], rotation, rotate_axis)
            q1.append(q1p)
            q2.append(Point(q1p.x, -q1p.y, 2*local_pos[2] - q1p.z))
            q3.append(Point(-q1p.x, -q1p.y, 2*local_pos[2] - q1p.z))
            q4.append(Point(-q1p.x, q1p.y, q1p.z))
    else:
        q1.append(rad_to_point(0, radius, local_pos[2], rotation, rotate_axis))
        q3.append(rad_to_point(180, radius, local_pos[2], rotation, rotate_axis))
        if(sym_flag == True):
            q2e.append(rad_to_point(90, radius, local_pos[2], rotation, rotate_axis))
            q4e.append(rad_to_point(270, radius, local_pos[2], rotation, rotate_axis))
        for i in range(0, math.ceil(num_edges/4.0)-1):
            curr_deg = (i+1)*degree_offset
            q1p = rad_to_point(curr_deg, radius, local_pos[2], rotation, rotate_axis)
            q1.append(q1p)
            q2.append(Point(q1p.x, -q1p.y, q1p.z))
            q3.append(Point(-q1p.x, -q1p.y, 2*local_pos[2] - q1p.z))
            q4.append(Point(-q1p.x, q1p.y, 2*local_pos[2] - q1p.z))


    combined = q1 + q2e + q2[::-1] + q3 + q4e + q4[::-1]
    combined = [(i.x + local_pos[0], i.y + local_pos[1], i.z) for i in combined]
    return combined

def generate_curve(num_edges, local_pos, radius, rotation, degree_max):
    resolution = num_edges * 360/degree_max
    num_edges+=2
    if(num_edges % 2 == 1):
        num_edges -= 1
    q1, q4 = [], []
    degree_offset = 360/resolution
    q1.append(rad_to_point(0, radius, local_pos[2], rotation))
    for i in range(0, math.ceil(num_edges/2.0)-1):
        curr_deg = (i+1)*degree_offset
        q1p = rad_to_point(curr_deg, radius, local_pos[2], rotation)
        q1.append(q1p)
        q4.append(Point(-q1p.x, q1p.y, q1p.z))
    combined = q4[::-1] + q1
    combined = [(i.x + local_pos[0], radius - (i.y - local_pos[1]), i.z) for i in combined]
    return combined

def cylinder_gen(name = "Cylinder", num_edges = 4, top_local_pos = DEFAULT_TOP_POS, top_radius = 1, bottom_radius = 1, top_rotation = 0, bottom_rotation = 0, object_metadata = Object_Metadata(), base_face = True, top_face = True, rotate_axis = 0):
    faces = []
    verts = [] 
    bottom = generate_circle(num_edges, DEFAULT_POS, bottom_radius, bottom_rotation, rotate_axis)
    top = generate_circle(num_edges, top_local_pos, top_radius, top_rotation, rotate_axis)
    #print(len(bottom))
    #print(len(top))
    if(base_face == True):
        faces = [[i for i in range(len(bottom))]]
    else:
        faces = []
    if(top_face == True):
        faces += [[i + len(bottom) for i in range(len(top))]]
    faces += [[i, i+1 if i+1 != len(bottom) else 0, i+len(bottom) + 1 if i+1 != len(bottom) else len(bottom), i+len(bottom)] for i in range(len(bottom))]
    verts = bottom
    verts.extend(top)
    cyl = add_mesh(name, verts, faces)
    mutate_mesh(o_md=object_metadata)
    return cyl

def curve_gen(name = "Curve", num_edges = 8, top_local_pos = DEFAULT_TOP_POS, top_radius = 1, bottom_radius = 1, top_rotation = 0, bottom_rotation = 0, degree_max = 20, object_metadata = Object_Metadata()):
    faces = []
    verts = [] 
    bottom = generate_curve(num_edges, DEFAULT_POS, bottom_radius, bottom_rotation, degree_max)
    top = generate_curve(num_edges, top_local_pos, top_radius, top_rotation, degree_max)
    #print(len(bottom))
    #print(len(top))
    faces += [[i, i+1, i+len(bottom) + 1, i+len(bottom)] for i in range(len(bottom)-1)]
    verts = bottom
    verts.extend(top)
    curve = add_mesh(name, verts, faces)
    mutate_mesh(o_md=object_metadata)
    return curve

def grass_gen(name = "Grass", num_edges = 8, base_radius=.2, vert_vel=2, hor_vel=1, gravity=.1, vel_cutoff = -.4, grass_radius = 0.5, resolution = 1.0, degree_max = 20, num_curve = 5, random_bool = False, seed = 0, random_weight = 1.0, drift_bool = False, drift_weight = 0.0, reseed = True):
    if seed == 0:
        seed = time.time()
    if(reseed == True):
        random.seed(seed)
    grass_list = []
    bpy.ops.object.select_all(action='DESELECT')
    for i in range(num_curve):
        sub_curve_gen("Grass_Stem", num_edges, base_radius, vert_vel, hor_vel, gravity, vel_cutoff, degree_max, random_bool, seed, random_weight, drift_bool, drift_weight, (True if random_bool is False else (True if random.random() > .5 else False)))
        obj = bpy.context.selected_objects[0]
        rotate_val=random.random()*2*math.pi + (0 if random_bool == False else (random.random()-.5)*random_weight)
        bpy.context.object.location = [-math.sin(rotate_val) * grass_radius * (random.random()+.2 if random_bool == True else 0), math.cos(rotate_val) * grass_radius * (random.random()+.2 if random_bool == True else 0), 0]
        bpy.ops.transform.rotate(value= rotate_val, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)        
        grass_list.append(obj)
        obj.select_set(False)
    for obj in grass_list:
        obj.select_set(True)
    bpy.ops.object.join()
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.context.scene.cursor.rotation_euler = (0.0, 0.0, 0.0)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')

def noise_gen(name = "Noise Plane", grid_len = 10, grid_width = 10, resolution = 1, height_scalar = 1, h_scale = 3, lacunarity = 1, octaves = 2, offset = 1, x_shift = 0, y_shift = 0, random_bool = False, seed = 0, random_weight = 1):
    if(random_bool == True and seed == 0):
        seed = time.time()
    if(random_bool == True):
        if(x_shift == 0):
            x_shift = time.time()*31%10000
            y_shift = time.time()*17%10000
    random.seed(seed)
    x_traverse = grid_width * resolution
    y_traverse = grid_len * resolution
    verts = [(x/resolution, 
             y/resolution,
             height_scalar*mathutils.noise.hetero_terrain(mathutils.Vector((x*0.1/resolution + x_shift, y*0.1/resolution + y_shift, 0.0)),
                                            h_scale, 
                                            lacunarity, 
                                            octaves, 
                                            offset))
             for x in range(int(x_traverse))
             for y in range(int(y_traverse))]
    faces = []
    add_mesh(name, verts, faces)    

def rock_gen(name = "Rock", rock_radius = 5, resolution = 1, height_scalar = 1, num_rings = 5,
             h_scale = 3, lacunarity = 1, octaves = 2, offset = 1, x_shift = 0, y_shift = 0,
             random_bool = False, seed = 0, random_weight = 1, reseed = True):
    bpy.ops.object.select_all(action='DESELECT')
    num_points = 4*resolution
    verts = []
    faces = []
    if seed == 0:
        seed = time.time()
    if(reseed == True):
        random.seed(seed)
    if(random_bool == True):
        if(x_shift == 0):
            x_shift = time.time()*31%10000
            y_shift = time.time()*17%10000
    random.seed(seed)
    x_traverse = rock_radius * resolution
    y_traverse = rock_radius * resolution
    noise_basii =  (
        'BLENDER', 
        'PERLIN_ORIGINAL', 
        'PERLIN_NEW', 
        'VORONOI_F1', 
        'VORONOI_F2', 
        'VORONOI_F3', 
        'VORONOI_F4', 
        'VORONOI_F2F1', 
        'VORONOI_CRACKLE', 
        'CELLNOISE')
    x_scalar = random.random()+.1
    y_scalar = random.random()+.1
    rock_holder = [generate_circle(num_points, DEFAULT_POS, rock_radius*math.cos((math.pi * i * 0.5)/num_rings), 0, 0) for i in range(0, num_rings)]
    rock_holder.append([(0, 0, rock_radius)])
    for i, ring in enumerate(rock_holder):
        for j, vert in enumerate(ring):
            if i != num_rings:
                current = ((num_points*i)+j)
                next = (current + 1 if current + 1 != num_points*(i+1) else num_points*i)
                if i == num_rings - 1:
                    faces.append([current, next, num_rings*num_points])
                else:
                    faces.append([current, next, next + num_points, current+num_points])
        h = rock_radius*math.sin((math.pi * i * 0.5)/num_rings)*height_scalar
        for j, vert in enumerate(ring):
            ring[j] = ((vert[0]+(random.random()+.5))*x_scalar, (vert[1]+(random.random()+.5))*y_scalar, h*mathutils.noise.hetero_terrain(mathutils.Vector((vert[0]*0.1/resolution + x_shift, vert[1]*0.1/resolution + y_shift, 0.0)),
                                            h_scale, 
                                            lacunarity, 
                                            octaves, 
                                            offset))
        verts.extend(ring)
    faces.append([i for i in range(num_points)])
    # verts = [(x/resolution, 
    #          y/resolution,
    #          height_scalar*mathutils.noise.hetero_terrain(mathutils.Vector((x*0.1/resolution + x_shift, y*0.1/resolution + y_shift, 0.0)),
    #                                         h_scale, 
    #                                         lacunarity, 
    #                                         octaves, 
    #                                         offset))
    #          for x in range(int(x_traverse))
    #          for y in range(int(y_traverse))]
    add_mesh(name, verts, faces)    

def stick_gen( name = "Stick", num_edges = 4, height = 1, base_width = .4, end_width = .4, resolution = 1.0, mutate_chance = 0.2, max_perm = 20, degree_offset = 20, random_bool = False, seed = 0, random_weight = 1, reseed = True):
    bpy.ops.object.select_all(action='DESELECT')  
    if seed == 0:
        seed = time.time()
    if(reseed == True):
        random.seed(seed)
    offset_scalar = random_weight / 3
    degree_offset = degree_offset
    euc_movement = [-90, 0, 0]
    cylinder_list = []
    point_list = []
    max_perm *= resolution
    height = height/resolution
    mutate_chance = mutate_chance/resolution
    width_decrementor = (base_width - end_width)/max_perm
    queue = [Stick_Node(max_perm, DEFAULT_POS, False, 0)]
    while(len(queue) > 0):
        current = queue[0]
        queue = queue[1::]
        if(current.iterations > 0):
            if(mutate_chance > random.random()):
                if(math.ceil(random.random()*2) == 2):
                    deg_1 = (random.random()-.5)*degree_offset + current.angle
                    deg_2 = (random.random()-.5)*degree_offset*2 + current.angle
                    if(deg_1 > 0 and deg_2 > 0 or deg_1 < 0 and deg_2 < 0):
                        deg_2 = -deg_2 
                    rad_1 = deg_1 / 180 * math.pi
                    rad_2 = deg_2 / 180 * math.pi
                    pos_1 = [current.position[0] + height * math.sin(rad_1), current.position[1], current.position[2] + height * math.cos(rad_1)]
                    pos_2 = [current.position[0] + height * math.sin(rad_2), current.position[1], current.position[2] + height * math.cos(rad_2)]
                    offset = (0 if random_bool == False else (random.random() - 0.5)*offset_scalar)
                    queue.append(Stick_Node(int(current.iterations*.5), [current.position[0] + height * math.sin(rad_1), current.position[1] + height * math.cos(rad_1), current.position[2]], True, rad_1, offset))
                    cyl = cylinder_gen(name, num_edges, 
                                [x_i - y_i for x_i, y_i in zip(pos_1, current.position)],
                                base_width - width_decrementor* (max_perm - int(current.iterations * .5)) + offset * (base_width - width_decrementor* (max_perm - int(current.iterations * .5))),
                                base_width - width_decrementor* (max_perm - (current.iterations)) + current.offset * (base_width - width_decrementor* (max_perm - (current.iterations))),
                                -deg_1, -current.angle*180/math.pi,
                                Object_Metadata(name, current.position, euc_movement),
                                (True if current.iterations == max_perm else False),
                                (True if int(current.iterations * .5) == 0 else False),
                                 1)
                    cyl.select_set(False)
                    cylinder_list.append(cyl)
                    offset = (0 if random_bool == False else (random.random() - 0.5)*offset_scalar)
                    queue.append(Stick_Node(int(current.iterations*.25), [current.position[0] + height * math.sin(rad_2), current.position[1] + height * math.cos(rad_2), current.position[2]], True, rad_2, offset))
                    cyl = cylinder_gen(name, num_edges, 
                                [x_i - y_i for x_i, y_i in zip(pos_2, current.position)], 
                                base_width - width_decrementor* (max_perm - int(current.iterations * .25)) + offset * (base_width - width_decrementor* (max_perm - int(current.iterations * .25))),
                                base_width - width_decrementor* (max_perm - (current.iterations)) + current.offset * (base_width - width_decrementor* (max_perm - (current.iterations))),
                                 -deg_2, -current.angle*180/math.pi,
                                Object_Metadata(name, current.position, euc_movement),
                                (True if current.iterations == max_perm else False),
                                (True if int(current.iterations * .25) == 0 else False),
                                 1)
                    cyl.select_set(False)
                    cylinder_list.append(cyl)
                else:
                    deg_1 = (random.random()-.5 + (.1 if current.angle > 0 else -.1))*degree_offset + current.angle
                    rad_1 = deg_1 / 180 * math.pi
                    pos_1 = [current.position[0] + height * math.sin(rad_1), current.position[1], current.position[2] + height * math.cos(rad_1)]
                    offset = (0 if random_bool == False else (random.random() - 0.5)*offset_scalar)
                    queue.append(Stick_Node(int(current.iterations * .75), [current.position[0] + height * math.sin(rad_1), current.position[1] + height * math.cos(rad_1), current.position[2]], True, rad_1, offset))
                    cyl = cylinder_gen(name, num_edges, 
                                [x_i - y_i for x_i, y_i in zip(pos_1, current.position)], 
                                base_width - width_decrementor* (max_perm - int(current.iterations * .75)) + offset * (base_width - width_decrementor* (max_perm - int(current.iterations * .75))),
                                base_width - width_decrementor* (max_perm - (current.iterations)) + current.offset * (base_width - width_decrementor* (max_perm - (current.iterations))),
                                 -deg_1, -current.angle*180/math.pi,
                                Object_Metadata(name, current.position, euc_movement),
                                (True if current.iterations == max_perm else False),
                                (True if int(current.iterations * .5) == 0 else False),
                                 1)
                    cyl.select_set(False)
                    cylinder_list.append(cyl)
            else:
                if(current.locked):
                    pos_1 = [current.position[0] + height * math.sin(current.angle), current.position[1], current.position[2] + height * math.cos(current.angle)]
                    offset = (0 if random_bool == False else (random.random() - 0.5)*offset_scalar)
                    queue.append(Stick_Node(int(current.iterations-1), [current.position[0] + height * math.sin(current.angle), current.position[1] + height * math.cos(current.angle), current.position[2]], True, current.angle, offset))
                    cyl = cylinder_gen(name, num_edges, 
                                [x_i - y_i for x_i, y_i in zip(pos_1, current.position)], 
                                base_width - width_decrementor* (max_perm - (current.iterations - 1)) + offset * (base_width - width_decrementor* (max_perm - (current.iterations - 1))),
                                base_width - width_decrementor* (max_perm - (current.iterations)) + current.offset * (base_width - width_decrementor* (max_perm - (current.iterations))),
                                -current.angle*180/math.pi, -current.angle*180/math.pi,
                                Object_Metadata(name, current.position, euc_movement),
                                (True if current.iterations == max_perm else False),
                                (True if current.iterations - 1 == 0 else False),
                                 1)
                    cyl.select_set(False)
                    cylinder_list.append(cyl)
                else:
                    pos_1 = [current.position[0] + 0, current.position[1], current.position[2] + height]
                    offset = (0 if random_bool == False else (random.random() - 0.5)*offset_scalar)
                    queue.append(Stick_Node(int(current.iterations-1), [current.position[0] + 0, current.position[1] + height, current.position[2]], False, 0, offset))
                    cyl = cylinder_gen(name, num_edges, 
                                [x_i - y_i for x_i, y_i in zip(pos_1, current.position)], 
                                base_width - width_decrementor* (max_perm - (current.iterations - 1)) + offset * (base_width - width_decrementor* (max_perm - (current.iterations - 1))),
                                base_width - width_decrementor* (max_perm - (current.iterations))+ current.offset * (base_width - width_decrementor* (max_perm - (current.iterations))),
                                0, 0,
                                Object_Metadata(name, current.position, euc_movement),
                                (True if current.iterations == max_perm else False),
                                (True if current.iterations - 1 == 0 else False),
                                 1)
                    cyl.select_set(False)
                    cylinder_list.append(cyl)

    for cyl in cylinder_list:
        cyl.select_set(True)
    bpy.ops.object.join()
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.context.scene.cursor.rotation_euler = (0.0, 0.0, 0.0)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    obj = bpy.context.selected_objects[0]
    return obj

def grass_tile_gen( name = "Grass Tile", grid_len = 10, grid_width = 10, density = 1, spawn_offset = 1, selection_pool = 5,
                    num_cols = 8, base_radius=.2, vert_vel=2, hor_vel=1, gravity=.1, vel_cutoff = -.4, grass_radius = 0.5, detail = 1.0, degree_max = 20, num_curve = 5,
                    h_scale = 3, lacunarity = 1, octaves = 2, offset = 1,
                    x_shift = 0, y_shift = 0,
                    random_bool = False, seed = 0, random_weight = 1, drift_bool = False, drift_weight = 0):
    pool = []
    for i in range(selection_pool):
        grass_gen(  name = "Grass", 
                    num_edges=num_cols,
                    base_radius=base_radius,
                    vert_vel=vert_vel,
                    hor_vel=hor_vel,
                    gravity=gravity,
                    vel_cutoff=vel_cutoff,
                    grass_radius=grass_radius,
                    resolution=detail,
                    degree_max=degree_max,
                    num_curve=num_curve,
                    random_bool=random_bool,
                    random_weight=random_weight,
                    drift_bool=drift_bool,
                    drift_weight=drift_weight,
                    reseed=True)
        obj = bpy.context.selected_objects[0]
        pool.append(obj)
        obj.select_set(False)

    #grass_gen(name = "Grass", num_edges=num_cols, base_radius=base_radius, vert_vel=vert_vel, hor_vel=hor_vel, gravity=gravity, vel_cutoff=vel_cutoff, grass_radius=grass_radius, resolution=detail, degree_max=degree_max, num_curve=num_curve)
    x_traverse = grid_width / spawn_offset
    y_traverse = grid_len / spawn_offset
    verts = [(x*spawn_offset - (grid_width/2), 
             y*spawn_offset - (grid_len/2),
             mathutils.noise.hetero_terrain(mathutils.Vector((x*0.1*spawn_offset + x_shift, y*0.1*spawn_offset + y_shift, 0.0)),
                                            h_scale, 
                                            lacunarity, 
                                            octaves, 
                                            offset))
             for x in range(int(x_traverse))
             for y in range(int(y_traverse))]
    faces = []
    i = 0
    for vert in verts:
        if vert[2] > 4/density:
            i = (i + 1) % selection_pool
            obj = pool[i]
            obj.select_set(True)
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(vert[0], vert[1], 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
            obj.select_set(False)
            bpy.ops.transform.rotate(value=random.random()*2*math.pi, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            obj = bpy.context.selected_objects[0]
            obj.select_set(False)
    for obj in pool:
        obj.select_set(True)
        bpy.ops.object.delete()
    #add_mesh(name, verts, faces) 

def multi_tile_gen( name = "Multi Tile", grid_len = 10, grid_width = 10, density = 1, spawn_offset = 1, selection_pool = 5,
                    function_select = 0, al = [],
                    h_scale = 3, lacunarity = 1, octaves = 2, offset = 1, shift_bool = False,
                    x_shift = 0, y_shift = 0,
                    random_bool = False, seed = 0, random_weight = 1, drift_bool = False, drift_weight = 0, reseed = True):
    #kill case
    if seed == 0:
        seed = time.time()
    if(reseed == True):
        random.seed(seed)
    if(shift_bool == True):
        x_shift = (random.random()-.5)*20000
        y_shift = (random.random()-.5)*20000
    if(function_select < 1 or function_select > 4):
        return 
    pool = []
    for i in range(selection_pool):
        if(function_select == 1):
            fern_gen(*al)
        elif(function_select == 2):
            grass_gen(*al)
        elif(function_select == 3):
            rock_gen(*al)
        else:
            stick_gen(*al)
        obj = bpy.context.selected_objects[0]
        pool.append(obj)
        obj.select_set(False)
    x_traverse = grid_width / spawn_offset
    y_traverse = grid_len / spawn_offset
    verts = [(x*spawn_offset - (grid_width/2), 
             y*spawn_offset - (grid_len/2),
             mathutils.noise.hetero_terrain(mathutils.Vector((x*0.1*spawn_offset + x_shift, y*0.1*spawn_offset + y_shift, 0.0)),
                                            h_scale, 
                                            lacunarity, 
                                            octaves, 
                                            offset))
             for x in range(int(x_traverse))
             for y in range(int(y_traverse))]
    faces = []
    i = 0
    for vert in verts:
        if vert[2] > 4/density:
            i = (i + 1) % selection_pool
            obj = pool[i]
            obj.select_set(True)
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(vert[0], vert[1], 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
            obj.select_set(False)
            bpy.ops.transform.rotate(value=random.random()*2*math.pi, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            obj = bpy.context.selected_objects[0]
            obj.select_set(False)
    for obj in pool:
        obj.select_set(True)
        bpy.ops.object.delete()
    #add_mesh(name, verts, faces) 

def plane_gen(name = "Plane", num_edges = 4, position = DEFAULT_POS, scale = DEFAULT_SCALE, rotation = DEFAULT_EUC):
    verts = [(1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0)]
    faces = [[0, 1, 3, 2]]
    add_mesh(name, verts, faces)