from . import mesh_ops
import bpy
#mutate chance
#max len
#base width
#change weight

class FLORA_GEN_PT_StickOperator(bpy.types.Operator):
    bl_idname = "wm.stick_operator"
    bl_label = "Stick Operator"
    location = "VIEW_3D"
    
    name: bpy.props.StringProperty(name ="name", default = "Stick", maxlen = 100)
    position: bpy.props.FloatVectorProperty(name = "Location")
    rotation: bpy.props.IntVectorProperty(name = "Rotation", min = -180, max = 180)
    scale: bpy.props.FloatVectorProperty(name = "Scale", default = (1.0, 1.0, 1.0))

    num_cols: bpy.props.IntProperty(default = 8, name = "Number of sides",  max = 1024, min = 0)
    height: bpy.props.FloatProperty(default = .8, name = "Height")
    base_rad: bpy.props.FloatProperty(default = 0.20, name = "Base Radius", max = 10, min = 0)
    end_rad: bpy.props.FloatProperty(default = 0.02, name = "Tip Radius", max = 10, min = 0)
    resolution: bpy.props.FloatProperty(default = 1.0, name = "Stick Resolution")

    #stick specific
    mutate_chance: bpy.props.FloatProperty(default = .4, min = 0, max = 1.0, name = "Split Chance")
    max_perm: bpy.props.IntProperty(default = 20, min = 1, name = "Max Permutations")
    degree_offset: bpy.props.IntProperty(default = 40, min = 0, max = 360, name = "Degree Offset")


    random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    random_weight: bpy.props.FloatProperty(default = 1.2, min = 0.0, max = 4.0, name = "Weight of Randomizations")

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
            box1.prop(self, "end_rad")
            box1.prop(self, "resolution")
            box1.prop(self, "mutate_chance")
            box1.prop(self, "max_perm")
            box1.prop(self, "degree_offset")

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

            
    def execute(self, context):
        obj_data = mesh_ops.Object_Metadata(self.name, self.position, self.rotation, self.scale)
        mesh_ops.stick_gen( name=self.name, 
                            num_edges=self.num_cols, 
                            height=self.height, 
                            base_width=self.base_rad,
                            end_width=self.end_rad,
                            resolution=self.resolution, 
                            mutate_chance=self.mutate_chance, 
                            max_perm=self.max_perm, 
                            degree_offset=self.degree_offset, 
                            random_bool=self.random, 
                            seed=self.seed, 
                            random_weight=self.random_weight)
        #mesh_ops.apply_values(obj_data)
        return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_StickOperator.bl_idname)