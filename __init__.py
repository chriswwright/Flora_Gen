# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Flora_Gen",
    "author" : "Christopher Wright",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View_3D",
    "warning" : "",
    "category" : "Generic"
}

#blender imports
import bpy

#addon imports
#panels
from . hello_world_panel import FLORA_GEN_PT_FernPanel, FLORA_GEN_PT_GrassPanel, FLORA_GEN_PT_HelloWorldPanel, FLORA_GEN_PT_NoisePanel

#debug operators
from . hello_world_op import FLORA_GEN_PT_HelloWorldOperator
from . cylinder_op import FLORA_GEN_PT_CylinderOperator
from . curve_op import FLORA_GEN_PT_CurveOperator

#flora
from . stem_op import FLORA_GEN_PT_StemOperator
from . frond_op import FLORA_GEN_PT_FrondOperator
from . fern_op import FLORA_GEN_PT_FernOperator
from . grass_op import FLORA_GEN_PT_GrassOperator
from . stick_op import FLORA_GEN_PT_StickOperator


#noise
from . noise_op import FLORA_GEN_PT_NoiseOperator
from . rock_op import FLORA_GEN_PT_RockOperator

#tile set
from . grass_tile_op import FLORA_GEN_PT_Grass_Tile_Operator
from . multi_tile_op import FLORA_GEN_PT_Multi_Tile_Operator

classes = [ FLORA_GEN_PT_HelloWorldPanel, 
            FLORA_GEN_PT_FernPanel, 
            FLORA_GEN_PT_GrassPanel, 
            FLORA_GEN_PT_NoisePanel, 
            FLORA_GEN_PT_HelloWorldOperator, 
            FLORA_GEN_PT_CylinderOperator, 
            FLORA_GEN_PT_StemOperator, 
            FLORA_GEN_PT_FrondOperator, 
            FLORA_GEN_PT_FernOperator, 
            FLORA_GEN_PT_GrassOperator, 
            FLORA_GEN_PT_CurveOperator, 
            FLORA_GEN_PT_NoiseOperator, 
            FLORA_GEN_PT_RockOperator,
            FLORA_GEN_PT_Grass_Tile_Operator,
            FLORA_GEN_PT_StickOperator,
            FLORA_GEN_PT_Multi_Tile_Operator]
classes_strings = [ "FLORA_GEN_PT_HelloWorld", 
                    "FLORA_GEN_PT_Fern", 
                    "FLORA_GEN_PT_Grass", 
                    "FLORA_GEN_PT_Noise", 
                    "wm.hello_world_operator", 
                    "wm.cylinder_operator", 
                    "wm.stem_operator", 
                    "wm.frond_operator", 
                    "wm.fern_operator", 
                    "wm.grass_operator", 
                    "wm.curve_operator", 
                    "wm.noise_operator", 
                    "wm.rock_operator",
                    "wm.grass_tile_operator",
                    "wm.stick_operator",
                    "wm.multi_tile_operator"]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.VIEW3D_MT_object.append(cls.menu_func)

def unregister():
    for cls in classes_strings:
            TargetClass = bpy.types.Panel.bl_rna_get_subclass_py(cls)
            if(TargetClass != None):
                bpy.utils.unregister_class(TargetClass)

if __name__ == "__main__":
    register()