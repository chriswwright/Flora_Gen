import bpy

class FLORA_GEN_PT_HelloWorldOperator(bpy.types.Operator):
    bl_idname = "wm.hello_world_operator"
    bl_label = "Hello World Operator"
    location = "VIEW_3D"
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        
    def execute(self, context):
       bpy.ops.mesh.primitive_cube_add()
       return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_HelloWorldOperator.bl_idname)