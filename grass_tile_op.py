from . import mesh_ops
import bpy

class FLORA_GEN_PT_Grass_Tile_Operator(bpy.types.Operator):
    bl_idname = "wm.grass_tile_operator"
    bl_label = "Grass Tile Operator"
    location = "VIEW_3D"
    
    name: bpy.props.StringProperty(name ="name", default = "Grass Tile", maxlen = 100)
    position: bpy.props.FloatVectorProperty(name = "Location")
    rotation: bpy.props.IntVectorProperty(name = "Rotation", min = -180, max = 180)
    scale: bpy.props.FloatVectorProperty(name = "Scale", default = (1.0, 1.0, 1.0))

    grid_len: bpy.props.IntProperty(default = 10, name = "Grid Length")
    grid_width: bpy.props.IntProperty(default = 10, name = "Grid Width")
    density: bpy.props.FloatProperty(default = 1, name = "Grass Density")
    spawn_offset: bpy.props.FloatProperty(default = 5, name = "Spawn Offset")
    selection_pool: bpy.props.IntProperty(default = 5, name = "Selection Pool")
    #hight_scalar: bpy.props.FloatProperty(default = 1, name = "Height Scalar")

    h_scale: bpy.props.FloatProperty(default = 3, name = "H Scalar")
    lacunarity: bpy.props.FloatProperty(default = 1, name = "Lacunarity")
    octaves: bpy.props.FloatProperty(default = 4, name = "Number of Octaves")
    offset: bpy.props.FloatProperty(default = 0.5, name = "Offset")


    random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    random_weight: bpy.props.FloatProperty(default = 1.2, min = 0.0, max = 4.0, name = "Weight of Randomizations")
    drift_bool: bpy.props.BoolProperty(default = True, name = "Enable Frond Drift") 
    drift_weight: bpy.props.FloatProperty(default = 0.8, name = "Drift Weight")
    shift_x: bpy.props.FloatProperty(default = 0, name = "X texture shift")
    shift_y: bpy.props.FloatProperty(default = 0, name = "Y texture shift")

    #grass op properties
    num_cols: bpy.props.IntProperty(default = 6, name = "Number of sides",  max = 64, min = 0)
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
    degree_max: bpy.props.IntProperty(default = 60, name = "Degree Max" , min = 10, max = 360)
    number_stem: bpy.props.IntProperty(default = 5, name = "Number of Stems", min = 1, max = 100)

    expanded_0: bpy.props.BoolProperty(default = False)
    expanded_1: bpy.props.BoolProperty(default = False)
    expanded_2: bpy.props.BoolProperty(default = False)
    expanded_3: bpy.props.BoolProperty(default = False)
    expanded_4: bpy.props.BoolProperty(default = False)

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
            box1.prop(self, "density")
            box1.prop(self, "spawn_offset")
            box1.prop(self, "selection_pool")

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
            box3.prop(self, "drift_bool")
            box3.prop(self, "drift_weight")
            
        box4 = layout.box()
        row4 = box4.row()
        row4.prop(self, "expanded_4", 
            icon="TRIA_DOWN" if self.expanded_4 else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row4.label(text="Grass Operator Properties")
        if(self.expanded_4):
            box4.prop(self, "num_cols")
            box4.prop(self, "base_rad")
            box4.prop(self, "vert_vel")
            box4.prop(self, "hor_vel")
            box4.prop(self, "gravity")
            box4.prop(self, "vel_cutoff")
            box4.prop(self, "grass_radius")
            box4.prop(self, "resolution")
            box4.prop(self, "degree_max")
            box4.prop(self, "number_stem")

    def execute(self, context):
        obj_data = mesh_ops.Object_Metadata(self.name, self.position, self.rotation, self.scale)
        mesh_ops.grass_tile_gen( name=self.name,
                            grid_len= self.grid_len,
                            grid_width= self.grid_width,
                            density= self.density,
                            spawn_offset= self.spawn_offset,
                            selection_pool= self.selection_pool,
                            num_cols= self.num_cols,
                            base_radius= self.base_rad,
                            vert_vel= self.vert_vel,
                            hor_vel= self.hor_vel,
                            gravity= self.gravity,
                            detail= self.resolution,
                            degree_max= self.degree_max,
                            num_curve= self.number_stem,
                            h_scale= self.h_scale,
                            lacunarity= self.lacunarity,
                            octaves= self.octaves,
                            offset= self.offset,
                            x_shift= self.shift_x,
                            y_shift= self.shift_y,
                            random_bool= self.random,
                            seed= self.seed,
                            random_weight= self.random_weight,
                            drift_bool= self.drift_bool,
                            drift_weight= self.drift_weight)
        #mesh_ops.apply_values(obj_data)
        return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_Grass_Tile_Operator.bl_idname)