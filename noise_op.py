from . import mesh_ops
import bpy

class FLORA_GEN_PT_NoiseOperator(bpy.types.Operator):
    bl_idname = "wm.noise_operator"
    bl_label = "Noise Operator"
    location = "VIEW_3D"
    
    name: bpy.props.StringProperty(name ="name", default = "Noise", maxlen = 100)
    position: bpy.props.FloatVectorProperty(name = "Location")
    rotation: bpy.props.IntVectorProperty(name = "Rotation", min = -180, max = 180)
    scale: bpy.props.FloatVectorProperty(name = "Scale", default = (1.0, 1.0, 1.0))

    grid_len: bpy.props.IntProperty(default = 10, name = "Grid Length")
    grid_width: bpy.props.IntProperty(default = 10, name = "Grid Width")
    resolution: bpy.props.FloatProperty(default = 1, name = "Grid Complexity")
    hight_scalar: bpy.props.FloatProperty(default = 1, name = "Height Scalar")

    h_scale: bpy.props.FloatProperty(default = 3, name = "H Scalar")
    lacunarity: bpy.props.FloatProperty(default = 1, name = "Lacunarity")
    octaves: bpy.props.FloatProperty(default = 4, name = "Number of Octaves")
    offset: bpy.props.FloatProperty(default = 0.5, name = "Offset")


    random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    random_weight: bpy.props.FloatProperty(default = 1.2, min = 0.0, max = 4.0, name = "Weight of Randomizations")
    shift_x: bpy.props.FloatProperty(default = 0, name = "X texture shift")
    shift_y: bpy.props.FloatProperty(default = 0, name = "Y texture shift")

    expanded_0: bpy.props.BoolProperty(default = False)
    expanded_1: bpy.props.BoolProperty(default = False)
    expanded_2: bpy.props.BoolProperty(default = False)
    expanded_3: bpy.props.BoolProperty(default = False)

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
            box1.prop(self, "grid_len")
            box1.prop(self, "grid_width")
            box1.prop(self, "resolution")
            box1.prop(self, "hight_scalar")


        box2 = layout.box()
        row2 = box2.row()
        row2.prop(self, "expanded_2",
            icon="TRIA_DOWN" if self.expanded_2 else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row2.label(text="Noise Properties")
        if(self.expanded_2):
            box2.prop(self, "h_scale")
            box2.prop(self, "lacunarity")
            box2.prop(self, "octaves")
            box2.prop(self, "offset")
            box2.prop(self, "shift_x")
            box2.prop(self, "shift_y")

        box3 = layout.box()
        row3 = box3.row()
        row3.prop(self, "expanded_3", 
            icon="TRIA_DOWN" if self.expanded_3 else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row3.label(text="Random Properties")
        if(self.expanded_3):
            box3.prop(self, "random")
            box3.prop(self, "seed")
            box3.prop(self, "random_weight")
            
    def execute(self, context):
        obj_data = mesh_ops.Object_Metadata(self.name, self.position, self.rotation, self.scale)
        mesh_ops.noise_gen( name=self.name,
                            grid_len= self.grid_len,
                            grid_width= self.grid_width,
                            resolution= self.resolution,
                            height_scalar= self.hight_scalar,
                            h_scale= self.h_scale,
                            lacunarity= self.lacunarity,
                            octaves= self.octaves,
                            offset= self.offset,
                            x_shift= self.shift_x,
                            y_shift= self.shift_y,
                            random_bool= self.random,
                            seed= self.seed,
                            random_weight= self.random_weight)
        mesh_ops.apply_values(obj_data)
        return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_NoiseOperator.bl_idname)