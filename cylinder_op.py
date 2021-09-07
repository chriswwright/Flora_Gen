from . import mesh_ops
import bpy

class FLORA_GEN_PT_CylinderOperator(bpy.types.Operator):
    bl_idname = "wm.cylinder_operator"
    bl_label = "Cylinder Operator"
    location = "VIEW_3D"
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        
    def execute(self, context):
       mesh_ops.cylinder_gen()
       return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_CylinderOperator.bl_idname)