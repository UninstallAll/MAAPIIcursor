import bpy

# 设置生成参数
bpy.context.scene.rows = 3        # 设置3行
bpy.context.scene.columns = 4     # 设置4列
bpy.context.scene.height = 2.5    # 设置高度为2.5
bpy.context.scene.count = 1       # 设置生成1组

# 创建六边形房屋阵列
bpy.ops.mesh.hexagonal_housing_add(
    radius=1.0,           # 设置半径
    spacing=1.2,          # 设置间距因子
    add_details=True      # 添加细节（窗户、网格和灯光）
)

# 如果要调整视图以查看整个阵列
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for region in area.regions:
            if region.type == 'WINDOW':
                override = {'area': area, 'region': region}
                bpy.ops.view3d.view_all(override)
                break 