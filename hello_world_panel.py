import bpy

class FLORA_GEN_PT_HelloWorldPanel(bpy.types.Panel):
    bl_idname = "FLORA_GEN_PT_HelloWorld"
    bl_label = "Hello World"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Flora Generator"
    bpy.types.Scene.expanded_0 = True
    

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        box0 = col.box()
        row0 = box0.row()
        box0.operator("wm.hello_world_operator")
        box0.operator("wm.cylinder_operator")
        box0.operator("wm.curve_operator")
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_HelloWorldPanel.bl_idname)


class FLORA_GEN_PT_FernPanel(bpy.types.Panel):
    bl_idname = "FLORA_GEN_PT_Fern"
    bl_label = "Fern Operators"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Flora Generator"
    bpy.types.Scene.expanded_0 = True
    

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        box2 = col.box()
        box2.operator("wm.stem_operator")
        box2.operator("wm.frond_operator")
        box2.operator("wm.fern_operator")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_FernPanel.bl_idname)


class FLORA_GEN_PT_GrassPanel(bpy.types.Panel):
    bl_idname = "FLORA_GEN_PT_Grass"
    bl_label = "Grass Operators"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Flora Generator"
    bpy.types.Scene.expanded_0 = True
    

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        box3 = col.box()
        box3.operator("wm.grass_operator")
        box3.operator("wm.stick_operator")
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_GrassPanel.bl_idname)

class FLORA_GEN_PT_NoisePanel(bpy.types.Panel):
    bl_idname = "FLORA_GEN_PT_Noise"
    bl_label = "Noise Operators"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Flora Generator"
    bpy.types.Scene.expanded_0 = True
    

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        box3 = col.box()
        box3.operator("wm.noise_operator")
        box3.operator("wm.rock_operator")
        box3.operator("wm.grass_tile_operator")
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_NoisePanel.bl_idname)
    