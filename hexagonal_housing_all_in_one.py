import bpy
import math
from bpy.props import IntProperty, FloatProperty, BoolProperty, EnumProperty, CollectionProperty, PointerProperty, StringProperty
from mathutils import Vector, Matrix

bl_info = {
    "name": "Hexagonal Housing Generator",
    "author": "AI Assistant",
    "version": (1, 1),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Hex Housing",
    "description": "Generate hexagonal housing structure arrays",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

def create_pipe_mesh(radius, height, shape_type, sides=8):
    """Create a pipe mesh between hexagons"""
    verts = []
    faces = []
    
    # Create vertices based on shape type
    if shape_type == 'CIRCLE':
        sides = 32  # More sides for smoother circle
    elif shape_type == 'SQUARE':
        sides = 4
    elif shape_type == 'TRIANGLE':
        sides = 3
    elif shape_type == 'HEXAGON':
        sides = 6
    # For 'CUSTOM', use the provided sides parameter
    
    # Create vertices for both ends
    for end in range(2):
        for i in range(sides):
            angle = (i * 2 * math.pi) / sides
            # Changed to create vertices in XZ plane (Y is now the pipe length)
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            y = height if end == 1 else 0
            verts.append((x, y, z))
    
    # Create faces
    # End faces
    bottom_face = list(range(sides))
    top_face = list(range(sides, sides * 2))
    faces.append(bottom_face)
    faces.append(top_face[::-1])  # Reverse for correct normal
    
    # Side faces
    for i in range(sides):
        next_i = (i + 1) % sides
        faces.append([i, next_i, next_i + sides, i + sides])
    
    return verts, faces

class AdditionalFeature(bpy.types.PropertyGroup):
    """Property group for additional pipes or holes"""
    name: StringProperty(
        name="Name",
        description="Name of the additional feature",
        default="Feature"
    )
    
    feature_type: EnumProperty(
        name="Type",
        description="Type of additional feature",
        items=[
            ('PIPE', "管道", "Additional connecting pipe"),
            ('HOLE', "空洞", "Additional vertical hole")
        ],
        default='PIPE'
    )
    
    # Pipe properties
    pipe_shape: EnumProperty(
        name="Pipe Shape",
        description="Choose the cross-section shape of the pipe",
        items=[
            ('CIRCLE', "圆形", "Circular cross-section"),
            ('SQUARE', "方形", "Square cross-section"),
            ('TRIANGLE', "三角形", "Triangular cross-section"),
            ('HEXAGON', "六边形", "Hexagonal cross-section"),
            ('CUSTOM', "多边形", "Custom polygon cross-section")
        ],
        default='CIRCLE'
    )
    
    pipe_radius: FloatProperty(
        name="Pipe Radius",
        description="Radius of the connecting pipe",
        default=0.1,
        min=0.01,
        max=1.0,
        precision=3
    )
    
    pipe_sides: IntProperty(
        name="Pipe Sides",
        description="Number of sides for custom polygon pipe shape",
        default=8,
        min=3,
        max=32
    )
    
    # Hole properties
    hole_shape: EnumProperty(
        name="Hole Shape",
        description="Choose the cross-section shape of the hole",
        items=[
            ('CIRCLE', "圆形", "Circular cross-section"),
            ('HEXAGON', "六边形", "Hexagonal cross-section"),
            ('SQUARE', "方形", "Square cross-section"),
            ('TRIANGLE', "三角形", "Triangular cross-section"),
            ('CUSTOM', "多边形", "Custom polygon cross-section")
        ],
        default='CIRCLE'
    )
    
    hole_distance: FloatProperty(
        name="Edge Distance",
        description="Distance from hole to hexagon edges",
        default=0.2,
        min=0.0,
        max=1.0,
        precision=3,
        step=0.1
    )
    
    hole_rotation: FloatProperty(
        name="Hole Rotation",
        description="Rotation angle of the hole in degrees",
        default=0.0,
        min=0.0,
        max=360.0,
        precision=1,
        step=45
    )
    
    hole_sides: IntProperty(
        name="Hole Sides",
        description="Number of sides for custom polygon hole",
        default=8,
        min=3,
        max=32
    )
    
    hole_height_ratio: FloatProperty(
        name="Height Ratio",
        description="Ratio of hole height to hexagon height (0-1)",
        default=1.0,
        min=0.0,
        max=1.0,
        precision=3,
        step=0.1
    )

class MESH_UL_additional_features(bpy.types.UIList):
    """UI list for displaying additional features"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False)
            layout.label(text="管道" if item.feature_type == 'PIPE' else "空洞")

class MESH_OT_add_feature(bpy.types.Operator):
    """Add a new pipe or hole feature"""
    bl_idname = "mesh.add_hex_feature"
    bl_label = "Add Feature"
    bl_options = {'REGISTER', 'UNDO'}
    
    feature_type: EnumProperty(
        name="Type",
        description="Type of feature to add",
        items=[
            ('PIPE', "管道", "Add a new pipe"),
            ('HOLE', "空洞", "Add a new hole")
        ],
        default='PIPE'
    )
    
    def execute(self, context):
        features = context.scene.additional_features
        new_feature = features.add()
        new_feature.feature_type = self.feature_type
        new_feature.name = f"{'管道' if self.feature_type == 'PIPE' else '空洞'} {len(features)}"
        context.scene.active_feature_index = len(features) - 1
        return {'FINISHED'}

class MESH_OT_remove_feature(bpy.types.Operator):
    """Remove the selected feature"""
    bl_idname = "mesh.remove_hex_feature"
    bl_label = "Remove Feature"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        features = context.scene.additional_features
        index = context.scene.active_feature_index
        
        if index >= 0 and index < len(features):
            features.remove(index)
            context.scene.active_feature_index = min(max(0, index - 1), len(features) - 1)
        
        return {'FINISHED'}

def create_hexagonal_array(context):
    """Create an array of hexagonal structures"""
    scene = context.scene
    
    # Get parameters from scene
    rows = scene.hex_rows
    columns = scene.hex_columns
    layers = scene.hex_layers
    layer_offset_x = scene.hex_layer_offset_x
    layer_offset_y = scene.hex_layer_offset_y
    radius = scene.hex_radius
    height = scene.hex_height
    center_distance = scene.hex_center_distance
    arrangement_mode = scene.hex_arrangement_mode
    
    # Get pipe parameters
    generate_pipes = scene.hex_generate_pipes
    pipe_shape = scene.hex_pipe_shape
    pipe_radius = scene.hex_pipe_radius
    pipe_sides = scene.hex_pipe_sides
    
    # Get hole parameters
    generate_holes = scene.hex_generate_holes
    hole_shape = scene.hex_hole_shape
    hole_distance = scene.hex_hole_distance
    hole_rotation = scene.hex_hole_rotation
    hole_sides = scene.hex_hole_sides
    hole_height_ratio = scene.hex_hole_height_ratio
    
    # Get additional features
    additional_features = scene.additional_features
    
    # Create collections
    array_collection = bpy.data.collections.new("Hexagonal Array")
    context.scene.collection.children.link(array_collection)
    if generate_pipes or any(f.feature_type == 'PIPE' for f in additional_features):
        pipe_collection = bpy.data.collections.new("Pipes")
        context.scene.collection.children.link(pipe_collection)
    
    # Function to create hexagon mesh WITH holes directly
    def create_hexagon_mesh_with_holes(radius, height, hole_params=None):
        verts = []
        faces = []
        
        # Create hexagon vertices (without holes)
        # Create bottom vertices
        bottom_hex_verts = []
        for i in range(6):
            angle = (i * math.pi / 3) + (math.pi / 6)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            bottom_hex_verts.append(len(verts))
            verts.append((x, y, 0))
        
        # Create top vertices
        top_hex_verts = []
        for i in range(6):
            angle = (i * math.pi / 3) + (math.pi / 6)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            top_hex_verts.append(len(verts))
            verts.append((x, y, height))
        
        # If no holes, just create the hexagon
        if not hole_params or len(hole_params) == 0:
            # Bottom face
            faces.append(bottom_hex_verts)
            # Top face
            faces.append(top_hex_verts[::-1])  # Reverse for correct normal direction
            # Side faces
            for i in range(6):
                next_i = (i + 1) % 6
                faces.append([bottom_hex_verts[i], bottom_hex_verts[next_i],
                            top_hex_verts[next_i], top_hex_verts[i]])
            
            return verts, faces
        
        # If we have holes, we need to handle them
        # Store all hole vertices for each face
        bottom_holes = []
        top_holes = []
        side_faces = []
        
        # Create vertices for each hole
        for params in hole_params:
            hole_radius = radius - params['distance']
            if hole_radius <= 0:
                hole_radius = radius * 0.1
            
            # Calculate number of sides for hole
            if params['shape'] == 'CIRCLE':
                sides = 32
            elif params['shape'] == 'HEXAGON':
                sides = 6
            elif params['shape'] == 'SQUARE':
                sides = 4
            elif params['shape'] == 'TRIANGLE':
                sides = 3
            else:  # CUSTOM
                sides = params['sides']
            
            # Create hole vertices
            bottom_hole_verts = []
            for i in range(sides):
                angle = (i * 2 * math.pi / sides) + math.radians(params['rotation'])
                x = hole_radius * math.cos(angle)
                y = hole_radius * math.sin(angle)
                bottom_hole_verts.append(len(verts))
                verts.append((x, y, 0))
            
            # Add to bottom holes list (reversed for correct face orientation)
            bottom_holes.append(bottom_hole_verts[::-1])
            
            # Create top hole vertices if not a complete through-hole
            hole_height = height * params['height_ratio']
            top_hole_verts = []
            for i in range(sides):
                angle = (i * 2 * math.pi / sides) + math.radians(params['rotation'])
                x = hole_radius * math.cos(angle)
                y = hole_radius * math.sin(angle)
                top_hole_verts.append(len(verts))
                verts.append((x, y, hole_height))
            
            # Add to top holes list
            top_holes.append(top_hole_verts)
            
            # Create side faces for hole
            for i in range(sides):
                next_i = (i + 1) % sides
                side_faces.append([bottom_hole_verts[i], bottom_hole_verts[next_i],
                                 top_hole_verts[next_i], top_hole_verts[i]])
        
        # Now create faces with holes
        # For bottom face (Use triangulation to create face with holes)
        triangulate_face_with_holes(verts, faces, bottom_hex_verts, bottom_holes)
        
        # For top face (Use triangulation to create face with holes)
        triangulate_face_with_holes(verts, faces, top_hex_verts[::-1], [h[::-1] for h in top_holes])
        
        # Add hexagon side faces
        for i in range(6):
            next_i = (i + 1) % 6
            faces.append([bottom_hex_verts[i], bottom_hex_verts[next_i],
                        top_hex_verts[next_i], top_hex_verts[i]])
        
        # Add all hole side faces
        faces.extend(side_faces)
        
        return verts, faces
    
    def triangulate_face_with_holes(verts, faces, outer_contour, holes):
        """Create triangulated faces for a polygon with holes"""
        # Basic triangulation (this is a simplified version)
        # For production, you might want to use more advanced triangulation algorithms
        
        # If no holes, just return the face
        if not holes or len(holes) == 0:
            faces.append(outer_contour)
            return
        
        # Create triangles connecting outer contour with each hole
        for hole in holes:
            # Find a vertex on the outer contour and hole to connect
            outer_point = outer_contour[0]
            hole_point = hole[0]
            
            # Create a "bridge" between the outer contour and hole
            bridge_points = [outer_point, hole_point]
            
            # Create triangles along the bridge
            for i in range(1, len(outer_contour)):
                faces.append([outer_point, outer_contour[i], outer_contour[i-1]])
            
            for i in range(1, len(hole)):
                faces.append([hole_point, hole[i-1], hole[i]])
    
    # Store hexagon positions for pipe creation
    hexagon_positions = []
    
    # Calculate grid offsets based on arrangement mode
    if arrangement_mode == 'HONEYCOMB':
        x_offset = center_distance
        y_offset = center_distance * math.sqrt(3) / 2  # This ensures equal distances between centers
    else:  # GRID mode
        x_offset = center_distance
        y_offset = center_distance
    
    # Generate array based on arrangement mode and layers
    for layer in range(layers):
        layer_z = layer * height  # Calculate Z position for current layer
        layer_x_offset = layer * layer_offset_x  # Calculate X offset for current layer
        layer_y_offset = layer * layer_offset_y  # Calculate Y offset for current layer
        
        for row in range(rows):
            row_offset = (x_offset / 2) if (arrangement_mode == 'HONEYCOMB' and row % 2) else 0
            for col in range(columns):
                x = (col * x_offset) + row_offset + layer_x_offset
                y = row * y_offset + layer_y_offset
                
                # Prepare hole parameters list for this hexagon
                hole_params = []
                
                # Add main hole if enabled
                if generate_holes:
                    hole_params.append({
                        'shape': hole_shape,
                        'distance': hole_distance,
                        'rotation': hole_rotation,
                        'sides': hole_sides,
                        'height_ratio': hole_height_ratio
                    })
                
                # Add additional holes
                for feature in additional_features:
                    if feature.feature_type == 'HOLE':
                        hole_params.append({
                            'shape': feature.hole_shape,
                            'distance': feature.hole_distance,
                            'rotation': feature.hole_rotation,
                            'sides': feature.hole_sides,
                            'height_ratio': feature.hole_height_ratio
                        })
                
                # Create hexagon mesh with holes directly
                hex_verts, hex_faces = create_hexagon_mesh_with_holes(radius, height, hole_params)
                
                # Create the mesh
                mesh_name = f"Hexagon_{layer}_{row}_{col}"
                hex_mesh = bpy.data.meshes.new(mesh_name)
                hex_mesh.from_pydata(hex_verts, [], hex_faces)
                hex_mesh.update()
                
                # Create object
                obj = bpy.data.objects.new(mesh_name, hex_mesh)
                array_collection.objects.link(obj)
                obj.location = Vector((x, y, layer_z))
                
                # Create hexagon material
                mat = bpy.data.materials.new(name="HexagonMaterial")
                mat.use_nodes = True
                nodes = mat.node_tree.nodes
                nodes.clear()
                
                # Create a simple material
                node_material = nodes.new(type='ShaderNodeBsdfPrincipled')
                node_material.inputs[0].default_value = (0.8, 0.8, 0.8, 1)  # Light gray
                node_output = nodes.new(type='ShaderNodeOutputMaterial')
                mat.node_tree.links.new(node_material.outputs[0], node_output.inputs[0])
                
                # Apply material
                if obj.data.materials:
                    obj.data.materials[0] = mat
                else:
                    obj.data.materials.append(mat)
                
                # Store position for pipe creation
                hexagon_positions.append((x, y, layer_z, layer, row, col))
    
    # Create pipes
    # Create additional pipe collections
    pipe_collections = {}
    if generate_pipes or any(f.feature_type == 'PIPE' for f in additional_features):
        if generate_pipes:
            pipe_collections['main'] = pipe_collection
        
        for i, feature in enumerate(additional_features):
            if feature.feature_type == 'PIPE':
                coll = bpy.data.collections.new(f"Pipes_{feature.name}")
                context.scene.collection.children.link(coll)
                pipe_collections[feature.name] = coll
    
    if pipe_collections:
        # Create pipes for each pipe type
        for feature_name, collection in pipe_collections.items():
            # Get pipe parameters
            if feature_name == 'main':
                p_shape = pipe_shape
                p_radius = pipe_radius
                p_sides = pipe_sides
            else:
                feature = next(f for f in additional_features if f.name == feature_name)
                p_shape = feature.pipe_shape
                p_radius = feature.pipe_radius
                p_sides = feature.pipe_sides
            
            # Create pipe mesh
            pipe_verts, pipe_faces = create_pipe_mesh(
                p_radius,
                center_distance,
                p_shape,
                p_sides
            )
            pipe_mesh = bpy.data.meshes.new(f"PipeBase_{feature_name}")
            pipe_mesh.from_pydata(pipe_verts, [], pipe_faces)
            pipe_mesh.update()
            
            # Create pipe material
            pipe_mat = bpy.data.materials.new(name="PipeMaterial")
            pipe_mat.use_nodes = True
            nodes = pipe_mat.node_tree.nodes
            nodes.clear()
            node_material = nodes.new(type='ShaderNodeBsdfPrincipled')
            node_material.inputs[0].default_value = (0.6, 0.6, 0.6, 1)  # Darker gray
            node_output = nodes.new(type='ShaderNodeOutputMaterial')
            pipe_mat.node_tree.links.new(node_material.outputs[0], node_output.inputs[0])
            
            # Function to create a pipe between two positions
            def create_pipe(start_pos, end_pos, collection):
                # Calculate direction vector between centers
                direction = Vector(end_pos) - Vector(start_pos)
                direction.normalize()
                
                # Create up vector (Z-axis)
                up = Vector((0, 0, 1))
                
                # Calculate right vector (perpendicular to direction and up)
                right = direction.cross(up)
                right.normalize()
                
                # Recalculate up vector to ensure perfect perpendicularity
                up = right.cross(direction)
                up.normalize()
                
                # Create rotation matrix from these vectors
                rot_matrix = Matrix((right, direction, up)).transposed()
                
                # Create pipe object
                pipe = bpy.data.objects.new("Pipe", pipe_mesh)
                collection.objects.link(pipe)
                
                # Position pipe at start position
                pipe.location = Vector(start_pos)
                
                # Apply rotation from matrix
                pipe.rotation_euler = rot_matrix.to_euler('XYZ')
                
                # Scale pipe to match distance
                distance = (Vector(end_pos) - Vector(start_pos)).length
                pipe.scale.y = distance / center_distance
                
                # Apply material
                if pipe.data.materials:
                    pipe.data.materials[0] = pipe_mat
                else:
                    pipe.data.materials.append(pipe_mat)
            
            # Create pipes between adjacent hexagons
            processed_pairs = set()  # Keep track of connected pairs
            
            for i, (x, y, z, layer, row, col) in enumerate(hexagon_positions):
                current_pos = (x, y, z)
                
                # Connect to neighbors based on arrangement mode
                if arrangement_mode == 'HONEYCOMB':
                    # Define possible neighbor offsets for honeycomb pattern
                    # Each offset is (dx, dy, dz, condition)
                    neighbor_offsets = [
                        (x_offset, 0, 0, col < columns - 1),  # Right
                        (x_offset/2, y_offset, 0, row < rows - 1 and col < columns - 1),  # Lower right
                        (-x_offset/2, y_offset, 0, row < rows - 1 and col > 0),  # Lower left
                        (0, 0, height, layer < layers - 1)  # Up to next layer
                    ]
                    
                    if row % 2 == 1:  # Odd rows are shifted
                        neighbor_offsets = [
                            (x_offset, 0, 0, col < columns - 1),  # Right
                            (x_offset/2, -y_offset, 0, row > 0 and col < columns - 1),  # Upper right
                            (-x_offset/2, -y_offset, 0, row > 0 and col > 0),  # Upper left
                            (0, 0, height, layer < layers - 1)  # Up to next layer
                        ]
                else:  # GRID mode
                    neighbor_offsets = [
                        (x_offset, 0, 0, col < columns - 1),  # Right
                        (0, y_offset, 0, row < rows - 1),  # Down
                        (0, 0, height, layer < layers - 1)  # Up to next layer
                    ]
                
                # Create pipes to valid neighbors
                for dx, dy, dz, condition in neighbor_offsets:
                    if condition:
                        next_pos = (x + dx, y + dy, z + dz)
                        
                        # Create unique identifier for this pipe connection
                        pipe_id = tuple(sorted([current_pos, next_pos]))
                        
                        # Only create pipe if this connection hasn't been processed
                        if pipe_id not in processed_pairs:
                            processed_pairs.add(pipe_id)
                            
                            # Calculate pipe endpoints at hexagon centers
                            start_pos = (x, y, z + height/2)
                            end_pos = (x + dx, y + dy, z + dz + height/2)
                            
                            create_pipe(start_pos, end_pos, collection)
    
    # Select the collection
    for obj in array_collection.objects:
        obj.select_set(True)
    
    # Set active object
    if array_collection.objects:
        context.view_layer.objects.active = array_collection.objects[0]
    
    return {'FINISHED'}

class MESH_OT_hexagonal_housing(bpy.types.Operator):
    """Create hexagonal housing structure array"""
    bl_idname = "mesh.hexagonal_housing_add"
    bl_label = "Add Hexagonal Housing Array"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        return create_hexagonal_array(context)

class VIEW3D_PT_hexagonal_housing(bpy.types.Panel):
    """Hexagonal Housing Generator Panel"""
    bl_label = "Hexagonal Housing Generator"
    bl_idname = "VIEW3D_PT_hexagonal_housing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Hex Housing"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Arrangement mode
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Arrangement Mode:")
        col.prop(scene, "hex_arrangement_mode", text="")
        
        # Array parameters
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Array Parameters:")
        col.prop(scene, "hex_rows", text="Rows")
        col.prop(scene, "hex_columns", text="Columns")
        col.prop(scene, "hex_layers", text="Layers")
        
        # Layer offset parameters
        if scene.hex_layers > 1:  # Only show if multiple layers
            box = layout.box()
            col = box.column(align=True)
            col.label(text="Layer Offset:")
            col.prop(scene, "hex_layer_offset_x", text="X Offset")
            col.prop(scene, "hex_layer_offset_y", text="Y Offset")
        
        # Size parameters
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Size Parameters:")
        col.prop(scene, "hex_radius", text="Radius")
        col.prop(scene, "hex_height", text="Height")
        
        # Spacing parameter
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Spacing Parameter:")
        col.prop(scene, "hex_center_distance", text="Center Distance")
        
        # Pipe parameters
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Pipe Parameters:")
        row = col.row()
        row.prop(scene, "hex_generate_pipes", text="Generate Pipes")
        
        # Only show pipe options if pipes are enabled
        if scene.hex_generate_pipes:
            col.prop(scene, "hex_pipe_shape", text="Pipe Shape")
            col.prop(scene, "hex_pipe_radius", text="Pipe Radius")
            if scene.hex_pipe_shape == 'CUSTOM':
                col.prop(scene, "hex_pipe_sides", text="Pipe Sides")
        
        # Hole parameters
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Vertical Hole:")
        row = col.row()
        row.prop(scene, "hex_generate_holes", text="Generate Holes")
        
        # Only show hole options if holes are enabled
        if scene.hex_generate_holes:
            col.prop(scene, "hex_hole_shape", text="Hole Shape")
            col.prop(scene, "hex_hole_distance", text="Edge Distance")
            col.prop(scene, "hex_hole_rotation", text="Rotation")
            col.prop(scene, "hex_hole_height_ratio", text="Height Ratio")
            if scene.hex_hole_shape == 'CUSTOM':
                col.prop(scene, "hex_hole_sides", text="Hole Sides")
        
        # Additional features
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Additional Features:")
        
        # List of additional features
        row = col.row()
        row.template_list("MESH_UL_additional_features", "", scene, "additional_features",
                         scene, "active_feature_index", rows=3)
        
        # Add/Remove buttons
        col = row.column(align=True)
        col.operator_menu_enum("mesh.add_hex_feature", "feature_type", text="", icon='ADD')
        col.operator("mesh.remove_hex_feature", text="", icon='REMOVE')
        
        # Selected feature settings
        if len(scene.additional_features) > 0 and scene.active_feature_index >= 0:
            feature = scene.additional_features[scene.active_feature_index]
            box = layout.box()
            col = box.column(align=True)
            col.label(text=f"Feature Settings ({feature.name}):")
            
            if feature.feature_type == 'PIPE':
                col.prop(feature, "pipe_shape", text="Pipe Shape")
                col.prop(feature, "pipe_radius", text="Pipe Radius")
                if feature.pipe_shape == 'CUSTOM':
                    col.prop(feature, "pipe_sides", text="Pipe Sides")
            else:  # HOLE
                col.prop(feature, "hole_shape", text="Hole Shape")
                col.prop(feature, "hole_distance", text="Edge Distance")
                col.prop(feature, "hole_rotation", text="Rotation")
                col.prop(feature, "hole_height_ratio", text="Height Ratio")
                if feature.hole_shape == 'CUSTOM':
                    col.prop(feature, "hole_sides", text="Hole Sides")
        
        # Create operator button
        layout.separator()
        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator("mesh.hexagonal_housing_add", text="Generate Hexagonal Array")

classes = (
    AdditionalFeature,
    MESH_UL_additional_features,
    MESH_OT_add_feature,
    MESH_OT_remove_feature,
    MESH_OT_hexagonal_housing,
    VIEW3D_PT_hexagonal_housing,
)

def register():
    # First register the property group class
    bpy.utils.register_class(AdditionalFeature)
    
    # Then register other classes
    bpy.utils.register_class(MESH_UL_additional_features)
    bpy.utils.register_class(MESH_OT_add_feature)
    bpy.utils.register_class(MESH_OT_remove_feature)
    bpy.utils.register_class(MESH_OT_hexagonal_housing)
    bpy.utils.register_class(VIEW3D_PT_hexagonal_housing)
    
    # Register scene properties
    bpy.types.Scene.hex_arrangement_mode = EnumProperty(
        name="Arrangement Mode",
        description="Choose the arrangement pattern for hexagons",
        items=[
            ('HONEYCOMB', "蜂巢状", "Arrange hexagons in a honeycomb pattern with staggered rows"),
            ('GRID', "并列状", "Arrange hexagons in a grid pattern with aligned centers")
        ],
        default='HONEYCOMB'
    )
    
    bpy.types.Scene.hex_rows = IntProperty(
        name="Rows",
        description="Number of rows in the array",
        default=5,
        min=1,
        max=20
    )
    
    bpy.types.Scene.hex_columns = IntProperty(
        name="Columns",
        description="Number of columns in the array",
        default=6,
        min=1,
        max=20
    )
    
    bpy.types.Scene.hex_layers = IntProperty(
        name="Layers",
        description="Number of vertical layers in the array",
        default=1,
        min=1,
        max=20
    )
    
    bpy.types.Scene.hex_radius = FloatProperty(
        name="Radius",
        description="Radius of the hexagon",
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    bpy.types.Scene.hex_height = FloatProperty(
        name="Height",
        description="Height of the hexagonal housing",
        default=2.0,
        min=0.1,
        max=5.0
    )
    
    bpy.types.Scene.hex_center_distance = FloatProperty(
        name="Center Distance",
        description="Distance between centers of adjacent hexagons",
        default=2.5,
        min=0.0,
        max=100.0,
        precision=3,
        step=1
    )
    
    bpy.types.Scene.hex_generate_pipes = BoolProperty(
        name="Generate Pipes",
        description="Generate connecting pipes between hexagons",
        default=False
    )
    
    bpy.types.Scene.hex_pipe_shape = EnumProperty(
        name="Pipe Shape",
        description="Choose the cross-section shape of the pipes",
        items=[
            ('CIRCLE', "圆形", "Circular cross-section"),
            ('SQUARE', "方形", "Square cross-section"),
            ('TRIANGLE', "三角形", "Triangular cross-section"),
            ('HEXAGON', "六边形", "Hexagonal cross-section"),
            ('CUSTOM', "多边形", "Custom polygon cross-section")
        ],
        default='CIRCLE'
    )
    
    bpy.types.Scene.hex_pipe_radius = FloatProperty(
        name="Pipe Radius",
        description="Radius of the connecting pipes",
        default=0.1,
        min=0.01,
        max=1.0,
        precision=3
    )
    
    bpy.types.Scene.hex_pipe_sides = IntProperty(
        name="Pipe Sides",
        description="Number of sides for custom polygon pipe shape",
        default=8,
        min=3,
        max=32
    )
    
    bpy.types.Scene.hex_layer_offset_x = FloatProperty(
        name="Layer X Offset",
        description="X-axis offset between consecutive layers",
        default=0.0,
        min=-10.0,
        max=10.0,
        precision=3,
        step=0.1
    )
    
    bpy.types.Scene.hex_layer_offset_y = FloatProperty(
        name="Layer Y Offset",
        description="Y-axis offset between consecutive layers",
        default=0.0,
        min=-10.0,
        max=10.0,
        precision=3,
        step=0.1
    )
    
    bpy.types.Scene.hex_generate_holes = BoolProperty(
        name="Generate Holes",
        description="Generate vertical holes in hexagons",
        default=False
    )
    
    bpy.types.Scene.hex_hole_shape = EnumProperty(
        name="Hole Shape",
        description="Choose the cross-section shape of the holes",
        items=[
            ('CIRCLE', "圆形", "Circular cross-section"),
            ('HEXAGON', "六边形", "Hexagonal cross-section"),
            ('SQUARE', "方形", "Square cross-section"),
            ('TRIANGLE', "三角形", "Triangular cross-section"),
            ('CUSTOM', "多边形", "Custom polygon cross-section")
        ],
        default='CIRCLE'
    )
    
    bpy.types.Scene.hex_hole_distance = FloatProperty(
        name="Edge Distance",
        description="Distance from hole to hexagon edges",
        default=0.2,
        min=0.0,
        max=1.0,
        precision=3,
        step=0.1
    )
    
    bpy.types.Scene.hex_hole_rotation = FloatProperty(
        name="Hole Rotation",
        description="Rotation angle of the hole in degrees",
        default=0.0,
        min=0.0,
        max=360.0,
        precision=1,
        step=45
    )
    
    bpy.types.Scene.hex_hole_sides = IntProperty(
        name="Hole Sides",
        description="Number of sides for custom polygon hole",
        default=8,
        min=3,
        max=32
    )
    
    bpy.types.Scene.hex_hole_height_ratio = FloatProperty(
        name="Height Ratio",
        description="Ratio of hole height to hexagon height (0-1)",
        default=1.0,
        min=0.0,
        max=1.0,
        precision=3,
        step=0.1
    )
    
    # Register additional feature properties AFTER the property group class is registered
    bpy.types.Scene.additional_features = CollectionProperty(type=AdditionalFeature)
    bpy.types.Scene.active_feature_index = IntProperty(name="Active Feature Index")

def unregister():
    # First unregister the properties
    del bpy.types.Scene.active_feature_index
    del bpy.types.Scene.additional_features
    del bpy.types.Scene.hex_arrangement_mode
    del bpy.types.Scene.hex_rows
    del bpy.types.Scene.hex_columns
    del bpy.types.Scene.hex_layers
    del bpy.types.Scene.hex_radius
    del bpy.types.Scene.hex_height
    del bpy.types.Scene.hex_center_distance
    del bpy.types.Scene.hex_generate_pipes
    del bpy.types.Scene.hex_pipe_shape
    del bpy.types.Scene.hex_pipe_radius
    del bpy.types.Scene.hex_pipe_sides
    del bpy.types.Scene.hex_layer_offset_x
    del bpy.types.Scene.hex_layer_offset_y
    del bpy.types.Scene.hex_generate_holes
    del bpy.types.Scene.hex_hole_shape
    del bpy.types.Scene.hex_hole_distance
    del bpy.types.Scene.hex_hole_rotation
    del bpy.types.Scene.hex_hole_sides
    del bpy.types.Scene.hex_hole_height_ratio
    
    # Then unregister classes in reverse order
    bpy.utils.unregister_class(VIEW3D_PT_hexagonal_housing)
    bpy.utils.unregister_class(MESH_OT_hexagonal_housing)
    bpy.utils.unregister_class(MESH_OT_remove_feature)
    bpy.utils.unregister_class(MESH_OT_add_feature)
    bpy.utils.unregister_class(MESH_UL_additional_features)
    bpy.utils.unregister_class(AdditionalFeature)

if __name__ == "__main__":
    register() 