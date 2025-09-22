# MySQL完整配置指南

## 📋 系统要求

- macOS 10.14+ 或 Linux
- Python 3.7+
- MySQL 5.7+ 或 MySQL 8.0+

## 🚀 安装MySQL

### 方法1: 使用Homebrew（推荐）

```bash
# 安装Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装MySQL
brew install mysql

# 启动MySQL服务
brew services start mysql

# 设置开机自启
brew services enable mysql
```

### 方法2: 从官网下载

1. 访问 [MySQL官网](https://dev.mysql.com/downloads/mysql/)
2. 下载适合macOS的安装包
3. 运行安装程序
4. 按照向导完成安装

### 方法3: 使用包管理器

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

## 🔧 配置MySQL

### 1. 启动MySQL服务

```bash
# macOS (Homebrew)
brew services start mysql

# macOS (官方安装)
sudo /usr/local/mysql/support-files/mysql.server start

# Linux
sudo systemctl start mysql
# 或
sudo service mysql start
```

### 2. 设置root密码

```bash
# 连接MySQL
mysql -u root

# 设置密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
EXIT;
```

### 3. 创建数据库

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

## 📝 配置应用

### 1. 创建.env文件

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

### 2. 安装Python依赖

```bash
pip install pymysql
```

### 3. 测试连接

```bash
python mysql_config.py --quick
```

## 🔍 验证配置

### 检查MySQL状态

```bash
# 检查进程
ps aux | grep mysql

# 检查端口
lsof -i :3306

# 测试连接
mysql -u root -p -e "SHOW DATABASES;"
```

### 启动应用

```bash
python app.py
```

查看控制台输出：
- ✅ **MySQL成功**: `成功连接MySQL数据库: localhost:3306/ai_urban_system`
- ⚠️ **回退SQLite**: `MySQL连接失败，回退到SQLite: [错误信息]`

## 🛠️ 故障排除

### 问题1: MySQL服务未启动

**症状**: `Can't connect to MySQL server`

**解决方案**:
```bash
# 检查服务状态
brew services list | grep mysql

# 启动服务
brew services start mysql

# 或使用系统服务
sudo /usr/local/mysql/support-files/mysql.server start
```

### 问题2: 权限被拒绝

**症状**: `Access denied for user`

**解决方案**:
```sql
-- 重置root密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;

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

### MySQL配置优化

编辑MySQL配置文件（通常在`/usr/local/mysql/my.cnf`或`/etc/mysql/my.cnf`）：

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

### 应用配置优化

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

### 常用命令

```bash
# 启动MySQL
brew services start mysql

# 停止MySQL
brew services stop mysql

# 重启MySQL
brew services restart mysql

# 查看MySQL状态
brew services list | grep mysql

# 连接MySQL
mysql -u root -p

# 查看数据库
SHOW DATABASES;

# 使用数据库
USE ai_urban_system;

# 查看表
SHOW TABLES;
```

## 🎯 下一步

配置完成后，您可以：

1. 启动应用：`python app.py`
2. 访问系统：http://localhost:8080
3. 使用默认账号登录：
   - 用户名：admin
   - 密码：admin123
4. 开始使用AI城建系统
