# AI城建系统 v1.0.0

## 项目简介

AI城建系统是一个智能城市建设项目管理平台，提供项目信息管理、资金安排跟踪、数据分析可视化等核心功能。

## 主要功能

### 1. 基础数据管理模块
- **项目基本信息管理**：支持项目的增删改查、批量导入导出
- **资金安排管理**：跟踪项目资金安排和使用情况
- **项目总表**：汇总展示所有项目的关键信息

### 2. 智能图表分析模块
- **多维度图表**：项目状态、区域分布、投资模式等可视化分析
- **数据透视表**：支持拖拽字段进行多维度数据透视
- **趋势分析**：项目投资趋势、资金执行情况分析

### 3. 智慧管理模块
- **Excel文件管理**：支持Excel文件的上传、解析和在线编辑
- **数据同步**：实时同步各模块间的数据

### 4. 用户权限管理模块
- **用户管理**：用户注册、登录、权限控制
- **角色管理**：基于角色的访问控制
- **审计日志**：操作记录和审计跟踪

## 技术栈

- **后端**：Python Flask + SQLAlchemy
- **前端**：Bootstrap + DataTables + Plotly.js
- **数据库**：SQLite (支持MySQL)
- **数据处理**：Pandas + OpenPyXL

## 快速开始

### 环境要求
- Python 3.8+
- pip

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/jiashancai/ai-项目.git
cd ai-项目
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 初始化数据库
```bash
python3 app.py
```

4. 访问系统
打开浏览器访问：http://localhost:8080

### 数据初始化

生成模拟数据：
```bash
python3 generate_mock_data.py
python3 import_mock_data.py
```

## 功能特色

- ✅ 完整的项目生命周期管理
- ✅ 多维度数据分析和可视化
- ✅ Excel文件导入导出
- ✅ 响应式设计，支持移动端
- ✅ 数据透视表和图表交互
- ✅ 用户权限管理
- ✅ 实时数据同步

## 系统截图

### 基础数据管理
- 项目信息表格展示
- 资金安排跟踪
- 项目总表汇总

### 智能图表分析
- 多维度图表展示
- 数据透视表
- 趋势分析

## 开发说明

### 项目结构
```
ai-项目/
├── app.py                 # 主应用文件
├── requirements.txt       # 依赖包列表
├── templates/            # HTML模板
├── static/              # 静态资源
├── generate_mock_data.py # 模拟数据生成
└── import_mock_data.py   # 数据导入脚本
```

### API接口
- `/api/project_info` - 项目信息管理
- `/api/funding_arrangement` - 资金安排管理
- `/api/charts_data` - 图表数据
- `/api/pivot_table` - 透视表数据

## 更新日志

### v1.0.0 (2025-09-20)
- 初始版本发布
- 完成基础数据管理功能
- 实现智能图表分析
- 添加Excel导入导出功能
- 完善用户权限管理

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 许可证

MIT License

## 联系方式

如有问题，请通过GitHub Issues联系。