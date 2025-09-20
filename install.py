#!/usr/bin/env python3
"""
AI城建系统自动安装脚本
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ Python版本过低，需要Python 3.7或更高版本")
        print(f"当前版本：{sys.version}")
        return False
    print(f"✅ Python版本检查通过：{sys.version}")
    return True

def install_requirements():
    """安装依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败：{e}")
        return False

def create_directories():
    """创建必要的目录"""
    directories = ["instance", "logs", "uploads", "backup"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ 创建目录：{directory}")
        else:
            print(f"✅ 目录已存在：{directory}")

def check_database():
    """检查数据库"""
    if os.path.exists("instance/ai_urban_system.db"):
        print("✅ 数据库文件已存在")
    else:
        print("ℹ️ 数据库文件将在首次运行时自动创建")

def main():
    """主安装流程"""
    print("=" * 50)
    print("AI城建系统自动安装程序")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    # 安装依赖
    if not install_requirements():
        sys.exit(1)
    
    # 检查数据库
    check_database()
    
    print("\n" + "=" * 50)
    print("✅ 安装完成！")
    print("=" * 50)
    print("启动方式：")
    print("  Windows: 双击 start.bat")
    print("  Linux/Mac: 运行 ./start.sh")
    print("  或直接运行: python app.py")
    print("\n访问地址：http://localhost:8080")
    print("=" * 50)

if __name__ == "__main__":
    main()
