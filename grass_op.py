from . import mesh_ops
import bpy

class FLORA_GEN_PT_GrassOperator(bpy.types.Operator):
    bl_idname = "wm.grass_operator"
    bl_label = "Grass Operator"
    location = "VIEW_3D"
    
    name: bpy.props.StringProperty(name ="name", default = "Grass", maxlen = 100)
    position: bpy.props.FloatVectorProperty(name = "Location")
    rotation: bpy.props.IntVectorProperty(name = "Rotation", min = -180, max = 180)
    scale: bpy.props.FloatVectorProperty(name = "Scale", default = (1.0, 1.0, 1.0))

    num_cols: bpy.props.IntProperty(default = 8, name = "Number of sides",  max = 1024, min = 0)
    height: bpy.props.FloatProperty(default = 1.0, name = "Height")
    base_rad: bpy.props.FloatProperty(default = 1, name = "Base Radius", max = 10, min = 0)
    vert_vel: bpy.props.FloatProperty(default = 3, name = "Vertical Velocity")
    hor_vel: bpy.props.FloatProperty(default = 1, name = "Horizontal Velocity")
    gravity: bpy.props.FloatProperty(default = .4, name = "Gravity")
    vel_cutoff: bpy.props.FloatProperty(default = -.4, name = "Velocity Cutoff")
    grass_radius: bpy.props.FloatProperty(default = 1.0, name = "Frond Spawn Radius")
    leaf_width: bpy.props.FloatProperty(default = 0.2, name = "Initial Leaf Width")
    leaf_len: bpy.props.FloatProperty(default = 0.5, name = "Initial Leaf Length")
    resolution: bpy.props.FloatProperty(default = 1, name = "Leaf Detail")
    
    random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    random_weight: bpy.props.FloatProperty(default = 1.2, min = 0.0, max = 4.0, name = "Weight of Randomizations")
    drift_bool: bpy.props.BoolProperty(default = True, name = "Enable Frond Drift") 
    drift_weight: bpy.props.FloatProperty(default = 0.8, name = "Drift Weight")
    degree_max: bpy.props.IntProperty(default = 60, name = "Degree Max" , min = 10, max = 360)
    number_stem: bpy.props.IntProperty(default = 5, name = "Number of Stems", min = 1, max = 100)
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
            box1.prop(self, "grass_radius")
            box1.prop(self, "resolution")
            box1.prop(self, "degree_max")
            box1.prop(self, "number_stem")

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
            
    def execute(self, context):
       obj_data = mesh_ops.Object_Metadata(self.name, self.position, self.rotation, self.scale)
       mesh_ops.grass_gen("Grass", self.num_cols, self.base_rad, self.vert_vel, self.hor_vel, self.gravity, self.vel_cutoff, self.grass_radius, self.resolution, self.degree_max, self.number_stem, self.random, self.seed, self.random_weight, self.drift_bool, self.drift_weight)
       mesh_ops.apply_values(obj_data)
       return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_GrassOperator.bl_idname)