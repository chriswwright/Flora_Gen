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
from . hello_world_panel import FLORA_GEN_PT_HelloWorldPanel
from . hello_world_op import FLORA_GEN_PT_HelloWorldOperator

classes = [FLORA_GEN_PT_HelloWorldPanel, FLORA_GEN_PT_HelloWorldOperator]
classes_strings = ["FLORA_GEN_PT_HelloWorld", "wm.hello_world_operator"]

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