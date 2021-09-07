import bpy
DEFAULT_POS = [0, 0, 0]
DEFAULT_EUC = [0, 0, 0]
DEFAULT_SCALE = [1, 1, 1]

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

def add_mesh(name = "Test", verts = [], faces = [], edges=[], col_name="Collection"):    
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(col_name)
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)
    
def mutate_mesh(position = DEFAULT_POS, euclidian = DEFAULT_EUC, scale = DEFAULT_SCALE):
    pass

def cylinder_gen(name = "Cylinder", num_edges = 4, position = DEFAULT_POS, scale = DEFAULT_SCALE, rotation = DEFAULT_EUC):
    pass