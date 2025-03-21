bl_info = {
    "name": "六边形房屋生成器",
    "author": "AI助手",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > 侧边栏 > 六边形房屋",
    "description": "生成六边形房屋结构阵列",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
import bmesh
import math
import random
from mathutils import Vector
from bpy.props import (
    IntProperty,
    FloatProperty,
    BoolProperty,
    FloatVectorProperty,
    EnumProperty,
)

def create_hexagon_base(radius, height, segments=6):
    """创建六边形基础"""
    bm = bmesh.new()
    
    # 创建顶面顶点
    top_verts = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        top_verts.append(bm.verts.new((x, y, height)))
    
    # 创建底面顶点
    bottom_verts = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        bottom_verts.append(bm.verts.new((x, y, 0)))
    
    # 创建顶面
    bm.faces.new(top_verts)
    
    # 创建底面
    bm.faces.new(bottom_verts[::-1])  # 反向以确保法线朝外
    
    # 创建侧面
    for i in range(segments):
        next_i = (i + 1) % segments
        bm.faces.new([top_verts[i], top_verts[next_i], 
                     bottom_verts[next_i], bottom_verts[i]])
    
    return bm

def add_windows(bm, radius, height, window_height=0.4, window_width=0.3, window_depth=0.05, segments=6):
    """在六边形的侧面添加窗户"""
    for i in range(segments):
        angle = 2 * math.pi * i / segments + (math.pi / segments)  # 中心点
        x = (radius - window_depth) * math.cos(angle)
        y = (radius - window_depth) * math.sin(angle)
        
        # 窗户中心高度
        z_center = height / 2
        
        # 创建窗户 (简化为矩形凹槽)
        window_verts = []
        # 左上
        window_verts.append(bm.verts.new((
            x - window_width/2, 
            y - window_width/2, 
            z_center + window_height/2
        )))
        # 右上
        window_verts.append(bm.verts.new((
            x + window_width/2, 
            y + window_width/2, 
            z_center + window_height/2
        )))
        # 右下
        window_verts.append(bm.verts.new((
            x + window_width/2, 
            y + window_width/2, 
            z_center - window_height/2
        )))
        # 左下
        window_verts.append(bm.verts.new((
            x - window_width/2, 
            y - window_width/2, 
            z_center - window_height/2
        )))
        
        bm.faces.new(window_verts)

def add_interior_grid(bm, radius, height, grid_density=5):
    """添加内部网格结构 - 改进版，更接近图片中的网格结构"""
    # 水平网格
    horizontal_layers = 3  # 水平层数
    
    for layer in range(1, horizontal_layers + 1):
        z = layer * height / (horizontal_layers + 1)
        
        # 创建同心六边形网格
        for scale in [0.3, 0.6, 0.9]:
            inner_radius = radius * scale
            inner_verts = []
            
            for i in range(6):
                angle = 2 * math.pi * i / 6
                x = inner_radius * math.cos(angle)
                y = inner_radius * math.sin(angle)
                inner_verts.append(bm.verts.new((x, y, z)))
            
            # 创建六边形边缘
            for i in range(6):
                next_i = (i + 1) % 6
                bm.edges.new([inner_verts[i], inner_verts[next_i]])
        
        # 创建径向支柱
        for i in range(6):
            angle = 2 * math.pi * i / 6
            for scale in [0.3, 0.6, 0.9]:
                x1 = radius * scale * math.cos(angle)
                y1 = radius * scale * math.sin(angle)
                
                # 如果不是最外层，则连接到下一个同心圆
                if scale < 0.9:
                    x2 = radius * (scale + 0.3) * math.cos(angle)
                    y2 = radius * (scale + 0.3) * math.sin(angle)
                    
                    v1 = bm.verts.new((x1, y1, z))
                    v2 = bm.verts.new((x2, y2, z))
                    bm.edges.new([v1, v2])
    
    # 垂直支柱
    for i in range(6):
        angle = 2 * math.pi * i / 6
        for scale in [0.3, 0.6, 0.9]:
            x = radius * scale * math.cos(angle)
            y = radius * scale * math.sin(angle)
            
            for layer in range(1, horizontal_layers):
                z1 = layer * height / (horizontal_layers + 1)
                z2 = (layer + 1) * height / (horizontal_layers + 1)
                
                v1 = bm.verts.new((x, y, z1))
                v2 = bm.verts.new((x, y, z2))
                bm.edges.new([v1, v2])

def add_lights(bm, radius, height, count=5):
    """添加灯光效果（小球体）- 改进版，更接近图片中的灯光效果"""
    light_positions = []
    
    # 在六边形内部添加随机分布的灯光
    for i in range(count):
        # 使用更合理的随机分布
        r = radius * 0.8 * math.sqrt(random.random())  # 平方根分布使灯光更均匀
        theta = random.random() * 2 * math.pi
        
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = random.uniform(height * 0.2, height * 0.8)  # 在高度范围内随机分布
        
        light_positions.append((x, y, z))
    
    # 在网格的交点处添加更多的灯光
    for layer in range(1, 3):
        z = layer * height / 4
        
        for scale in [0.4, 0.7]:
            for i in range(6):
                angle = 2 * math.pi * i / 6
                x = radius * scale * math.cos(angle)
                y = radius * scale * math.sin(angle)
                
                # 只在部分交点添加灯光，不是所有
                if random.random() < 0.3:  # 30%的概率添加灯光
                    light_positions.append((x, y, z))
    
    # 创建灯光球体
    for pos in light_positions:
        x, y, z = pos
        light_radius = 0.05 + random.random() * 0.05  # 变化的灯光大小
        
        # 创建UV球体
        light_bmesh = bmesh.new()
        bmesh.ops.create_uvsphere(
            light_bmesh, 
            u_segments=8, 
            v_segments=4, 
            radius=light_radius
        )
        
        # 移动到正确位置
        for v in light_bmesh.verts:
            v.co.x += x
            v.co.y += y
            v.co.z += z
        
        # 合并到主网格 - 修复：不使用不存在的add_mesh操作符
        # 而是手动将顶点和面添加到主网格
        verts_map = {}
        for v in light_bmesh.verts:
            new_v = bm.verts.new(v.co)
            verts_map[v] = new_v
            
        for f in light_bmesh.faces:
            new_face_verts = [verts_map[v] for v in f.verts]
            bm.faces.new(new_face_verts)
            
        light_bmesh.free()

def create_single_hexagon_house(radius, height, wall_thickness=0.1, add_details=True):
    """创建单个六边形房屋"""
    bm = create_hexagon_base(radius, height)
    
    # 创建内部六边形（挖空内部）
    inner_bm = create_hexagon_base(radius - wall_thickness, height - wall_thickness)
    
    # 平移内部六边形
    for v in inner_bm.verts:
        v.co.z += wall_thickness / 2
    
    # 反转内部六边形的法线方向
    for f in inner_bm.faces:
        bmesh.ops.reverse_faces(inner_bm, faces=[f])
    
    # 合并两个网格 - 修复：不使用不存在的add_mesh操作符
    # 而是手动将顶点和面添加到主网格
    verts_map = {}
    for v in inner_bm.verts:
        new_v = bm.verts.new(v.co)
        verts_map[v] = new_v
        
    for f in inner_bm.faces:
        new_face_verts = [verts_map[v] for v in f.verts]
        bm.faces.new(new_face_verts)
        
    inner_bm.free()
    
    if add_details:
        # 添加窗户
        add_windows(bm, radius, height)
        
        # 添加内部网格结构
        add_interior_grid(bm, radius - wall_thickness, height - wall_thickness)
        
        # 添加灯光效果
        add_lights(bm, radius - wall_thickness, height - wall_thickness)
    
    return bm

def create_hexagonal_array(rows, columns, radius, height, spacing_factor=1.1, add_details=True):
    """创建六边形房屋阵列"""
    # 计算六边形偏移量
    x_offset = radius * 1.75 * spacing_factor
    y_offset = radius * math.sqrt(3) * spacing_factor
    
    # 创建网格物体
    mesh = bpy.data.meshes.new("HexagonalHousingArray")
    obj = bpy.data.objects.new("HexagonalHousingArray", mesh)
    
    # 链接到场景
    bpy.context.collection.objects.link(obj)
    
    # 创建BMesh
    bm = bmesh.new()
    
    for row in range(rows):
        for col in range(columns):
            # 计算位置
            x = col * x_offset
            y = row * y_offset
            
            # 偶数行需要偏移
            if row % 2 == 1:
                x += radius * spacing_factor
            
            # 创建单个六边形房屋
            single_bm = create_single_hexagon_house(radius, height, add_details=add_details)
            
            # 移动到正确位置
            for v in single_bm.verts:
                v.co.x += x
                v.co.y += y
            
            # 合并到主网格 - 修复：不使用不存在的add_mesh操作符
            # 而是手动将顶点和面添加到主网格
            verts_map = {}
            for v in single_bm.verts:
                new_v = bm.verts.new(v.co)
                verts_map[v] = new_v
                
            for f in single_bm.faces:
                new_face_verts = [verts_map[v] for v in f.verts]
                try:
                    bm.faces.new(new_face_verts)
                except:
                    # 忽略无效面错误
                    pass
                    
            single_bm.free()
    
    # 更新网格
    bm.to_mesh(mesh)
    bm.free()
    
    # 添加发光材质
    if add_details:
        add_emissive_materials(obj)
    
    return obj

def add_emissive_materials(obj):
    """为对象添加基本材质和发光材质"""
    # 创建基本材质
    base_mat = bpy.data.materials.new(name="HexHousing_Base")
    base_mat.use_nodes = True
    nodes = base_mat.node_tree.nodes
    
    # 清除默认节点
    for node in nodes:
        nodes.remove(node)
    
    # 创建新节点
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # 设置材质属性
    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # 深灰色
    principled.inputs['Metallic'].default_value = 0.8
    principled.inputs['Roughness'].default_value = 0.2
    
    # 连接节点
    base_mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # 创建发光材质
    emit_mat = bpy.data.materials.new(name="HexHousing_Emissive")
    emit_mat.use_nodes = True
    nodes = emit_mat.node_tree.nodes
    
    # 清除默认节点
    for node in nodes:
        nodes.remove(node)
    
    # 创建新节点
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # 设置材质属性
    emission.inputs['Color'].default_value = (1.0, 0.8, 0.2, 1.0)  # 温暖的黄色
    emission.inputs['Strength'].default_value = 5.0
    
    # 连接节点
    emit_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # 分配材质到对象
    obj.data.materials.append(base_mat)
    obj.data.materials.append(emit_mat)

class MESH_OT_hexagonal_housing(bpy.types.Operator):
    """创建六边形房屋结构阵列"""
    bl_idname = "mesh.hexagonal_housing_add"
    bl_label = "添加六边形房屋阵列"
    bl_options = {'REGISTER', 'UNDO'}
    
    rows: IntProperty(
        name="行数",
        description="阵列中的行数",
        default=5,
        min=1,
        max=50
    )
    
    columns: IntProperty(
        name="列数",
        description="阵列中的列数",
        default=5,
        min=1,
        max=50
    )
    
    radius: FloatProperty(
        name="半径",
        description="六边形的半径",
        default=1.0,
        min=0.1,
        max=10.0
    )
    
    height: FloatProperty(
        name="高度",
        description="六边形房屋的高度",
        default=2.0,
        min=0.1,
        max=10.0
    )
    
    spacing: FloatProperty(
        name="间距因子",
        description="六边形之间的间距",
        default=1.1,
        min=1.0,
        max=2.0
    )
    
    add_details: BoolProperty(
        name="添加细节",
        description="添加窗户、网格和灯光等细节",
        default=True
    )
    
    def execute(self, context):
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
    """六边形房屋生成器面板"""
    bl_label = "六边形房屋生成器"
    bl_idname = "VIEW3D_PT_hexagonal_housing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "六边形房屋"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("mesh.hexagonal_housing_add", text="生成六边形房屋阵列")

def menu_func(self, context):
    self.layout.operator(MESH_OT_hexagonal_housing.bl_idname, text="六边形房屋阵列")

classes = (
    MESH_OT_hexagonal_housing,
    VIEW3D_PT_hexagonal_housing,
)

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