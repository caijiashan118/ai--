# AI城建系统部署指南

## 系统要求

- Python 3.7 或更高版本
- 操作系统：Windows、macOS、Linux

## 快速部署

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：http://localhost:8080

## 功能模块

### 基础数据模块 (http://localhost:8080/basic_data)
- 项目总表：汇总所有项目信息
- 项目基本信息表：管理项目基础数据
- 项目资金安排表：管理资金分配信息
- 数据筛选：支持多条件筛选
- 字段选择器：自定义显示字段
- 数据导出：支持Excel导出

### 智能图表模块 (http://localhost:8080/smart_charts)
- 实时数据监控
- 项目进度分析
- 资金执行情况
- 风险预警系统

## 数据库配置

系统默认使用SQLite数据库，无需额外配置。数据库文件会自动创建在 `instance/` 目录下。

如需使用MySQL，请修改 `app.py` 中的数据库连接配置。

## 端口配置

默认端口：8080

如需修改端口，请编辑 `app.py` 文件中的 `app.run()` 部分。

## 数据同步

系统包含数据同步功能，可以：
1. 将现有数据同步到项目总表
2. 确保数据一致性
3. 自动同步数据

## 故障排除

### 常见问题

1. **端口被占用**
   - 修改 `app.py` 中的端口号
   - 或停止占用端口的其他程序

2. **数据库连接失败**
   - 检查数据库文件权限
   - 确保 `instance/` 目录存在

3. **依赖安装失败**
   - 使用 `pip install --upgrade pip` 升级pip
   - 使用 `pip install -r requirements.txt --force-reinstall` 重新安装

### 日志查看

应用运行时会在控制台显示详细日志，包括：
- 请求处理时间
- 数据库操作
- 错误信息

## 生产环境部署

### 使用Gunicorn（推荐）

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 备份与恢复

### 数据备份
```bash
# 备份数据库
cp instance/ai_urban_system.db backup/ai_urban_system_$(date +%Y%m%d).db
```

### 数据恢复
```bash
# 恢复数据库
cp backup/ai_urban_system_20231201.db instance/ai_urban_system.db
```

## 技术支持

如遇到问题，请检查：
1. Python版本是否符合要求
2. 所有依赖是否正确安装
3. 端口是否被占用
4. 数据库文件权限是否正确

## 更新日志

- v1.0.0: 初始版本，包含基础数据管理和智能图表功能
- 支持项目信息管理
- 支持资金安排管理
- 支持数据筛选和导出
- 支持字段选择器
- 支持数据一致性检查
