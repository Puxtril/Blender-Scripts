import bpy

bl_info = {
    "name": "Empty Vgroup Remover",
    "description": "Adds a button to remove empty vertex groups",
    "author": "Puxtril",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Object Data Properties > Vertex Groups > Vertex Group Specials > Remove Empty Vertex Groups",
    "category": "Mesh",
}

class MESH_OT_vertex_group_remove_empty(bpy.types.Operator):
    """From the selected object, remove all vertex groups with 0 assigned vertex weights"""
    bl_idname = "mesh.vertex_group_remove_empty"
    bl_label = "Remove Empty Groups"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        mesh = context.active_object
        emptyGroups = []
        for vertexGroup in mesh.vertex_groups:
            if (self.isEmpty(vertexGroup, mesh.data.vertices)):
                emptyGroups.append(vertexGroup)
        
        print(f"Removing {len(emptyGroups)} groups")
        for emptyGroup in emptyGroups:
            print(f"  {emptyGroup.name}")

        for emptyVertexGroup in emptyGroups:
            mesh.vertex_groups.remove(emptyVertexGroup)
        return {'FINISHED'}

    @staticmethod
    def isEmpty(vertexGroup, meshVertices):
        for vertex in meshVertices:
            try:
                if vertexGroup.weight(vertex.index) > 0.0:
                    return False
            except RuntimeError:
                # Vertex does not exist in Vgroup
                pass
        return True

    @classmethod
    def poll(cls, context):
        return len(context.active_object.vertex_groups) != 0

def vgroup_menu(self, context):
    self.layout.operator(MESH_OT_vertex_group_remove_empty.bl_idname, icon="X")

def register():
    bpy.utils.register_class(MESH_OT_vertex_group_remove_empty)
    bpy.types.MESH_MT_vertex_group_context_menu.append(vgroup_menu)

def unregister():
    bpy.types.MESH_MT_vertex_group_context_menu.remove(vgroup_menu)
    bpy.utils.unregister_class(MESH_OT_vertex_group_remove_empty)