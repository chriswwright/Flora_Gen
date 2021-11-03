from . import mesh_ops
import bpy

class FLORA_GEN_PT_CurveOperator(bpy.types.Operator):
    bl_idname = "wm.curve_operator"
    bl_label = "Curve Operator"
    location = "VIEW_3D"
    
    name: bpy.props.StringProperty(name ="name", default = "Cylinder", maxlen = 100)
    position: bpy.props.FloatVectorProperty(name = "Location")
    rotation: bpy.props.IntVectorProperty(name = "Rotation", min = -180, max = 180)
    scale: bpy.props.FloatVectorProperty(name = "Scale", default = (1.0, 1.0, 1.0))

    num_cols: bpy.props.IntProperty(default = 8, name = "Number of sides",  max = 1024, min = 0)
    top_loc_pos: bpy.props.FloatVectorProperty(default = (0.0, 0.0, 1.0), name = "Top Local Offset")
    top: bpy.props.FloatProperty(default = 1, name = "Top Radius", max = 10, min = 0)
    bottom: bpy.props.FloatProperty(default = 1, name = "Bottom Radius", max = 10, min = 0)
    top_rotation: bpy.props.IntProperty(default = 0, name = "Top Rotation", max = 90, min = -90)
    bottom_rotation: bpy.props.IntProperty(default = 0, name = "Bottom Rotation", max = 90, min = -90)
    present_radius: bpy.props.IntProperty(default = 20, name = "Present Radius", max = 360, min = 10)
    expanded_0: bpy.props.BoolProperty(default = False)
    expanded_1: bpy.props.BoolProperty(default = False)

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
            box1.prop(self, "top_loc_pos")
            box1.prop(self, "top")
            box1.prop(self, "bottom")
            box1.prop(self, "top_rotation")
            box1.prop(self, "bottom_rotation")
            box1.prop(self, "present_radius")
        
        
    def execute(self, context):
       obj_data = mesh_ops.Object_Metadata(self.name, self.position, self.rotation, self.scale)
       mesh_ops.curve_gen(num_edges=self.num_cols, top_local_pos=self.top_loc_pos, top_radius=self.top, bottom_radius=self.bottom, top_rotation=self.top_rotation, bottom_rotation=self.bottom_rotation, degree_max = self.present_radius, object_metadata=obj_data)
       return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_CurveOperator.bl_idname)