# 登录问题解决指南

## 🔐 默认登录信息

**用户名**: `admin`  
**密码**: `admin123`

## 🚨 常见登录问题

### 问题1: 用户名或密码错误

**症状**: 输入admin/admin123后提示"用户名或密码错误"

**解决方案**:
1. 确认用户名是 `admin`（全小写）
2. 确认密码是 `admin123`（全小写，无空格）
3. 检查是否开启了Caps Lock
4. 尝试刷新页面重新登录

### 问题2: 忘记密码

**解决方案**:
```bash
# 使用密码重置脚本
python reset_admin_password.py

# 或检查当前密码状态
python reset_admin_password.py --check
```

### 问题3: 用户不存在

**症状**: 提示"用户不存在"

**解决方案**:
```bash
# 重新初始化认证数据
python -c "
from app import app, db
with app.app_context():
    from app import init_auth_data
    init_auth_data()
    print('认证数据初始化完成')
"
```

### 问题4: 数据库连接问题

**症状**: 登录页面无法加载或出现数据库错误

**解决方案**:
1. 检查应用是否正在运行
2. 重启应用: `python app.py`
3. 检查数据库文件是否存在: `ls instance/`

## 🔧 密码管理

### 重置admin密码

```bash
# 交互式重置密码
python reset_admin_password.py

# 检查当前密码状态
python reset_admin_password.py --check
```

### 创建新用户

1. 使用admin账号登录系统
2. 访问用户管理页面
3. 点击"新增用户"按钮
4. 填写用户信息并保存

## 🛠️ 系统维护

### 检查用户数据

```bash
python -c "
from app import app, db, User
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f'{user.username} - {user.real_name} - {\"激活\" if user.is_active else \"未激活\"}')
"
```

### 重置所有认证数据

```bash
python -c "
from app import app, db, User, Role, Permission
with app.app_context():
    # 删除所有用户数据
    User.query.delete()
    Role.query.delete()
    Permission.query.delete()
    db.session.commit()
    
    # 重新初始化
    from app import init_auth_data
    init_auth_data()
    print('认证数据已重置')
"
```

## 📞 技术支持

如果以上方法都无法解决问题，请检查：

1. **应用日志**: 查看控制台输出的错误信息
2. **数据库状态**: 确认数据库文件完整
3. **网络连接**: 确认可以访问localhost:8080
4. **浏览器缓存**: 尝试清除浏览器缓存

## 🎯 快速解决步骤

1. **确认登录信息**:
   - 用户名: `admin`
   - 密码: `admin123`

2. **刷新页面**: 按F5或Ctrl+R刷新登录页面

3. **检查应用状态**: 确认应用正在运行

4. **重置密码**（如需要）:
   ```bash
   python reset_admin_password.py
   ```

5. **重新初始化**（最后手段）:
   ```bash
   python -c "
   from app import app, db
   with app.app_context():
       from app import init_auth_data
       init_auth_data()
   "
   ```

## ✅ 验证登录成功

登录成功后，您应该能够：
- 看到系统首页
- 访问基础数据管理
- 使用智能图表分析
- 管理用户和权限

如果登录后无法看到这些功能，请检查用户权限设置。
