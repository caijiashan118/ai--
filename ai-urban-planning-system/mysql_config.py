#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL数据库配置脚本
自动配置MySQL数据库连接和表结构
"""

import os
import sys
import pymysql
import subprocess
import time

def check_mysql_installation():
    """检查MySQL是否已安装"""
    print("🔍 检查MySQL安装状态...")
    
    # 检查MySQL命令是否存在
    mysql_paths = [
        '/usr/local/mysql/bin/mysql',
        '/usr/bin/mysql',
        '/opt/homebrew/bin/mysql',
        'mysql'  # 如果在PATH中
    ]
    
    mysql_path = None
    for path in mysql_paths:
        try:
            result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                mysql_path = path
                print(f"✅ 找到MySQL: {path}")
                print(f"   版本: {result.stdout.strip()}")
                break
        except:
            continue
    
    if not mysql_path:
        print("❌ 未找到MySQL安装")
        print("请先安装MySQL:")
        print("1. macOS: brew install mysql")
        print("2. 或从官网下载: https://dev.mysql.com/downloads/mysql/")
        return None
    
    return mysql_path

def start_mysql_service():
    """启动MySQL服务"""
    print("🚀 启动MySQL服务...")
    
    # 尝试不同的启动方法
    start_commands = [
        ['brew', 'services', 'start', 'mysql'],
        ['sudo', '/usr/local/mysql/support-files/mysql.server', 'start'],
        ['/opt/homebrew/bin/mysql.server', 'start'],
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
                    return True
        except Exception as e:
            print(f"⚠️ 启动失败: {e}")
            continue
    
    return False

def check_mysql_running():
    """检查MySQL是否运行"""
    try:
        result = subprocess.run(['pgrep', '-x', 'mysqld'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def test_mysql_connection(host='localhost', port=3306, user='root', password=''):
    """测试MySQL连接"""
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        print(f"✅ MySQL连接成功: {user}@{host}:{port}")
        return connection
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        return None

def create_database(connection, db_name='ai_urban_system'):
    """创建数据库"""
    print(f"📊 创建数据库: {db_name}")
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.commit()
        print(f"✅ 数据库 {db_name} 创建成功")
        return True
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False
    finally:
        cursor.close()

def create_env_file(host, port, user, password, database):
    """创建.env配置文件"""
    print("📝 创建.env配置文件...")
    
    env_content = f"""# MySQL数据库配置
MYSQL_HOST={host}
MYSQL_PORT={port}
MYSQL_USER={user}
MYSQL_PASSWORD={password}
MYSQL_DB={database}

# Flask配置
SECRET_KEY=your-secret-key-here-{os.urandom(16).hex()}
FLASK_ENV=production
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env文件创建成功")
        return True
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")
        return False

def test_app_connection():
    """测试应用连接"""
    print("🧪 测试应用数据库连接...")
    
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from app import app, db
        
        with app.app_context():
            # 创建表
            db.create_all()
            print("✅ 数据库表创建成功")
            
            # 测试查询
            from app import ProjectInfo, FundingArrangement, User
            project_count = ProjectInfo.query.count()
            funding_count = FundingArrangement.query.count()
            user_count = User.query.count()
            
            print(f"📊 数据统计:")
            print(f"   项目信息表: {project_count} 条记录")
            print(f"   资金安排表: {funding_count} 条记录")
            print(f"   用户表: {user_count} 条记录")
        
        return True
    except Exception as e:
        print(f"❌ 应用连接测试失败: {e}")
        return False

def interactive_setup():
    """交互式配置"""
    print("🚀 MySQL数据库配置向导")
    print("=" * 50)
    
    # 1. 检查MySQL安装
    mysql_path = check_mysql_installation()
    if not mysql_path:
        return False
    
    # 2. 检查MySQL服务状态
    if not check_mysql_running():
        print("⚠️ MySQL服务未运行，尝试启动...")
        if not start_mysql_service():
            print("❌ 无法启动MySQL服务")
            print("请手动启动MySQL服务后重试")
            return False
    else:
        print("✅ MySQL服务正在运行")
    
    # 3. 获取连接参数
    print("\n📋 请输入MySQL连接信息:")
    host = input("主机地址 (默认: localhost): ").strip() or "localhost"
    port = input("端口 (默认: 3306): ").strip() or "3306"
    user = input("用户名 (默认: root): ").strip() or "root"
    password = input("密码: ").strip()
    database = input("数据库名 (默认: ai_urban_system): ").strip() or "ai_urban_system"
    
    # 4. 测试连接
    connection = test_mysql_connection(host, int(port), user, password)
    if not connection:
        print("❌ 连接失败，请检查连接信息")
        return False
    
    # 5. 创建数据库
    if not create_database(connection, database):
        return False
    
    connection.close()
    
    # 6. 创建.env文件
    if not create_env_file(host, port, user, password, database):
        return False
    
    # 7. 测试应用连接
    if not test_app_connection():
        return False
    
    print("\n🎉 MySQL配置完成！")
    print("=" * 50)
    print("📋 配置信息:")
    print(f"   主机: {host}")
    print(f"   端口: {port}")
    print(f"   数据库: {database}")
    print(f"   用户: {user}")
    print("\n🚀 现在可以启动应用:")
    print("   python app.py")
    print("\n🌐 访问地址: http://localhost:8080")
    print("\n🔐 默认登录信息:")
    print("   用户名: admin")
    print("   密码: admin123")
    
    return True

def quick_setup():
    """快速配置（使用默认参数）"""
    print("🚀 MySQL快速配置")
    print("=" * 30)
    
    # 默认配置
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',  # 空密码
        'database': 'ai_urban_system'
    }
    
    try:
        # 1. 检查MySQL服务
        if not check_mysql_running():
            print("⚠️ MySQL服务未运行，请先启动MySQL服务")
            print("启动方法:")
            print("1. brew services start mysql")
            print("2. sudo /usr/local/mysql/support-files/mysql.server start")
            return False
        
        # 2. 测试连接
        connection = test_mysql_connection(**config)
        if not connection:
            print("❌ 连接失败，请检查MySQL服务状态")
            return False
        
        # 3. 创建数据库
        if not create_database(connection, config['database']):
            return False
        
        connection.close()
        
        # 4. 创建.env文件
        if not create_env_file(**config):
            return False
        
        # 5. 测试应用连接
        if not test_app_connection():
            return False
        
        print("\n🎉 快速配置完成！")
        print("📋 配置信息:")
        print(f"   主机: {config['host']}")
        print(f"   端口: {config['port']}")
        print(f"   数据库: {config['database']}")
        print(f"   用户: {config['user']}")
        print(f"   密码: (空)")
        
        return True
        
    except Exception as e:
        print(f"❌ 快速配置失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 MySQL数据库配置工具")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        # 快速配置模式
        success = quick_setup()
    else:
        # 交互式配置模式
        success = interactive_setup()
    
    if success:
        print("\n✅ 配置成功！")
        sys.exit(0)
    else:
        print("\n❌ 配置失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
