#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL启动脚本
自动检测并启动MySQL服务
"""

import subprocess
import time
import sys
import os

def check_mysql_running():
    """检查MySQL是否运行"""
    try:
        result = subprocess.run(['pgrep', '-x', 'mysqld'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def start_mysql():
    """启动MySQL服务"""
    print("🚀 启动MySQL服务...")
    
    # 尝试不同的启动方法
    start_commands = [
        ['brew', 'services', 'start', 'mysql'],
        ['/opt/homebrew/bin/mysql.server', 'start'],
        ['sudo', '/usr/local/mysql/support-files/mysql.server', 'start'],
        ['sudo', 'systemctl', 'start', 'mysql'],
        ['sudo', 'service', 'mysql', 'start']
    ]
    
    for cmd in start_commands:
        try:
            print(f"📦 尝试启动命令: {' '.join(cmd)}")
            if cmd[0] == 'sudo':
                print("⚠️ 需要管理员权限，请手动执行:")
                print(f"   {' '.join(cmd)}")
                continue
                
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ MySQL启动命令执行成功")
                time.sleep(3)  # 等待启动
                if check_mysql_running():
                    print("✅ MySQL服务启动成功")
                    return True
        except Exception as e:
            print(f"⚠️ 启动失败: {e}")
            continue
    
    return False

def main():
    """主函数"""
    print("🔧 MySQL启动工具")
    print("=" * 30)
    
    if check_mysql_running():
        print("✅ MySQL服务已经在运行")
        return True
    
    if start_mysql():
        print("🎉 MySQL启动成功！")
        return True
    else:
        print("❌ MySQL启动失败")
        print("\n请手动启动MySQL服务:")
        print("1. brew services start mysql")
        print("2. sudo /usr/local/mysql/support-files/mysql.server start")
        print("3. 使用MySQL Workbench启动")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
