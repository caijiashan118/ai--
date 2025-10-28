#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统启动脚本
优化版本，确保稳定运行
"""

import os
import sys
import time
from app import app, db

def start_server():
    """启动服务器"""
    print("=" * 60)
    print("🚀 AI城建系统启动中...")
    print("=" * 60)
    
    # 初始化数据库
    with app.app_context():
        try:
            db.create_all()
            print("✅ 数据库初始化完成")
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            return False
    
    # 服务器配置信息
    print("\n📡 服务器配置:")
    print("   - 主机: 0.0.0.0 (监听所有网络接口)")
    print("   - 端口: 5000")
    print("   - 模式: 生产模式 (debug=False)")
    print("   - 线程: 启用多线程支持")
    
    print("\n🌐 访问地址:")
    print("   - 主要地址: http://localhost:5000")
    print("   - 备用地址: http://127.0.0.1:5000")
    
    print("\n📊 系统功能:")
    print("   - 基础数据管理: http://localhost:5000/basic_data")
    print("   - 智能图表分析: http://localhost:5000/smart_charts")
    
    print("\n" + "=" * 60)
    print("✅ 系统启动完成！请在浏览器中访问上述地址")
    print("=" * 60)
    
    try:
        # 启动Flask应用
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")
        return False
    
    return True

if __name__ == '__main__':
    start_server()