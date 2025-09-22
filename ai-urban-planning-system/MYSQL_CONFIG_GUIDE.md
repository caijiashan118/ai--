# MySQL数据库配置指南

## 🚀 快速配置

### 方法1: 使用自动配置脚本（推荐）

```bash
# 交互式配置
python mysql_config.py

# 快速配置（使用默认参数）
python mysql_config.py --quick
```

### 方法2: 手动配置

#### 1. 安装MySQL

**macOS:**
```bash
# 使用Homebrew安装
brew install mysql

# 启动MySQL服务
brew services start mysql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

**CentOS/RHEL:**
```bash
sudo yum install mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

#### 2. 创建数据库

```bash
# 连接MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE ai_urban_system 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

# 创建用户（可选）
CREATE USER 'ai_urban_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ai_urban_system.* TO 'ai_urban_user'@'localhost';
FLUSH PRIVILEGES;

# 退出
EXIT;
```

#### 3. 创建.env配置文件

在项目根目录创建`.env`文件：

```env
# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=ai_urban_system

# Flask配置
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

#### 4. 启动应用

```bash
python app.py
```

## 🔍 验证配置

### 检查MySQL服务状态

```bash
# 检查进程
ps aux | grep mysql

# 检查端口
lsof -i :3306

# 测试连接
mysql -u root -p -e "SHOW DATABASES;"
```

### 检查应用连接

启动应用后，查看控制台输出：

- ✅ **MySQL成功**: `成功连接MySQL数据库: localhost:3306/ai_urban_system`
- ⚠️ **回退SQLite**: `MySQL连接失败，回退到SQLite: [错误信息]`

## 🛠️ 故障排除

### 问题1: MySQL服务未启动

**症状**: `Can't connect to MySQL server`

**解决方案**:
```bash
# macOS
brew services start mysql
# 或
sudo /usr/local/mysql/support-files/mysql.server start

# Ubuntu/Debian
sudo systemctl start mysql

# CentOS/RHEL
sudo systemctl start mysqld
```

### 问题2: 权限被拒绝

**症状**: `Access denied for user`

**解决方案**:
```sql
-- 重置root密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';

-- 或创建新用户
CREATE USER 'ai_urban_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON ai_urban_system.* TO 'ai_urban_user'@'localhost';
FLUSH PRIVILEGES;
```

### 问题3: 数据库不存在

**症状**: `Unknown database`

**解决方案**:
```sql
CREATE DATABASE ai_urban_system 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;
```

### 问题4: 字符集问题

**症状**: `Incorrect string value`

**解决方案**:
```sql
ALTER DATABASE ai_urban_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 📊 性能优化

### MySQL配置建议

在MySQL配置文件（my.cnf）中添加：

```ini
[mysqld]
# 字符集设置
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci

# 连接池设置
max_connections=200
max_connect_errors=1000

# 缓存设置
innodb_buffer_pool_size=256M
query_cache_size=32M
query_cache_type=1

# 日志设置
slow_query_log=1
slow_query_log_file=/var/log/mysql/slow.log
long_query_time=2
```

### 应用配置

在.env文件中添加：

```env
# 数据库连接池配置
SQLALCHEMY_ENGINE_OPTIONS={"pool_size": 10, "pool_timeout": 20, "pool_recycle": -1, "max_overflow": 0}
```

## 🔒 安全建议

1. **使用专用用户**: 不要使用root用户运行应用
2. **限制权限**: 只授予必要的数据库权限
3. **网络安全**: 使用防火墙限制数据库访问
4. **定期备份**: 设置自动备份策略
5. **密码安全**: 使用强密码并定期更换

## 📞 技术支持

如果遇到问题，请检查：

1. MySQL服务状态
2. 网络连接
3. 用户权限
4. 防火墙设置
5. 应用日志

更多帮助请参考：
- [MySQL官方文档](https://dev.mysql.com/doc/)
- [PyMySQL文档](https://pymysql.readthedocs.io/)
- [Flask-SQLAlchemy文档](https://flask-sqlalchemy.palletsprojects.com/)
