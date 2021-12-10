from random import seed
from . import mesh_ops
import bpy


  # make rock less
  # make grass more
  # make stick bigger      

class FLORA_GEN_PT_Multi_Tile_Operator(bpy.types.Operator):
    def box_show_func(self, layout, in_bool, bool_title, show_list, title, list_prefix = ""):
        box = layout.box()
        row = box.row()
        row.prop(self, bool_title, 
            icon="TRIA_DOWN" if in_bool else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row.label(text=title)
        if(in_bool):
            for prop in show_list:
                box.prop(self, list_prefix + prop)

    bl_idname = "wm.multi_tile_operator"
    bl_label = "Multi Tile Operator"
    location = "VIEW_3D"
    
    name: bpy.props.StringProperty(name ="name", default = "Grass Tile", maxlen = 100)
    position: bpy.props.FloatVectorProperty(name = "Location")
    rotation: bpy.props.IntVectorProperty(name = "Rotation", min = -180, max = 180)
    scale: bpy.props.FloatVectorProperty(name = "Scale", default = (1.0, 1.0, 1.0))

    expanded_0: bpy.props.BoolProperty(default = False)
    expanded_1: bpy.props.BoolProperty(default = False)
    expanded_2: bpy.props.BoolProperty(default = False)

    f_parent: bpy.props.BoolProperty(default = False)
    expanded_f_0: bpy.props.BoolProperty(default = False)
    expanded_f_1: bpy.props.BoolProperty(default = False)
    expanded_f_2: bpy.props.BoolProperty(default = False)
    expanded_f_3: bpy.props.BoolProperty(default = False)


    g_parent: bpy.props.BoolProperty(default = False)
    expanded_g_0: bpy.props.BoolProperty(default = False)
    expanded_g_1: bpy.props.BoolProperty(default = False)
    expanded_g_2: bpy.props.BoolProperty(default = False)
    expanded_g_3: bpy.props.BoolProperty(default = False)

    r_parent: bpy.props.BoolProperty(default = False)
    expanded_r_0: bpy.props.BoolProperty(default = False)
    expanded_r_1: bpy.props.BoolProperty(default = False)
    expanded_r_2: bpy.props.BoolProperty(default = False)
    expanded_r_3: bpy.props.BoolProperty(default = False)

    s_parent: bpy.props.BoolProperty(default = False)
    expanded_s_0: bpy.props.BoolProperty(default = False)
    expanded_s_1: bpy.props.BoolProperty(default = False)
    expanded_s_2: bpy.props.BoolProperty(default = False)
    expanded_s_3: bpy.props.BoolProperty(default = False)    

    fern_show: bpy.props.BoolProperty(default = False, name = "Generate Fern Tile")
    grass_show: bpy.props.BoolProperty(default = False, name = "Generate Grass Tile")
    rock_show: bpy.props.BoolProperty(default = False, name = "Generate Rock Tile")
    stick_show: bpy.props.BoolProperty(default = False, name = "Generate Stick Tile")

    #fern
    #fern spawn properties
    f_grid_len: bpy.props.IntProperty(default = 1000, name = "Grid Length")
    f_grid_width: bpy.props.IntProperty(default = 1000, name = "Grid Width")
    f_density: bpy.props.FloatProperty(default = .8, name = "Spawn Density")
    f_spawn_offset: bpy.props.FloatProperty(default = 40, name = "Spawn Offset")
    f_selection_pool: bpy.props.IntProperty(default = 3, name = "Selection Pool")

    #fern noise properties
    f_h_scale: bpy.props.FloatProperty(default = 3, name = "H Scalar")
    f_lacunarity: bpy.props.FloatProperty(default = 1, name = "Lacunarity")
    f_octaves: bpy.props.FloatProperty(default = 4, name = "Number of Octaves")
    f_offset: bpy.props.FloatProperty(default = 0.5, name = "Offset")
    f_shift_x: bpy.props.FloatProperty(default = 0, name = "X texture shift")
    f_shift_y: bpy.props.FloatProperty(default = 0, name = "Y texture shift")
    f_random_shift: bpy.props.BoolProperty(default = True, name = "Randomize Shift X and Y")


    #fern op properties
    f_num_cols: bpy.props.IntProperty(default = 8, name = "Number of sides",  max = 1024, min = 0)
    f_base_rad: bpy.props.FloatProperty(default = 0.5, name = "Base Radius", max = 10, min = 0)
    f_vert_vel: bpy.props.FloatProperty(default = 2, name = "Vertical Velocity")
    f_hor_vel: bpy.props.FloatProperty(default = 1, name = "Horizontal Velocity")
    f_gravity: bpy.props.FloatProperty(default = .1, name = "Gravity")
    f_vel_cutoff: bpy.props.FloatProperty(default = -.4, name = "Velocity Cutoff")
    f_frond_len: bpy.props.FloatProperty(default = 1, name = "Initial Frond Length")
    f_resolution: bpy.props.FloatProperty(default = 1, name = "Leaf Detail")    
    f_fern_radius: bpy.props.FloatProperty(default = 2, min = 0, max = 10, name = "Max Stalk Spawn Radius")
    f_num_stalks: bpy.props.IntProperty(default = 3, min = 1, max = 12, name = "Number of Stalks")

    #fern random properties
    f_random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    f_seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    f_random_weight: bpy.props.FloatProperty(default = 0.4, min = 0.0, max = 4.0, name = "Weight of Randomizations")
    f_drift_bool: bpy.props.BoolProperty(default = True, name = "Enable Frond Drift") 
    f_drift_weight: bpy.props.FloatProperty(default = 0.4, name = "Drift Weight")

    #fern property lists
    list_f_1 = ["num_cols", "base_rad", "vert_vel", "hor_vel", "gravity", "vel_cutoff", "frond_len", "resolution", "fern_radius", "num_stalks"]

    #grass
    #grass spawn properties
    g_grid_len: bpy.props.IntProperty(default = 1000, name = "Grid Length")
    g_grid_width: bpy.props.IntProperty(default = 1000, name = "Grid Width")
    g_density: bpy.props.FloatProperty(default = 1, name = "Spawn Density")
    g_spawn_offset: bpy.props.FloatProperty(default = 25, name = "Spawn Offset")
    g_selection_pool: bpy.props.IntProperty(default = 5, name = "Selection Pool")

    #grass noise properties
    g_h_scale: bpy.props.FloatProperty(default = 3, name = "H Scalar")
    g_lacunarity: bpy.props.FloatProperty(default = 1, name = "Lacunarity")
    g_octaves: bpy.props.FloatProperty(default = 4, name = "Number of Octaves")
    g_offset: bpy.props.FloatProperty(default = 0.5, name = "Offset")
    g_shift_x: bpy.props.FloatProperty(default = 0, name = "X texture shift")
    g_shift_y: bpy.props.FloatProperty(default = 0, name = "Y texture shift")
    g_random_shift: bpy.props.BoolProperty(default = True, name = "Randomize Shift X and Y")


    #grass op properties
    g_num_cols: bpy.props.IntProperty(default = 6, name = "Number of sides",  max = 64, min = 0)
    g_height: bpy.props.FloatProperty(default = 1.0, name = "Height")
    g_base_rad: bpy.props.FloatProperty(default = 1, name = "Base Radius", max = 10, min = 0)
    g_vert_vel: bpy.props.FloatProperty(default = 3, name = "Vertical Velocity")
    g_hor_vel: bpy.props.FloatProperty(default = 1, name = "Horizontal Velocity")
    g_gravity: bpy.props.FloatProperty(default = .4, name = "Gravity")
    g_vel_cutoff: bpy.props.FloatProperty(default = -.4, name = "Velocity Cutoff")
    g_grass_radius: bpy.props.FloatProperty(default = 1.0, name = "Frond Spawn Radius")
    g_leaf_width: bpy.props.FloatProperty(default = 0.2, name = "Initial Leaf Width")
    g_leaf_len: bpy.props.FloatProperty(default = 0.5, name = "Initial Leaf Length")
    g_resolution: bpy.props.FloatProperty(default = 1, name = "Leaf Detail")
    g_degree_max: bpy.props.IntProperty(default = 60, name = "Degree Max" , min = 10, max = 360)
    g_number_stem: bpy.props.IntProperty(default = 5, name = "Number of Stems", min = 1, max = 100)

    #grass random properties
    g_random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    g_seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    g_random_weight: bpy.props.FloatProperty(default = 1.2, min = 0.0, max = 4.0, name = "Weight of Randomizations")
    g_drift_bool: bpy.props.BoolProperty(default = True, name = "Enable Frond Drift") 
    g_drift_weight: bpy.props.FloatProperty(default = 0.8, name = "Drift Weight")

    #grass property lists
    list_g_1 = ["num_cols", "base_rad", "vert_vel", "hor_vel", "gravity", "vel_cutoff", "grass_radius", "resolution", "degree_max", "number_stem"]

    #rock
    #rock spawn properties
    r_grid_len: bpy.props.IntProperty(default = 1000, name = "Grid Length")
    r_grid_width: bpy.props.IntProperty(default = 1000, name = "Grid Width")
    r_density: bpy.props.FloatProperty(default = 1.2, name = "Spawn Density")
    r_spawn_offset: bpy.props.FloatProperty(default = 40, name = "Spawn Offset")
    r_selection_pool: bpy.props.IntProperty(default = 10, name = "Selection Pool")

    #rock noise properties
    r_h_scale: bpy.props.FloatProperty(default = 3, name = "H Scalar")
    r_lacunarity: bpy.props.FloatProperty(default = 1, name = "Lacunarity")
    r_octaves: bpy.props.FloatProperty(default = 4, name = "Number of Octaves")
    r_offset: bpy.props.FloatProperty(default = 0.6, name = "Offset")
    r_shift_x: bpy.props.FloatProperty(default = 0, name = "X texture shift")
    r_shift_y: bpy.props.FloatProperty(default = 0, name = "Y texture shift")
    r_random_shift: bpy.props.BoolProperty(default = True, name = "Randomize Shift X and Y")

    #rock op properties
    r_rock_radius: bpy.props.IntProperty(default = 10, name = "Rock Radius")
    r_resolution: bpy.props.IntProperty(default = 3, name = "Resolution")
    r_hight_scalar: bpy.props.FloatProperty(default = .2, name = "Height Scalar")
    r_num_rings: bpy.props.IntProperty(default = 3, name = "Number of Rings")

    #rock random properties
    r_random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    r_seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    r_random_weight: bpy.props.FloatProperty(default = 1, min = 0.0, max = 4.0, name = "Weight of Randomizations")

    #rock property lists
    list_r_1 = ["rock_radius", "resolution", "hight_scalar", "num_rings"]

    #stick
    #stick spawn properties
    s_grid_len: bpy.props.IntProperty(default = 1000, name = "Grid Length")
    s_grid_width: bpy.props.IntProperty(default = 1000, name = "Grid Width")
    s_density: bpy.props.FloatProperty(default = 1, name = "Spawn Density")
    s_spawn_offset: bpy.props.FloatProperty(default = 20, name = "Spawn Offset")
    s_selection_pool: bpy.props.IntProperty(default = 20, name = "Selection Pool")

    #stick noise properties
    s_h_scale: bpy.props.FloatProperty(default = 3, name = "H Scalar")
    s_lacunarity: bpy.props.FloatProperty(default = 1, name = "Lacunarity")
    s_octaves: bpy.props.FloatProperty(default = 4, name = "Number of Octaves")
    s_offset: bpy.props.FloatProperty(default = 0.5, name = "Offset")
    s_shift_x: bpy.props.FloatProperty(default = 0, name = "X texture shift")
    s_shift_y: bpy.props.FloatProperty(default = 0, name = "Y texture shift")
    s_random_shift: bpy.props.BoolProperty(default = True, name = "Randomize Shift X and Y")

    #stick op properties
    s_num_cols: bpy.props.IntProperty(default = 8, name = "Number of sides",  max = 1024, min = 0)
    s_height: bpy.props.FloatProperty(default = 1, name = "Height")
    s_base_rad: bpy.props.FloatProperty(default = 0.40, name = "Base Radius", max = 10, min = 0)
    s_end_rad: bpy.props.FloatProperty(default = 0.04, name = "Tip Radius", max = 10, min = 0)
    s_resolution: bpy.props.FloatProperty(default = 1.0, name = "Stick Resolution")
    s_mutate_chance: bpy.props.FloatProperty(default = .4, min = 0, max = 1.0, name = "Split Chance")
    s_max_perm: bpy.props.IntProperty(default = 20, min = 1, name = "Max Permutations")
    s_degree_offset: bpy.props.IntProperty(default = 40, min = 0, max = 360, name = "Degree Offset")

    #stick random properties
    s_random: bpy.props.BoolProperty(default = True, name = "Randomize Values")
    s_seed: bpy.props.IntProperty(default = 0, name = "Seed: 0 sets to randomize")
    s_random_weight: bpy.props.FloatProperty(default = 1.2, min = 0.0, max = 4.0, name = "Weight of Randomizations")

    #stick property lists
    list_s_1 = ["num_cols", "height", "base_rad", "end_rad", "resolution", "mutate_chance", "max_perm", "degree_offset"]

    list_total_0 = ["name", "position", "rotation", "scale"]
    list_total_1 = ["grid_len", "grid_width", "density", "spawn_offset", "selection_pool"]
    list_total_2 = ["h_scale", "lacunarity", "octaves", "offset", "shift_x", "shift_y", "random_shift"]
    list_total_3 = ["random", "seed", "random_weight", "drift_bool", "drift_weight"]
    list_total_4 = ["fern_show", "grass_show", "rock_show", "stick_show"]



    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        #self.box_show_func(layout, self.expanded_0, "expanded_0", self.list_total_0, "Blender Specific Properties")
        self.box_show_func(layout, self.expanded_2, "expanded_2", self.list_total_4, "Tile Select Properties")

        if(self.fern_show):
            box_fern = layout.box()
            row_fern = box_fern.row()
            row_fern.prop(self, "f_parent", 
                icon="TRIA_DOWN" if self.f_parent else "TRIA_RIGHT",
                icon_only=True, emboss=False
            )
            row_fern.label(text="Fern Operators")
            if(self.f_parent):
                self.box_show_func(box_fern, self.expanded_f_0, "expanded_f_0", self.list_total_1, "Fern Spawning Properties", "f_")
                self.box_show_func(box_fern, self.expanded_f_1, "expanded_f_1", self.list_f_1, "Fern Operator Properties", "f_")
                self.box_show_func(box_fern, self.expanded_f_2, "expanded_f_2", self.list_total_2, "Fern Noise Properties", "f_")
                self.box_show_func(box_fern, self.expanded_f_3, "expanded_f_3", self.list_total_3, "Fern Random Properties", "f_")


        if(self.grass_show):
            box_grass = layout.box()
            row_grass = box_grass.row()
            row_grass.prop(self, "g_parent", 
                icon="TRIA_DOWN" if self.g_parent else "TRIA_RIGHT",
                icon_only=True, emboss=False
            )
            row_grass.label(text="Grass Operators")
            if(self.g_parent):
                self.box_show_func(box_grass, self.expanded_g_0, "expanded_g_0", self.list_total_1, "Grass Spawning Properties", "g_")
                self.box_show_func(box_grass, self.expanded_g_1, "expanded_g_1", self.list_g_1, "Grass Operator Properties", "g_")
                self.box_show_func(box_grass, self.expanded_g_2, "expanded_g_2", self.list_total_2, "Grass Noise Properties", "g_")
                self.box_show_func(box_grass, self.expanded_g_3, "expanded_g_3", self.list_total_3, "Grass Random Properties", "g_")

        if(self.rock_show):
            box_rock = layout.box()
            row_rock = box_rock.row()
            row_rock.prop(self, "r_parent", 
                icon="TRIA_DOWN" if self.r_parent else "TRIA_RIGHT",
                icon_only=True, emboss=False
            )
            row_rock.label(text="Rock Operators")
            if(self.r_parent):
                self.box_show_func(box_rock, self.expanded_r_0, "expanded_r_0", self.list_total_1, "Rock Spawning Properties", "r_")
                self.box_show_func(box_rock, self.expanded_r_1, "expanded_r_1", self.list_r_1, "Rock Operator Properties", "r_")
                self.box_show_func(box_rock, self.expanded_r_2, "expanded_r_2", self.list_total_2, "Rock Noise Properties", "r_")
                self.box_show_func(box_rock, self.expanded_r_3, "expanded_r_3", self.list_total_3[:-2], "Rock Random Properties", "r_")

        if(self.stick_show):
            box_stick = layout.box()
            row_stick = box_stick.row()
            row_stick.prop(self, "s_parent", 
                icon="TRIA_DOWN" if self.s_parent else "TRIA_RIGHT",
                icon_only=True, emboss=False
            )
            row_stick.label(text="Stick Operators")
            if(self.s_parent):
                self.box_show_func(box_stick, self.expanded_s_0, "expanded_s_0", self.list_total_1, "Stick Spawning Properties", "s_")
                self.box_show_func(box_stick, self.expanded_s_1, "expanded_s_1", self.list_s_1, "Stick Operator Properties", "s_")
                self.box_show_func(box_stick, self.expanded_s_2, "expanded_s_2", self.list_total_2, "Stick Noise Properties", "s_")
                self.box_show_func(box_stick, self.expanded_s_3, "expanded_s_3", self.list_total_3[:-2], "Stick Random Properties", "s_")
            


    def execute(self, context):
        obj_data = mesh_ops.Object_Metadata(self.name, self.position, self.rotation, self.scale)
        if(self.fern_show):
            mesh_ops.multi_tile_gen(name = "Fern Tile", 
                                    grid_len=self.f_grid_len, 
                                    grid_width=self.f_grid_width,
                                    density=self.f_density,
                                    spawn_offset=self.f_spawn_offset,
                                    selection_pool=self.f_selection_pool,
                                    function_select=1,
                                    al=["Fern", self.f_num_cols, self.f_base_rad, self.f_vert_vel, self.f_hor_vel, self.f_gravity, self.f_vel_cutoff, self.f_frond_len, self.f_resolution, self.f_random, self.f_seed, self.f_random_weight, self.f_drift_bool, self.f_drift_weight, self.f_fern_radius, self.f_num_stalks],
                                    h_scale=self.f_h_scale,
                                    lacunarity=self.f_lacunarity,
                                    octaves=self.f_octaves,
                                    offset=self.f_offset,
                                    x_shift=self.f_shift_x,
                                    y_shift=self.f_shift_y,
                                    shift_bool=self.f_random_shift,
                                    random_bool=self.f_random,
                                    seed=self.f_seed,
                                    random_weight=self.f_random_weight,
                                    drift_bool=self.f_drift_bool,
                                    drift_weight=self.f_drift_weight)
        if(self.grass_show):
            mesh_ops.multi_tile_gen(name = "Grass Tile",
                                    grid_len=self.g_grid_len, 
                                    grid_width=self.g_grid_width,
                                    density=self.g_density,
                                    spawn_offset=self.g_spawn_offset,
                                    selection_pool=self.g_selection_pool,
                                    function_select=2,
                                    al=["Grass", self.g_num_cols, self.g_base_rad, self.g_vert_vel, self.g_hor_vel, self.g_gravity, self.g_vel_cutoff, self.g_grass_radius, self.g_resolution, self.g_degree_max, self.g_number_stem, self.g_random, self.g_seed, self.g_random_weight, self.g_drift_bool, self.g_drift_weight],
                                    h_scale=self.g_h_scale,
                                    lacunarity=self.g_lacunarity,
                                    octaves=self.g_octaves,
                                    offset=self.g_offset,
                                    x_shift=self.g_shift_x,
                                    y_shift=self.g_shift_y,
                                    shift_bool=self.g_random_shift,
                                    random_bool=self.g_random,
                                    seed=self.g_seed,
                                    random_weight=self.g_random_weight,
                                    drift_bool=self.g_drift_bool,
                                    drift_weight=self.g_drift_weight)
        if(self.rock_show):
            mesh_ops.multi_tile_gen(name = "Rock Tile",
                                    grid_len=self.r_grid_len, 
                                    grid_width=self.r_grid_width,
                                    density=self.r_density,
                                    spawn_offset=self.r_spawn_offset,
                                    selection_pool=self.r_selection_pool,
                                    function_select=3,
                                    al=["Rock", self.r_rock_radius, self.r_resolution, self.r_hight_scalar, self.r_num_rings, self.r_h_scale, self.r_lacunarity, self.r_octaves, self.r_offset, self.r_shift_x, self.r_shift_y, self.r_random, self.r_seed, self.r_random_weight],
                                    h_scale=self.r_h_scale,
                                    lacunarity=self.r_lacunarity,
                                    octaves=self.r_octaves,
                                    offset=self.r_offset,
                                    x_shift=self.r_shift_x,
                                    y_shift=self.r_shift_y,
                                    shift_bool=self.r_random_shift,
                                    random_bool=self.r_random,
                                    seed=self.r_seed,
                                    random_weight=self.r_random_weight,
                                    drift_bool=False,
                                    drift_weight=0)
        if(self.stick_show):
            mesh_ops.multi_tile_gen(name = "Stick Tile",
                                    grid_len=self.s_grid_len, 
                                    grid_width=self.s_grid_width,
                                    density=self.s_density,
                                    spawn_offset=self.s_spawn_offset,
                                    selection_pool=self.s_selection_pool,
                                    function_select=4,
                                    al=["Stick", self.s_num_cols, self.s_height, self.s_base_rad, self.s_end_rad, self.s_resolution, self.s_mutate_chance, self.s_max_perm, self.s_degree_offset, self.s_random, self.s_seed, self.s_random_weight], 
                                    h_scale=self.s_h_scale,
                                    lacunarity=self.s_lacunarity,
                                    octaves=self.s_octaves,
                                    offset=self.s_offset,
                                    x_shift=self.s_shift_x,
                                    y_shift=self.s_shift_y,
                                    shift_bool=self.s_random_shift,
                                    random_bool=self.s_random,
                                    seed=self.s_seed,
                                    random_weight=self.s_random_weight,
                                    drift_bool=False,
                                    drift_weight=0)
        return {'FINISHED'}
    
    def menu_func(self, context):
        self.layout.operator(FLORA_GEN_PT_Multi_Tile_Operator.bl_idname)
