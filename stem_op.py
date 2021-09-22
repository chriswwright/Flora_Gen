from . import mesh_ops
import bpy

class FLORA_GEN_PT_StemOperator(bpy.types.Operator):
    bl_idname = "wm.stem_operator"
    bl_label = "Stem Operator"
    location = "VIEW_3D"
    
    name: bpy.props.StringProperty(name ="name", default = "Stem", maxlen = 100)
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
    random: bpy.props.BoolProperty(default = False, name = "Randomize Values")
    seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    #top_rotation: bpy.props.IntProperty(default = 0, name = "Top Rotation", max = 90, min = -90)
    #bottom_rotation: bpy.props.IntProperty(default = 0, name = "Bottom Rotation", max = 90, min = -90)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        box0 = layout.box()
        box0.label(text="Blender Specific Properties")
        box0.prop(self, "name")
        box0.prop(self, "position")
        box0.prop(self, "rotation")
        box0.prop(self, "scale")
        
        box1 = layout.box()
        box1.label(text="Flora Gen Properties")
        box1.prop(self, "num_cols")
        box1.prop(self, "height")
        box1.prop(self, "base_rad")
        box1.prop(self, "vert_vel")
        box1.prop(self, "hor_vel")
        box1.prop(self, "gravity")
        box1.prop(self, "vel_cutoff")
        
    def execute(self, context):
       obj_data = mesh_ops.Object_Metadata(self.name, self.position, self.rotation, self.scale)
       mesh_ops.stem_gen(name = self.name, num_edges=self.num_cols, base_radius=self.base_rad, vert_vel=self.vert_vel, hor_vel=self.hor_vel, gravity=self.gravity, vel_cutoff=self.vel_cutoff, random_bool= self.random, seed=self.seed)
       return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_StemOperator.bl_idname)