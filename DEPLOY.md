# 城市建设项目管理系统 - 部署说明

## 系统要求
- Python 3.8+
- pip (Python包管理器)
- MySQL 5.7+ 或 MariaDB 10.3+ (推荐)
- 或者 SQLite (备用选项)

## 数据库部署选项

### 选项1: MySQL部署 (推荐)

1. **安装MySQL**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install mysql-server
   
   # CentOS/RHEL
   sudo yum install mysql-server
   
   # macOS
   brew install mysql
   ```

2. **创建数据库**
   ```bash
   mysql -u root -p < mysql_setup.sql
   ```

3. **配置数据库连接**
   ```bash
   # 复制配置文件模板
   cp .env.example .env
   
   # 编辑.env文件，设置你的MySQL连接信息
   nano .env
   ```

### 选项2: SQLite部署 (简单)

如果不想使用MySQL，系统会自动回退到SQLite，无需额外配置。

## 快速部署

1. **解压项目文件**
   ```bash
   # 解压下载的压缩文件到目标目录
   tar -xzf ai-urban-planning-system.tar.gz
   cd python-ai-urban-system
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置数据库 (MySQL)**
   ```bash
   # 设置环境变量 (可选，也可使用.env文件)
   export MYSQL_HOST=localhost
   export MYSQL_PORT=3306
   export MYSQL_USER=root
   export MYSQL_PASSWORD=your_password
   export MYSQL_DB=ai_urban_system
   ```

4. **启动应用**
   ```bash
   python app.py
   ```

5. **访问系统**
   - 打开浏览器访问: http://localhost:3000
   - 首次启动会自动创建数据表
   - 可通过数据导入功能添加实际数据

## 功能说明

### 主要功能
- 项目基本信息管理 (新增概算编码字段)
- 资金安排管理
- Excel导入导出
- 智能图表分析
- 数据透视表

### 新增功能
- **概算编码字段**: 支持项目概算编码管理
- **MySQL支持**: 企业级数据库支持，更好的并发性能
- **自动回退**: MySQL连接失败时自动使用SQLite

### 支持的操作
- 新增、编辑、删除项目和资金安排
- 批量Excel数据导入导出
- 多维度数据筛选和分析
- 交互式图表展示

## 数据库结构

### 项目基本信息表 (project_info)
- 新增字段: `budget_code` (概算编码)
- 金额字段改为 DECIMAL(15,2) 类型
- 支持负数金额输入

### 技术改进
- 数据库: SQLite → MySQL (支持自动回退)
- 金额字段: Float → DECIMAL (更精确)
- 字段扩展: 增加概算编码字段

## 注意事项
- 确保Python版本为3.8或更高
- MySQL部署需要先创建数据库和用户
- SQLite模式下数据存储在 `ai_urban_system.db` 文件中
- 首次运行前请确保已安装所有依赖包
- 系统运行在3000端口，请确保该端口未被占用

## 环境变量配置

创建 `.env` 文件进行配置:
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=ai_urban_system
```

## 故障排除

1. **MySQL连接失败**
   - 检查MySQL服务是否启动
   - 验证用户名密码是否正确
   - 确认数据库是否已创建
   - 系统会自动回退到SQLite模式

2. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

3. **端口占用问题**
   ```bash
   # 查看端口占用
   lsof -i :3000
   
   # 或者修改app.py中的端口号
   app.run(host='0.0.0.0', port=8080, debug=True)
   ```