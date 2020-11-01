import bpy

bl_info = {
    "name": "Merge Vertex Groups",
    "description": "Adds a button to merge vertex groups",
    "author": "Puxtril",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Object Data Properties > Vertex Groups > Vertex Group Specials > Merge Vertex Group",
    "category": "Mesh",
}

class MESH_OT_vertex_group_merge(bpy.types.Operator):
    """For the currently selected vertex group, add the weights of the vertex group below"""
    bl_idname = "mesh.vertex_group_merge"
    bl_label = "Merge Vertex Groups"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        mesh = context.active_object
        groupTop = mesh.vertex_groups.active
        groupBot = mesh.vertex_groups[mesh.vertex_groups.active_index + 1]
        groupNew = mesh.vertex_groups.new()

        try:
            self.mergeGroups(groupTop, groupBot, groupNew, mesh.data.vertices)
            self.moveGroupTo(groupNew, groupBot.index)
        except BaseException as ex:
            mesh.vertex_groups.remove(groupNew)
            self.showMessage(context, str(ex), icon="ERROR")
            return {"CANCELLED"}

        nameTmp = groupTop.name
        mesh.vertex_groups.remove(groupBot)
        mesh.vertex_groups.remove(groupTop)
        groupNew.name = nameTmp

        return {'FINISHED'}

    @classmethod
    def mergeGroups(cls, group1, group2, group3, vertices):
        for vertex in vertices:
            weight1 = cls._getWeight(group1, vertex)
            weight2 = cls._getWeight(group2, vertex)
            weightComb = min(weight1 + weight2, 1.0)
            if weightComb > 0.0:
                group3.add([vertex.index], weightComb, "REPLACE")

    @staticmethod
    def _getWeight(group, vertex):
        try:
            return group.weight(vertex.index)
        except RuntimeError:
            return 0.0

    @staticmethod
    def moveGroupTo(group, targetIndex):
        while group.index > targetIndex:
            bpy.ops.object.vertex_group_move(direction="UP")

    @staticmethod
    def showMessage(context, message = "", title = "Script output", icon = 'INFO'):
        draw = lambda self, context: self.layout.label(text=message)
        context.window_manager.popup_menu(draw, title = title, icon = icon)

    @classmethod
    def poll(cls, context):
        groups = context.active_object.vertex_groups
        return groups.active_index <= (len(groups) - 2)

def vgroup_menu(self, context):
    self.layout.operator(MESH_OT_vertex_group_merge.bl_idname, icon="X")

def register():
    bpy.utils.register_class(MESH_OT_vertex_group_merge)
    bpy.types.MESH_MT_vertex_group_context_menu.append(vgroup_menu)

def unregister():
    bpy.types.MESH_MT_vertex_group_context_menu.remove(vgroup_menu)
    bpy.utils.unregister_class(MESH_OT_vertex_group_merge)