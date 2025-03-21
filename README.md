# 六边形房屋生成器 - Blender插件

这是一个用于在Blender中生成六边形房屋结构阵列的插件。

## 安装说明

### 自动安装（推荐）
1. 确保已安装Python 3.7或更高版本
2. 运行安装脚本：
   ```bash
   python install_plugin.py
   ```
3. 按照脚本输出的说明在Blender中启用插件

### 手动安装
1. 找到Blender的插件目录：
   - Windows: `%APPDATA%\Blender Foundation\Blender\3.0\scripts\addons`
   - macOS: `~/Library/Application Support/Blender/3.0/scripts/addons`
   - Linux: `~/.config/blender/3.0/scripts/addons`
2. 将 `hexagonal_housing` 文件夹复制到插件目录中
3. 重启Blender
4. 在Blender中启用插件：
   - 转到 编辑 > 偏好设置
   - 选择 插件 标签
   - 搜索 "六边形房屋生成器"
   - 勾选插件启用它

## 使用方法

1. 在Blender的3D视图中按 `N` 键打开侧边栏
2. 找到 "六边形房屋" 标签
3. 设置参数：
   - 行数：设置房屋阵列的行数（1-50）
   - 列数：设置房屋阵列的列数（1-50）
   - 高度：设置房屋的高度（0.1-10.0）
   - 生成数量：设置要生成的阵列数量（1-100）
4. 点击 "生成六边形房屋阵列" 按钮生成结构

## 功能特点

- 可调整的房屋尺寸和布局
- 自动生成窗户和内部结构
- 包含基础材质和发光效果
- 房屋之间通过通道连接
- 支持批量生成多个阵列

## 系统要求

- Blender 3.0 或更高版本
- 操作系统：Windows 10/11, macOS 10.15+, Linux

## 故障排除

如果安装过程中遇到问题：

1. 确保您有足够的权限访问Blender插件目录
2. 确保Blender没有在运行
3. 如果插件已存在，请先在Blender中禁用它，然后再重新安装
4. 检查Blender版本是否兼容（3.0或更高）

## 支持与反馈

如果您遇到任何问题或有改进建议，请提交issue。 