import bpy
import bmesh
import math
from bpy.props import IntProperty, FloatProperty, BoolProperty
from mathutils import Vector, Matrix

bl_info = {
    "name": "Hexagonal Housing Generator",
    "author": "AI Assistant",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Hex Housing",
    "description": "Generate hexagonal housing structure arrays",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

def create_hexagon(radius, height):
    """Create a basic hexagonal mesh"""
    vertices = []
    faces = []
    
    # Create bottom vertices
    for i in range(6):
        angle = i * math.pi / 3
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append(Vector((x, y, 0)))
    
    # Create top vertices
    for i in range(6):
        angle = i * math.pi / 3
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append(Vector((x, y, height)))
    
    # Create bottom face
    faces.append([0, 1, 2, 3, 4, 5])
    
    # Create top face
    faces.append([6, 7, 8, 9, 10, 11])
    
    # Create side faces
    for i in range(6):
        faces.append([i, (i + 1) % 6, ((i + 1) % 6) + 6, i + 6])
    
    return vertices, faces

def add_windows(obj, window_height=0.5, window_width=0.3):
    """Add windows to the hexagonal structure"""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Add window cuts on each side face
    for face in bm.faces:
        if len(face.verts) == 4:  # Side faces are quads
            # Calculate face center and dimensions
            center = face.calc_center_median()
            
            # Create window cut
            bmesh.ops.create_grid(
                bm,
                x_segments=1,
                y_segments=1,
                size=window_width,
                matrix=Matrix.Translation(center)
            )
    
    bm.to_mesh(obj.data)
    obj.data.update()
    bm.free()

def add_details(obj):
    """Add architectural details to the structure"""
    # Add windows
    add_windows(obj)
    
    # Add material slots for different parts
    if len(obj.material_slots) == 0:
        obj.data.materials.append(None)  # Add empty material slot
        obj.data.materials.append(None)  # Add second empty material slot

def create_hexagonal_array(rows, columns, radius, height, spacing, add_details_bool):
    """Create an array of hexagonal structures"""
    # Calculate offsets for hex grid
    x_offset = radius * 2 * spacing
    y_offset = radius * math.sqrt(3) * spacing
    
    for row in range(rows):
        for col in range(columns):
            # Calculate position
            x = col * x_offset + (row % 2) * (x_offset / 2)
            y = row * y_offset
            
            # Create vertices and faces
            verts, faces = create_hexagon(radius, height)
            
            # Create mesh and object
            mesh = bpy.data.meshes.new(name="HexagonalHousing")
            obj = bpy.data.objects.new("HexagonalHousing", mesh)
            
            # Link object to scene
            bpy.context.collection.objects.link(obj)
            
            # Create mesh from vertices and faces
            mesh.from_pydata(verts, [], faces)
            mesh.update()
            
            # Set object location
            obj.location = Vector((x, y, 0))
            
            # Add details if requested
            if add_details_bool:
                add_details(obj)
            
            # Select the created object
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

class MESH_OT_hexagonal_housing(bpy.types.Operator):
    """Create hexagonal housing structure array"""
    bl_idname = "mesh.hexagonal_housing_add"
    bl_label = "Add Hexagonal Housing Array"
    bl_options = {'REGISTER', 'UNDO'}
    
    rows: IntProperty(
        name="Rows",
        description="Number of rows in the array",
        default=5,
        min=1,
        max=50
    )
    
    columns: IntProperty(
        name="Columns",
        description="Number of columns in the array",
        default=5,
        min=1,
        max=50
    )
    
    radius: FloatProperty(
        name="Radius",
        description="Radius of the hexagon",
        default=1.0,
        min=0.1,
        max=10.0
    )
    
    height: FloatProperty(
        name="Height",
        description="Height of the hexagonal housing",
        default=2.0,
        min=0.1,
        max=10.0
    )
    
    spacing: FloatProperty(
        name="Spacing",
        description="Spacing between hexagons",
        default=1.1,
        min=1.0,
        max=2.0
    )
    
    add_details: BoolProperty(
        name="Add Details",
        description="Add windows, grids, and lights",
        default=True
    )
    
    count: IntProperty(
        name="Count",
        description="Number of housing arrays to generate",
        default=1,
        min=1,
        max=100
    )
    
    def execute(self, context):
        for _ in range(self.count):
            create_hexagonal_array(
                self.rows,
                self.columns,
                self.radius,
                self.height,
                self.spacing,
                self.add_details
            )
        return {'FINISHED'}

class VIEW3D_PT_hexagonal_housing(bpy.types.Panel):
    """Hexagonal Housing Generator Panel"""
    bl_label = "Hexagonal Housing Generator"
    bl_idname = "VIEW3D_PT_hexagonal_housing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Hex Housing"
    
    def draw(self, context):
        layout = self.layout
        
        # Create operator layout
        op = layout.operator("mesh.hexagonal_housing_add", text="Generate Housing Array")
        
        # Add all properties
        layout.prop(op, "rows", text="Rows")
        layout.prop(op, "columns", text="Columns")
        layout.prop(op, "radius", text="Radius")
        layout.prop(op, "height", text="Height")
        layout.prop(op, "spacing", text="Spacing")
        layout.prop(op, "add_details", text="Add Details")
        layout.prop(op, "count", text="Count")

classes = (
    MESH_OT_hexagonal_housing,
    VIEW3D_PT_hexagonal_housing,
)

def menu_func(self, context):
    self.layout.operator(MESH_OT_hexagonal_housing.bl_idname, text="Hexagonal Housing Array")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register() 