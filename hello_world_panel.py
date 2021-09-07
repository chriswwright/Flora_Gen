import bpy

class FLORA_GEN_PT_HelloWorldPanel(bpy.types.Panel):
    bl_idname = "FLORA_GEN_PT_HelloWorld"
    bl_label = "Hello World"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Flora Generator"
    
    def draw(self, context):
        layout = self.layout

        col = self.layout.column(align=True)
        col.operator("wm.hello_world_operator")
        col.operator("wm.cylinder_operator")
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_HelloWorldPanel.bl_idname)