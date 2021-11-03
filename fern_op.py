from . import mesh_ops
import bpy

class FLORA_GEN_PT_FernOperator(bpy.types.Operator):
    bl_idname = "wm.fern_operator"
    bl_label = "Fern Operator"
    location = "VIEW_3D"
    
    name: bpy.props.StringProperty(name ="name", default = "Fern", maxlen = 100)
    position: bpy.props.FloatVectorProperty(name = "Location")
    rotation: bpy.props.IntVectorProperty(name = "Rotation", min = -180, max = 180)
    scale: bpy.props.FloatVectorProperty(name = "Scale", default = (1.0, 1.0, 1.0))

    num_cols: bpy.props.IntProperty(default = 8, name = "Number of sides",  max = 1024, min = 0)
    height: bpy.props.FloatProperty(default = 1.0, name = "Height")
    base_rad: bpy.props.FloatProperty(default = 0.5, name = "Base Radius", max = 10, min = 0)
    vert_vel: bpy.props.FloatProperty(default = 2, name = "Vertical Velocity")
    hor_vel: bpy.props.FloatProperty(default = 1, name = "Horizontal Velocity")
    gravity: bpy.props.FloatProperty(default = .1, name = "Gravity")
    vel_cutoff: bpy.props.FloatProperty(default = -.4, name = "Velocity Cutoff")
    frond_len: bpy.props.FloatProperty(default = 1, name = "Initial Frond Length")
    resolution: bpy.props.FloatProperty(default = 1, name = "Leaf Detail")    
    random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    random_weight: bpy.props.FloatProperty(default = 0.2, min = 0.0, max = 4.0, name = "Weight of Randomizations")
    drift_bool: bpy.props.BoolProperty(default = True, name = "Enable Frond Drift") 
    drift_weight: bpy.props.FloatProperty(default = 0.2, name = "Drift Weight")
    fern_radius: bpy.props.FloatProperty(default = 2, min = 0, max = 10, name = "Max Stalk Spawn Radius")
    num_stalks: bpy.props.IntProperty(default = 3, min = 1, max = 12, name = "Number of Stalks")
    expanded_0: bpy.props.BoolProperty(default = False)
    expanded_1: bpy.props.BoolProperty(default = False)
    expanded_2: bpy.props.BoolProperty(default = False)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        box0 = layout.box()
        row0 = box0.row()
        row0.prop(self, "expanded_0", 
            icon="TRIA_DOWN" if self.expanded_0 else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row0.label(text="Blender Specific Properties")
        if(self.expanded_0):
            box0.prop(self, "name")
            box0.prop(self, "position")
            box0.prop(self, "rotation")
            box0.prop(self, "scale")

        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "expanded_1", 
            icon="TRIA_DOWN" if self.expanded_1 else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row1.label(text="Flora Gen Properties")
        if(self.expanded_1):
            box1.prop(self, "num_cols")
            box1.prop(self, "height")
            box1.prop(self, "base_rad")
            box1.prop(self, "vert_vel")
            box1.prop(self, "hor_vel")
            box1.prop(self, "gravity")
            box1.prop(self, "vel_cutoff")
            box1.prop(self, "frond_len")
            box1.prop(self, "resolution")

        box2 = layout.box()
        row2 = box2.row()
        row2.prop(self, "expanded_2", 
            icon="TRIA_DOWN" if self.expanded_2 else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row2.label(text="Random Properties")
        if(self.expanded_2):
            box2.prop(self, "random")
            box2.prop(self, "seed")
            box2.prop(self, "random_weight")
            box2.prop(self, "drift_bool")
            box2.prop(self, "drift_weight")
            box2.prop(self, "fern_radius")
            box2.prop(self, "num_stalks")
        
    def execute(self, context):
       obj_data = mesh_ops.Object_Metadata(self.name, self.position, self.rotation, self.scale)
       mesh_ops.fern_gen(name = self.name, num_edges=self.num_cols, base_radius=self.base_rad, vert_vel=self.vert_vel, hor_vel=self.hor_vel, resolution=self.resolution, gravity=self.gravity, vel_cutoff=self.vel_cutoff,  frond_len = self.frond_len, random_bool= self.random, seed=self.seed, random_weight = self.random_weight, drift_bool = self.drift_bool, drift_weight=self.drift_weight, fern_radius=self.fern_radius, num_stalks=self.num_stalks)
       mesh_ops.apply_values(obj_data)
       return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_FernOperator.bl_idname)