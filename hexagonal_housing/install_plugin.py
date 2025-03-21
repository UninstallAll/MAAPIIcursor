import os
import shutil
import sys
import glob
from pathlib import Path

def find_blender_addons_paths():
    """查找所有可能的Blender插件目录路径"""
    possible_paths = []
    
    if sys.platform == "win32":
        # Windows路径
        appdata = os.path.expandvars("%APPDATA%")
        possible_base = os.path.join(appdata, "Blender Foundation", "Blender")
        # 搜索所有版本的Blender文件夹
        for version_dir in glob.glob(os.path.join(possible_base, "*")):
            if os.path.isdir(version_dir):
                addon_path = os.path.join(version_dir, "scripts", "addons")
                possible_paths.append(addon_path)
                
    elif sys.platform == "darwin":
        # macOS路径
        base = os.path.expanduser("~/Library/Application Support/Blender")
        for version_dir in glob.glob(os.path.join(base, "*")):
            if os.path.isdir(version_dir):
                addon_path = os.path.join(version_dir, "scripts", "addons")
                possible_paths.append(addon_path)
                
    else:  # Linux
        # Linux路径
        base = os.path.expanduser("~/.config/blender")
        for version_dir in glob.glob(os.path.join(base, "*")):
            if os.path.isdir(version_dir):
                addon_path = os.path.join(version_dir, "scripts", "addons")
                possible_paths.append(addon_path)
    
    return possible_paths

def verify_plugin_structure():
    """验证插件文件结构是否完整"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.join(current_dir, "hexagonal_housing")
    
    required_files = [
        "__init__.py",
        "operator.py",
        "panel.py",
        "hexagon.py",
        "channel.py",
        "materials.py",
        "utils.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(plugin_dir, file)):
            missing_files.append(file)
    
    return missing_files

def install_plugin():
    """安装插件到Blender"""
    # 验证插件结构
    missing_files = verify_plugin_structure()
    if missing_files:
        print("错误：插件文件结构不完整！")
        print("缺少以下文件：")
        for file in missing_files:
            print(f"- {file}")
        return False
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.join(current_dir, "hexagonal_housing")
    
    # 获取所有可能的Blender插件目录
    addon_paths = find_blender_addons_paths()
    
    if not addon_paths:
        print("错误：未找到Blender插件目录！")
        print("请确保已安装Blender，或手动指定插件目录路径。")
        return False
    
    success = False
    for addon_path in addon_paths:
        try:
            # 创建插件目录（如果不存在）
            os.makedirs(addon_path, exist_ok=True)
            
            # 目标插件目录
            target_dir = os.path.join(addon_path, "hexagonal_housing")
            
            # 如果目标目录已存在，先删除
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            
            # 复制插件文件到Blender插件目录
            shutil.copytree(plugin_dir, target_dir)
            print(f"\n插件已成功安装到: {target_dir}")
            success = True
            
        except Exception as e:
            print(f"\n尝试安装到 {addon_path} 失败：{str(e)}")
            continue
    
    if success:
        print("\n安装成功！")
        print("\n请按照以下步骤在Blender中启用插件：")
        print("1. 打开Blender")
        print("2. 转到 编辑 > 偏好设置")
        print("3. 选择 插件 标签")
        print("4. 搜索 '六边形房屋生成器'")
        print("5. 勾选插件旁边的复选框以启用它")
        print("\n插件将出现在3D视图的侧边栏中（按N键打开）")
        print("在侧边栏中找到 '六边形房屋' 标签即可使用")
        return True
    else:
        print("\n错误：插件安装失败！")
        print("请检查以下可能的问题：")
        print("1. 是否有足够的权限访问Blender插件目录")
        print("2. Blender是否正在运行（建议关闭Blender后再安装）")
        print("3. 插件目录是否正确")
        return False

if __name__ == "__main__":
    install_plugin()