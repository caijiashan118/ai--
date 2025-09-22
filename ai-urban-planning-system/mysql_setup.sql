-- MySQL数据库初始化脚本
-- AI城市规划系统数据库设置

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS ai_urban_system 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

-- 2. 使用数据库
USE ai_urban_system;

-- 3. 创建用户（可选，建议为系统创建专用用户）
-- CREATE USER 'ai_urban_user'@'localhost' IDENTIFIED BY 'your_password_here';
-- GRANT ALL PRIVILEGES ON ai_urban_system.* TO 'ai_urban_user'@'localhost';
-- FLUSH PRIVILEGES;

-- 4. 设置时区（可选）
SET time_zone = '+08:00';

-- 注意：数据表将由Flask-SQLAlchemy自动创建
-- 当应用首次运行时，会自动创建以下表：
-- - project_info (项目基本信息表)
-- - funding_arrangement (项目资金安排表)
-- - system_log (系统操作日志表，如果启用)

-- 数据表结构预览：
/*
项目基本信息表 (project_info):
- id: 主键，自增
- project_name: 项目名称 VARCHAR(200)
- project_code: 项目编码 VARCHAR(50) UNIQUE
- budget_code: 概算编码 VARCHAR(50) [新增字段]
- region: 所属区域 VARCHAR(100)
- investment_mode: 投资模式 VARCHAR(50)
- project_type: 项目类型 VARCHAR(50)
- construction_unit: 建设单位 VARCHAR(200)
- supervisor_dept: 项目主管部门 VARCHAR(200)
- approval_date: 立项时间 DATE
- budget_amount: 概算批复金额 DECIMAL(15,2)
- contract_amount: 签订合同金额 DECIMAL(15,2)
- start_date: 开工时间 DATE
- end_date: 完工时间 DATE
- project_status: 项目状态 VARCHAR(50)
- created_at: 创建时间 DATETIME
- updated_at: 更新时间 DATETIME

项目资金安排表 (funding_arrangement):
- id: 主键，自增
- project_name: 项目名称 VARCHAR(200)
- project_code: 项目编码 VARCHAR(50)
- construction_unit: 建设单位 VARCHAR(200)
- supervisor_dept: 项目主管部门 VARCHAR(200)
- arrangement_amount: 安排金额 DECIMAL(15,2)
- funding_source: 资金来源 VARCHAR(100)
- funding_nature: 资金性质 VARCHAR(50)
- budget_doc_no: 财预文号 VARCHAR(100)
- handler: 经办人 VARCHAR(50)
- handling_office: 经办处室 VARCHAR(100)
- arrangement_year: 安排年度 INT
- superior_doc_no: 上级资金文号 VARCHAR(100)
- remarks: 备注 TEXT
- created_at: 创建时间 DATETIME
- updated_at: 更新时间 DATETIME
*/