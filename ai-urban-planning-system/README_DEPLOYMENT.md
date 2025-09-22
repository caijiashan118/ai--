# AI城建系统 - 本地部署指南

## 🚀 快速启动

### 方法1: 使用启动脚本（推荐）
```bash
cd /path/to/ai-urban-planning-system
./start.sh
```

### 方法2: 手动启动
```bash
cd /path/to/ai-urban-planning-system
python3 app.py
```

## 📋 系统要求

- Python 3.9+
- 依赖包（见 requirements.txt）

## 🌐 访问地址

- **主页**: http://localhost:8080
- **基础数据管理**: http://localhost:8080/basic_data
- **智能图表分析**: http://localhost:8080/smart_charts

## 📊 功能模块

### 1. 基础数据管理
- 项目基本信息管理
- 资金安排管理
- 项目总表查看
- 数据导入导出

### 2. 智能图表分析
- 数据可视化
- 图表生成
- 数据分析

## 🔧 故障排除

### 端口被占用
```bash
# 清理端口8080
lsof -ti:8080 | xargs kill -9
```

### 依赖问题
```bash
# 重新安装依赖
pip3 install -r requirements.txt
```

### 数据库问题
- 系统使用SQLite数据库，位于 `instance/ai_urban_system.db`
- 如果数据库损坏，删除该文件即可重新创建

## 📝 注意事项

1. 首次运行会自动创建数据库和表结构
2. 系统支持数据导入功能
3. 所有数据存储在本地SQLite数据库中
4. 支持Excel文件的导入导出功能

## 🛑 停止服务

在终端中按 `Ctrl+C` 停止服务


