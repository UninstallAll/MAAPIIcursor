import os
import shutil
import sys
import site
from pathlib import Path

def get_blender_addons_path():
    """获取Blender插件目录路径"""
    if sys.platform == "win32":
        return os.path.expanduser("~\\AppData\\Roaming\\Blender Foundation\\Blender\\3.0\\scripts\\addons")
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/Blender/3.0/scripts/addons")
    else:  # Linux
        return os.path.expanduser("~/.config/blender/3.0/scripts/addons")

def install_plugin():
    """安装插件到Blender"""
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.join(current_dir, "hexagonal_housing")
    
    # 获取Blender插件目录
    blender_addons_path = get_blender_addons_path()
    
    # 创建目标目录（如果不存在）
    os.makedirs(blender_addons_path, exist_ok=True)
    
    # 目标插件目录
    target_dir = os.path.join(blender_addons_path, "hexagonal_housing")
    
    # 如果目标目录已存在，先删除
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    try:
        # 复制插件文件到Blender插件目录
        shutil.copytree(plugin_dir, target_dir)
        print(f"插件已成功安装到: {target_dir}")
        print("\n安装成功！")
        print("请按照以下步骤在Blender中启用插件：")
        print("1. 打开Blender")
        print("2. 转到 编辑 > 偏好设置")
        print("3. 选择 插件 标签")
        print("4. 搜索 '六边形房屋生成器'")
        print("5. 勾选插件旁边的复选框以启用它")
        print("\n插件将出现在3D视图的侧边栏中（按N键打开）")
        print("在侧边栏中找到 '六边形房屋' 标签即可使用")
        
    except Exception as e:
        print(f"安装过程中出现错误: {str(e)}")
        print("请确保您有足够的权限访问Blender插件目录")
        return False
    
    return True

if __name__ == "__main__":
    install_plugin() 