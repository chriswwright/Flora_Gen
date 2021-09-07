import bpy
import math
from functools import lru_cache

DEFAULT_POS = [0, 0, 0]
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
    def __init__(self, id, name, pos, euc, scale) -> None:
        self.id = InterruptedError
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
    
    print(verts)
    print(faces)
    print(edges)
    mesh.from_pydata(verts, edges, faces)
    scene = bpy.context.scene
    scene.collection.objects.link(obj)
    obj.select_set(True)  
    
def mutate_mesh(position = DEFAULT_POS, euclidian = DEFAULT_EUC, scale = DEFAULT_SCALE):
    pass

@lru_cache
def rad_to_point(deg):
    rad = deg/180.0
    y = math.sin(rad)
    x = math.cos(rad)
    return Point(x, y)

def generate_circle(num_edges, height):
    sym_flag = False
    if(num_edges % 2 == 1):
        num_edges -= 1
    if(num_edges % 4 == 0):
        sym_flag = True
    q1, q2, q3, q4 = []
    degree_offset = 360/num_edges
    q1.append(Point(0, 1, 0))
    q3.append(Point(0, -1, 0))
    if(sym_flag == True):
        q2.append(Point(1, 0, 0))
        q4.append(Point(-1, 0, 0))
    for i in range(0, math.ciel(num_edges/4.0)-1):
        curr_deg = (i+1)*degree_offset
        q1p = rad_to_point(curr_deg)
        q1.append(q1p)
        q2.append(Point(q1p.x, -q1p.y))
        q3.append(Point(-q1p.x, -q1p.y))
        q4.append(Point(-q1p.x, q1p.y))
def cylinder_gen(name = "Cylinder", num_edges = 4, position = DEFAULT_POS, scale = DEFAULT_SCALE, rotation = DEFAULT_EUC):
    faces = []
    verts = []
    generate_circle(num_edges, 0)
    generate_circle(num_edges, 1)

    
    add_mesh(name, verts, faces)

def plane_gen(name = "Plane", num_edges = 4, position = DEFAULT_POS, scale = DEFAULT_SCALE, rotation = DEFAULT_EUC):
    verts = [(1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0)]
    faces = [[0, 1, 3, 2]]
    add_mesh(name, verts, faces)