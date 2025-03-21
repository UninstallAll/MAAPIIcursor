import bpy
import os
import sys

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.realpath(__file__))
plugin_file = os.path.join(current_dir, "hexagonal_housing.py")

# 加载插件
exec(compile(open(plugin_file).read(), plugin_file, 'exec'))

# 创建一个小型测试阵列
bpy.ops.mesh.hexagonal_housing_add(rows=3, columns=3, radius=1.0, height=2.0, spacing=1.1, add_details=True)

# 移动摄像机以便更好地查看结果
if 'Camera' in bpy.data.objects:
    camera = bpy.data.objects['Camera']
    camera.location = (10, -10, 15)
    camera.rotation_euler = (0.5, 0.0, 0.8)

# 添加灯光以便更好地查看模型
light_data = bpy.data.lights.new(name="测试灯光", type='SUN')
light_data.energy = 5.0
light_object = bpy.data.objects.new(name="测试灯光", object_data=light_data)
bpy.context.collection.objects.link(light_object)
light_object.location = (0, 0, 10)
light_object.rotation_euler = (0.5, 0.5, 0)

# 输出成功信息
print("\n\n======================================")
print("六边形房屋生成器插件测试成功!")
print("创建了 3x3 的六边形房屋阵列")
print("======================================\n\n") 