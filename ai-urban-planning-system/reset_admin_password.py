#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重置管理员密码脚本
用于重置admin用户的密码
"""

import sys
import os
import getpass

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, hash_password, verify_password

def reset_admin_password():
    """重置admin用户密码"""
    print("🔧 重置管理员密码工具")
    print("=" * 40)
    
    with app.app_context():
        # 查找admin用户
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            print("❌ 未找到admin用户")
            return False
        
        print(f"👤 找到admin用户: {admin_user.real_name}")
        print(f"   当前邮箱: {admin_user.email}")
        
        # 获取新密码
        while True:
            new_password = getpass.getpass("请输入新密码: ")
            if not new_password:
                print("❌ 密码不能为空")
                continue
            
            confirm_password = getpass.getpass("请确认新密码: ")
            if new_password != confirm_password:
                print("❌ 两次输入的密码不一致")
                continue
            
            if len(new_password) < 6:
                print("❌ 密码长度至少6位")
                continue
            
            break
        
        # 更新密码
        try:
            admin_user.password_hash = hash_password(new_password)
            db.session.commit()
            
            # 验证新密码
            is_valid = verify_password(new_password, admin_user.password_hash)
            
            if is_valid:
                print("✅ 密码重置成功！")
                print(f"   用户名: admin")
                print(f"   新密码: {new_password}")
                return True
            else:
                print("❌ 密码验证失败")
                return False
                
        except Exception as e:
            print(f"❌ 密码重置失败: {e}")
            db.session.rollback()
            return False

def show_current_password():
    """显示当前密码信息（用于测试）"""
    print("🔍 检查当前密码状态")
    print("=" * 30)
    
    with app.app_context():
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            print("❌ 未找到admin用户")
            return
        
        print(f"👤 admin用户信息:")
        print(f"   用户名: {admin_user.username}")
        print(f"   邮箱: {admin_user.email}")
        print(f"   真实姓名: {admin_user.real_name}")
        print(f"   状态: {'激活' if admin_user.is_active else '未激活'}")
        print(f"   密码哈希: {admin_user.password_hash[:20]}...")
        
        # 测试常见密码
        common_passwords = ['admin123', 'changeme', 'admin', 'password', '123456']
        print(f"\\n🔍 测试常见密码:")
        
        for pwd in common_passwords:
            is_valid = verify_password(pwd, admin_user.password_hash)
            status = "✅ 正确" if is_valid else "❌ 错误"
            print(f"   {pwd}: {status}")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        show_current_password()
    else:
        success = reset_admin_password()
        if success:
            print("\\n🎉 密码重置完成！")
            print("现在可以使用新密码登录系统")
        else:
            print("\\n❌ 密码重置失败！")
            sys.exit(1)

if __name__ == "__main__":
    main()
