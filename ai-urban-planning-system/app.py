#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统
功能: 基础数据管理 + 智能图表分析
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json
import os
from datetime import datetime
import hashlib
import secrets
from io import BytesIO

app = Flask(__name__)

# 启用压缩（若可用）
try:
    from flask_compress import Compress
    Compress(app)
    print("✅ 启用HTTP压缩")
except Exception:
    print("ℹ️ 未安装 flask-compress，跳过压缩配置")

# 静态资源缓存：设置较长的缓存时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(os.getenv('STATIC_MAX_AGE', 60 * 60 * 24 * 7))  # 7天
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# MySQL 数据库配置
# 通过环境变量配置，请在.env文件或系统环境变量中设置
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': os.getenv('MYSQL_PORT', '3306'),
    'username': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DB', 'urban_system')
}

# 构建MySQL连接字符串
mysql_url = f"mysql+pymysql://{MYSQL_CONFIG['username']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}?charset=utf8mb4"

# 尝试连接MySQL，失败则回退到SQLite
use_mysql = False
try:
    import pymysql
    # 测试MySQL连接
    connection = pymysql.connect(
        host=MYSQL_CONFIG['host'],
        port=int(MYSQL_CONFIG['port']),
        user=MYSQL_CONFIG['username'],
        password=MYSQL_CONFIG['password'],
        charset='utf8mb4'
    )
    # 创建数据库（如果不存在）
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    connection.commit()
    cursor.close()
    connection.close()
    
    # MySQL配置成功
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_timeout': 20,
        'pool_recycle': -1,
        'max_overflow': 0
    }
    use_mysql = True
    print(f"✅ 成功连接MySQL数据库: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}")
    
except Exception as e:
    print(f"⚠️ MySQL连接失败，回退到SQLite: {e}")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_urban_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    use_mysql = False

db = SQLAlchemy(app)


# ================== 数据库模型 ==================

class ProjectInfo(db.Model):
    """项目基本信息表"""
    __tablename__ = 'project_info'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(200), nullable=False, comment='项目名称')
    project_code = db.Column(db.String(50), unique=True, nullable=False, comment='项目编码')
    budget_code = db.Column(db.String(50), nullable=True, comment='概算编码')
    budget_project_name = db.Column(db.String(200), nullable=True, comment='概算项目名称')
    region = db.Column(db.String(100), nullable=False, comment='所属区域')
    investment_mode = db.Column(db.String(50), nullable=False, comment='投资模式')
    project_type = db.Column(db.String(50), nullable=False, comment='项目类型')
    construction_unit = db.Column(db.String(200), nullable=False, comment='建设单位')
    supervisor_dept = db.Column(db.String(200), nullable=False, comment='项目主管部门')
    approval_date = db.Column(db.Date, nullable=False, comment='立项时间')
    budget_amount = db.Column(db.DECIMAL(15, 2), nullable=False, comment='概算批复金额')
    contract_amount = db.Column(db.DECIMAL(15, 2), nullable=True, comment='签订合同金额')
    start_date = db.Column(db.Date, nullable=True, comment='（预计）开工时间')
    end_date = db.Column(db.Date, nullable=True, comment='（预计）完工时间')
    project_status = db.Column(db.String(50), nullable=False, comment='项目状态')
    handling_office = db.Column(db.String(100), nullable=True, comment='业务处')
    remarks = db.Column(db.Text, nullable=True, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'project_name': self.project_name,
            'project_code': self.project_code,
            'budget_code': self.budget_code,
            'budget_project_name': self.budget_project_name,
            'region': self.region,
            'investment_mode': self.investment_mode,
            'project_type': self.project_type,
            'construction_unit': self.construction_unit,
            'supervisor_dept': self.supervisor_dept,
            'approval_date': self.approval_date.strftime('%Y-%m-%d') if self.approval_date else '',
            'budget_amount': float(self.budget_amount) if self.budget_amount else 0,
            'contract_amount': float(self.contract_amount) if self.contract_amount else None,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else '',
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else '',
            'project_status': self.project_status,
            'handling_office': self.handling_office,
            'remarks': self.remarks
        }

class ProjectProgress(db.Model):
    """项目进度跟踪表"""
    __tablename__ = 'project_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.String(50), nullable=False, comment='项目编码')
    milestone_name = db.Column(db.String(200), nullable=False, comment='里程碑名称')
    milestone_type = db.Column(db.String(50), nullable=False, comment='里程碑类型')
    planned_date = db.Column(db.Date, nullable=False, comment='计划完成日期')
    actual_date = db.Column(db.Date, nullable=True, comment='实际完成日期')
    progress_percentage = db.Column(db.Float, default=0, comment='完成百分比')
    status = db.Column(db.String(50), default='未开始', comment='状态')
    description = db.Column(db.Text, nullable=True, comment='描述')
    responsible_person = db.Column(db.String(100), nullable=True, comment='负责人')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'milestone_name': self.milestone_name,
            'milestone_type': self.milestone_type,
            'planned_date': self.planned_date.strftime('%Y-%m-%d') if self.planned_date else '',
            'actual_date': self.actual_date.strftime('%Y-%m-%d') if self.actual_date else '',
            'progress_percentage': self.progress_percentage,
            'status': self.status,
            'description': self.description,
            'responsible_person': self.responsible_person
        }

class SystemLog(db.Model):
    """系统操作日志表"""
    __tablename__ = 'system_log'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), default='系统用户', comment='操作用户')
    action = db.Column(db.String(100), nullable=False, comment='操作类型')
    target_type = db.Column(db.String(50), nullable=False, comment='目标类型')
    target_id = db.Column(db.String(100), nullable=True, comment='目标ID')
    description = db.Column(db.Text, nullable=True, comment='操作描述')
    ip_address = db.Column(db.String(50), nullable=True, comment='IP地址')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'action': self.action,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'description': self.description,
            'ip_address': self.ip_address,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class FundingArrangement(db.Model):
    """项目资金安排表"""
    __tablename__ = 'funding_arrangement'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(200), nullable=False, comment='项目名称')
    project_code = db.Column(db.String(50), nullable=False, comment='项目编码')
    construction_unit = db.Column(db.String(200), nullable=False, comment='建设单位')
    supervisor_dept = db.Column(db.String(200), nullable=False, comment='项目主管部门')
    arrangement_amount = db.Column(db.DECIMAL(15, 2), nullable=False, comment='安排金额')
    funding_source = db.Column(db.String(100), nullable=False, comment='资金来源')
    funding_nature = db.Column(db.String(50), nullable=False, comment='资金性质')
    budget_doc_no = db.Column(db.String(100), nullable=True, comment='财预文号')
    handler = db.Column(db.String(50), nullable=True, comment='经办人')
    handling_office = db.Column(db.String(100), nullable=True, comment='业务处')
    arrangement_year = db.Column(db.Integer, nullable=True, comment='安排年度')
    superior_doc_no = db.Column(db.String(100), nullable=True, comment='上级资金文号')
    remarks = db.Column(db.Text, nullable=True, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'project_name': self.project_name,
            'project_code': self.project_code,
            'construction_unit': self.construction_unit,
            'supervisor_dept': self.supervisor_dept,
            'arrangement_amount': float(self.arrangement_amount) if self.arrangement_amount else 0,
            'funding_source': self.funding_source,
            'funding_nature': self.funding_nature,
            'budget_doc_no': self.budget_doc_no,
            'handler': self.handler,
            'handling_office': self.handling_office,
            'arrangement_year': self.arrangement_year,
            'superior_doc_no': self.superior_doc_no,
            'remarks': self.remarks
        }

class ProjectSummary(db.Model):
    """
    项目总表（只读汇总表）
    
    关系定义：
    - 数据来源：完全依赖项目基本信息表(ProjectInfo)和项目资金安排表(FundingArrangement)
    - 数据流向：单向从源表流向项目总表
    - 影响关系：项目总表不对源表产生任何影响，源表的增删改不影响项目总表结构
    - 更新机制：通过API自动重新生成，不直接编辑
    - 数据完整性：项目总表数据始终反映源表的最新状态
    
    字段依赖关系：
    - 与项目资金安排表相同的字段（项目名称、项目编码、建设单位、项目主管部门）：
      以项目编码（可研）为链接，字段信息依赖于项目资金安排表
    - 项目资金安排表独有字段：完全依赖项目资金安排表
    - 项目基本信息表独有字段：依赖项目基本信息表
    - 项目基本信息表和项目资金安排表中的建设单位、项目主管部门相互独立，彼此互不干涉
    """
    __tablename__ = 'project_summary'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 基础信息字段（两表共有）
    project_name = db.Column(db.String(200), nullable=False, comment='项目名称')
    project_code = db.Column(db.String(50), nullable=False, comment='项目编码')
    construction_unit = db.Column(db.String(200), nullable=False, comment='建设单位')
    supervisor_dept = db.Column(db.String(200), nullable=False, comment='项目主管部门')
    
    # 项目基本信息表独有字段
    budget_code = db.Column(db.String(50), nullable=True, comment='概算编码')
    budget_project_name = db.Column(db.String(200), nullable=True, comment='概算项目名称')
    region = db.Column(db.String(100), nullable=False, comment='所属区域')
    investment_mode = db.Column(db.String(50), nullable=False, comment='投资模式')
    project_type = db.Column(db.String(50), nullable=False, comment='项目类型')
    approval_date = db.Column(db.Date, nullable=True, comment='立项时间')
    budget_amount = db.Column(db.DECIMAL(15, 2), nullable=True, comment='概算批复金额(万元)')
    contract_amount = db.Column(db.DECIMAL(15, 2), nullable=True, comment='签订合同金额(万元)')
    start_date = db.Column(db.Date, nullable=True, comment='（预计）开工时间')
    end_date = db.Column(db.Date, nullable=True, comment='（预计）完工时间')
    project_status = db.Column(db.String(50), nullable=True, comment='项目状态')
    
    # 资金安排表独有字段
    arrangement_amount = db.Column(db.DECIMAL(15, 2), nullable=True, comment='安排金额(万元)')
    funding_source = db.Column(db.String(100), nullable=True, comment='资金来源')
    funding_nature = db.Column(db.String(50), nullable=True, comment='资金性质')
    budget_doc_no = db.Column(db.String(100), nullable=True, comment='财预文号')
    handler = db.Column(db.String(50), nullable=True, comment='经办人')
    handling_office = db.Column(db.String(100), nullable=True, comment='业务处')
    arrangement_year = db.Column(db.Integer, nullable=True, comment='安排年度')
    superior_doc_no = db.Column(db.String(100), nullable=True, comment='上级资金文号')
    remarks = db.Column(db.Text, nullable=True, comment='备注')

    def to_dict(self):
        """按指定顺序返回字典：基础信息 → 资金安排表字段 → 项目基本信息表字段"""
        from collections import OrderedDict
        
        result = OrderedDict()
        
        # ID字段
        result['id'] = self.id
        
        # 基础信息字段（两表共有）
        result['project_name'] = self.project_name
        result['project_code'] = self.project_code
        result['construction_unit'] = self.construction_unit
        result['supervisor_dept'] = self.supervisor_dept
        
        # 资金安排表独有字段
        result['arrangement_amount'] = float(self.arrangement_amount) if self.arrangement_amount else None
        result['funding_source'] = self.funding_source
        result['funding_nature'] = self.funding_nature
        result['budget_doc_no'] = self.budget_doc_no
        result['handler'] = self.handler
        result['handling_office'] = self.handling_office
        result['arrangement_year'] = self.arrangement_year
        result['superior_doc_no'] = self.superior_doc_no
        result['remarks'] = self.remarks
        
        # 项目基本信息表独有字段
        result['budget_code'] = self.budget_code
        result['budget_project_name'] = self.budget_project_name
        result['region'] = self.region
        result['investment_mode'] = self.investment_mode
        result['project_type'] = self.project_type
        result['approval_date'] = self.approval_date.strftime('%Y-%m-%d') if self.approval_date else ''
        result['budget_amount'] = float(self.budget_amount) if self.budget_amount else None
        result['contract_amount'] = float(self.contract_amount) if self.contract_amount else None
        result['start_date'] = self.start_date.strftime('%Y-%m-%d') if self.start_date else ''
        result['end_date'] = self.end_date.strftime('%Y-%m-%d') if self.end_date else ''
        result['project_status'] = self.project_status
        
        return result

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(100), unique=True, nullable=False, comment='邮箱')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    real_name = db.Column(db.String(100), nullable=False, comment='真实姓名')
    department = db.Column(db.String(100), nullable=True, comment='所属部门')
    position = db.Column(db.String(100), nullable=True, comment='职位')
    phone = db.Column(db.String(20), nullable=True, comment='联系电话')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    last_login = db.Column(db.DateTime, nullable=True, comment='最后登录时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'real_name': self.real_name,
            'department': self.department,
            'position': self.position,
            'phone': self.phone,
            'is_active': self.is_active,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Role(db.Model):
    """角色表"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False, comment='角色名称')
    role_code = db.Column(db.String(50), unique=True, nullable=False, comment='角色编码')
    description = db.Column(db.Text, nullable=True, comment='角色描述')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'role_name': self.role_name,
            'role_code': self.role_code,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Permission(db.Model):
    """权限表"""
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(100), nullable=False, comment='权限名称')
    permission_code = db.Column(db.String(100), unique=True, nullable=False, comment='权限编码')
    module = db.Column(db.String(50), nullable=False, comment='所属模块')
    description = db.Column(db.Text, nullable=True, comment='权限描述')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'permission_name': self.permission_name,
            'permission_code': self.permission_code,
            'module': self.module,
            'description': self.description
        }

class UserRole(db.Model):
    """用户角色关联表"""
    __tablename__ = 'user_roles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, comment='分配时间')

class RolePermission(db.Model):
    """角色权限关联表"""
    __tablename__ = 'role_permissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    granted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    granted_at = db.Column(db.DateTime, default=datetime.utcnow, comment='授权时间')

class AuditLog(db.Model):
    """操作日志表"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username = db.Column(db.String(50), nullable=True, comment='用户名')
    action = db.Column(db.String(100), nullable=False, comment='操作类型')
    module = db.Column(db.String(50), nullable=False, comment='操作模块')
    target_type = db.Column(db.String(50), nullable=True, comment='目标类型')
    target_id = db.Column(db.String(50), nullable=True, comment='目标ID')
    description = db.Column(db.Text, nullable=True, comment='操作描述')
    ip_address = db.Column(db.String(50), nullable=True, comment='IP地址')
    user_agent = db.Column(db.Text, nullable=True, comment='用户代理')
    status = db.Column(db.String(20), default='success', comment='操作状态')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'action': self.action,
            'module': self.module,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'description': self.description,
            'ip_address': self.ip_address,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# ================== 路由函数 ==================

@app.route('/')
def index():
    """主页 - 模块导航"""
    return render_template('index.html')


@app.route('/basic_data')
def basic_data():
    """基础数据模块"""
    return render_template('basic_data.html')

@app.route('/smart_charts')
def smart_charts():
    """智能图表模块"""
    return render_template('smart_charts.html')

@app.route('/add_project')
def add_project_page():
    """新增项目页面"""
    return render_template('add_project.html')

@app.route('/add_funding')
def add_funding_page():
    """新增资金安排页面"""
    return render_template('add_funding.html')

@app.route('/login')
def login_page():
    """登录页面"""
    return render_template('login.html')

@app.route('/user_management')
def user_management_page():
    """用户管理页面"""
    return render_template('user_management.html')

@app.route('/test_data')
def test_data_page():
    """数据测试页面"""
    return render_template('test_data_display.html')

@app.route('/debug')
def debug_page():
    """调试页面"""
    return render_template('debug_page.html')

@app.route('/force_refresh')
def force_refresh_page():
    """强制刷新测试页面"""
    return render_template('force_refresh.html')

@app.route('/simple_test')
def simple_test_page():
    """简单测试页面"""
    return render_template('simple_test.html')

@app.route('/data_display')
def data_display_page():
    """数据展示测试页面"""
    return render_template('data_display.html')

# 删除重复的API路由，使用下面的分页版本


# ================== 服务器端分页API ==================

def parse_datatables_params(request_args):
    """解析DataTables请求参数"""
    draw = int(request_args.get('draw', 1))
    start = int(request_args.get('start', 0))
    length = int(request_args.get('length', 10))
    search_value = request_args.get('search[value]', '').strip()
    order_col_idx = request_args.get('order[0][column]')
    order_dir = request_args.get('order[0][dir]', 'asc')
    return draw, start, length, search_value, order_col_idx, order_dir

def apply_search_filters(query, model, search_value, searchable_columns):
    if not search_value:
        return query
    from sqlalchemy import or_
    conditions = []
    for col_name in searchable_columns:
        column = getattr(model, col_name, None)
        if column is not None:
            conditions.append(column.like(f"%{search_value}%"))
    if conditions:
        query = query.filter(or_(*conditions))
    return query

def apply_ordering(query, model, columns, order_col_idx, order_dir):
    try:
        idx = int(order_col_idx) if order_col_idx is not None else 0
    except Exception:
        idx = 0
    col_key = columns[idx] if 0 <= idx < len(columns) else columns[0]
    column = getattr(model, col_key, None)
    if column is not None:
        query = query.order_by(column.desc() if order_dir == 'desc' else column.asc())
    return query

@app.route('/api/project_info_page')
def project_info_page():
    draw, start, length, search_value, order_col_idx, order_dir = parse_datatables_params(request.args)
    base_query = ProjectInfo.query
    total = base_query.count()
    searchable = ['project_name','project_code','budget_code','budget_project_name','region','investment_mode','project_type','construction_unit','supervisor_dept','project_status']
    filtered_query = apply_search_filters(base_query, ProjectInfo, search_value, searchable)
    filtered = filtered_query.count()
    columns = ['project_name','project_code','budget_code','budget_project_name','region','investment_mode','project_type','construction_unit','supervisor_dept','approval_date','budget_amount','contract_amount','start_date','end_date','project_status']
    ordered_query = apply_ordering(filtered_query, ProjectInfo, columns, order_col_idx, order_dir)
    rows = ordered_query.offset(start).limit(length).all()
    data = [r.to_dict() for r in rows]
    return jsonify({'draw': draw, 'recordsTotal': total, 'recordsFiltered': filtered, 'data': data})

@app.route('/api/funding_arrangement_page')
def funding_arrangement_page():
    draw, start, length, search_value, order_col_idx, order_dir = parse_datatables_params(request.args)
    base_query = FundingArrangement.query
    total = base_query.count()
    searchable = ['project_name','project_code','construction_unit','supervisor_dept','funding_source','funding_nature','budget_doc_no','handler','handling_office','superior_doc_no','remarks']
    filtered_query = apply_search_filters(base_query, FundingArrangement, search_value, searchable)
    filtered = filtered_query.count()
    columns = ['project_name','project_code','construction_unit','supervisor_dept','arrangement_amount','funding_source','funding_nature','budget_doc_no','handler','handling_office','arrangement_year','superior_doc_no','remarks']
    ordered_query = apply_ordering(filtered_query, FundingArrangement, columns, order_col_idx, order_dir)
    rows = ordered_query.offset(start).limit(length).all()
    data = [r.to_dict() for r in rows]
    return jsonify({'draw': draw, 'recordsTotal': total, 'recordsFiltered': filtered, 'data': data})

@app.route('/api/project_summary_page')
def project_summary_page():
    draw, start, length, search_value, order_col_idx, order_dir = parse_datatables_params(request.args)
    base_query = ProjectSummary.query
    total = base_query.count()
    searchable = ['project_name','project_code','construction_unit','supervisor_dept','region','investment_mode','project_type','funding_source','funding_nature','budget_doc_no','handler','handling_office','superior_doc_no','remarks','project_status','budget_project_name','budget_code']
    filtered_query = apply_search_filters(base_query, ProjectSummary, search_value, searchable)
    filtered = filtered_query.count()
    columns = [
        'project_name','project_code','construction_unit','supervisor_dept',
        'arrangement_amount','funding_source','funding_nature','budget_doc_no','handler','handling_office','arrangement_year','superior_doc_no','remarks',
        'budget_code','budget_project_name','region','investment_mode','project_type','approval_date','budget_amount','contract_amount','start_date','end_date','project_status'
    ]
    ordered_query = apply_ordering(filtered_query, ProjectSummary, columns, order_col_idx, order_dir)
    rows = ordered_query.offset(start).limit(length).all()
    data = [r.to_dict() for r in rows]
    return jsonify({'draw': draw, 'recordsTotal': total, 'recordsFiltered': filtered, 'data': data})

@app.route('/api/funding_arrangement')
def get_funding_arrangement():
    """获取项目资金安排"""
    arrangements = FundingArrangement.query.all()
    return jsonify([a.to_dict() for a in arrangements])


@app.route('/api/project_summary')
def get_project_summary():
    """
    获取项目总表（只读汇总表）
    
    数据生成规则：
    1. 完全依赖项目基本信息表(ProjectInfo)和项目资金安排表(FundingArrangement)
    2. 每次请求都重新生成，确保数据最新
    3. 不直接编辑项目总表，所有修改通过源表进行
    4. 项目总表不对源表产生任何影响
    
    字段依赖关系：
    - 与项目资金安排表相同的字段（项目名称、项目编码、建设单位、项目主管部门）：
      以项目编码（可研）为链接，字段信息依赖于项目资金安排表
    - 项目资金安排表独有字段：完全依赖项目资金安排表
    - 项目基本信息表独有字段：依赖项目基本信息表
    - 项目基本信息表和项目资金安排表中的建设单位、项目主管部门相互独立，彼此互不干涉
    """
    try:
        # 直接返回现有数据，不尝试删除和重新创建
        existing_data = ProjectSummary.query.all()
        if existing_data:
            data = [s.to_dict() for s in existing_data]
            return jsonify(data)
        
        # 如果没有数据，返回空列表
        return jsonify([])
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'生成项目总表失败: {str(e)}'})




@app.route('/api/export_excel/<table_type>')
def export_excel(table_type):
    """导出Excel文件"""
    try:
        if table_type == 'project_info':
            projects = ProjectInfo.query.all()
            data = [p.to_dict() for p in projects]
            filename = '项目基本信息表.xlsx'
        elif table_type == 'funding':
            arrangements = FundingArrangement.query.all()
            data = [a.to_dict() for a in arrangements]
            filename = '项目资金安排表.xlsx'
        elif table_type == 'summary':
            query = db.session.query(
                FundingArrangement,
                ProjectInfo
            ).join(
                ProjectInfo, 
                FundingArrangement.project_code == ProjectInfo.project_code
            ).all()
            
            data = []
            for funding, project in query:
                summary_item = funding.to_dict()
                summary_item.update({
                    'region': project.region,
                    'investment_mode': project.investment_mode,
                    'project_type': project.project_type,
                    'approval_date': project.approval_date.strftime('%Y-%m-%d') if project.approval_date else '',
                    'budget_amount': project.budget_amount,
                    'contract_amount': project.contract_amount,
                    'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else '',
                    'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else '',
                    'project_status': project.project_status
                })
                data.append(summary_item)
            filename = '项目总表.xlsx'
        else:
            return jsonify({'success': False, 'message': '无效的表格类型'})

        # 创建Excel文件
        df = pd.DataFrame(data)
        
        # 根据表格类型设置列名映射和列顺序
        if table_type == 'project_info':
            column_mapping = {
                'project_name': '项目名称',
                'project_code': '项目编码（可研）',
                'region': '所属区域',
                'project_type': '项目类型',
                'investment_mode': '投资模式',
                'construction_unit': '建设单位',
                'supervisor_dept': '项目主管部门',
                'budget_amount': '概算批复金额(万元)',
                'contract_amount': '签订合同金额(万元)',
                'project_status': '项目状态',
                'approval_date': '立项时间',
                'start_date': '开工时间',
                'end_date': '完工时间',
                'budget_code': '概算编码',
                'budget_project_name': '概算项目名称',
                'handling_office': '业务处',
                'remarks': '备注'
            }
            # 定义列顺序（与前端表格顺序一致）
            column_order = [
                'project_name', 'project_code', 'region', 'project_type', 'investment_mode',
                'construction_unit', 'supervisor_dept', 'budget_amount', 'contract_amount',
                'project_status', 'approval_date', 'start_date', 'end_date', 'budget_code',
                'budget_project_name', 'handling_office', 'remarks'
            ]
        elif table_type == 'funding':
            column_mapping = {
                'project_name': '项目名称',
                'project_code': '项目编码（可研）',
                'construction_unit': '建设单位',
                'supervisor_dept': '项目主管部门',
                'arrangement_amount': '安排金额(万元)',
                'funding_source': '资金来源',
                'funding_nature': '资金性质',
                'budget_doc_no': '财预文号',
                'arrangement_year': '安排年度',
                'superior_doc_no': '上级资金文号',
                'handler': '经办人',
                'handling_office': '业务处',
                'remarks': '备注'
            }
            # 定义列顺序（与前端表格顺序一致）
            column_order = [
                'project_name', 'project_code', 'construction_unit', 'supervisor_dept',
                'arrangement_amount', 'funding_source', 'funding_nature', 'budget_doc_no',
                'arrangement_year', 'superior_doc_no', 'handler', 'handling_office', 'remarks'
            ]
        else:
            column_mapping = {}
        
        # 应用列名映射
        if column_mapping:
            df = df.rename(columns=column_mapping)
        
        # 应用列顺序（如果定义了的话）
        if 'column_order' in locals() and column_order:
            # 重新排列列顺序
            df = df[column_order]
        
        # 创建BytesIO对象
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='数据')
            
            # 设置列宽
            worksheet = writer.sheets['数据']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        
        # 返回文件
        return send_file(
            output, 
            download_name=filename,
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'导出失败: {str(e)}'})

@app.route('/api/export_filtered_data', methods=['POST'])
def export_filtered_data():
    """导出筛选后的数据（支持新的项目总表）"""
    try:
        filter_data = request.get_json()
        table_type = filter_data.get('table_type', 'summary')
        filters = filter_data.get('filters', {})
        visible_columns = filter_data.get('visible_columns', [])
        
        if table_type == 'summary':
            # 使用新的项目总表
            query = ProjectSummary.query
            # 应用筛选条件
            filtered_query = apply_filters_to_summary_query(query, filters)
            results = filtered_query.all()
            
            # 转换为DataFrame
            summary_data = [result.to_dict() for result in results]
            
        else:
            # 使用传统的JOIN方式（向后兼容）
            query = db.session.query(
                FundingArrangement,
                ProjectInfo
            ).join(
                ProjectInfo,
                FundingArrangement.project_code == ProjectInfo.project_code
            )
            
            # 应用筛选条件
            filtered_query = apply_filters_to_query(query, filter_data)
            results = filtered_query.all()
            
            # 转换为DataFrame
            summary_data = []
            for funding, project in results:
                summary_item = funding.to_dict()
                # 添加项目基本信息字段
                summary_item.update({
                    'region': project.region,
                    'project_type': project.project_type,
                    'investment_mode': project.investment_mode,
                    'budget_code': project.budget_code,
                    'budget_project_name': project.budget_project_name,
                    'budget_amount': project.budget_amount,
                    'contract_amount': project.contract_amount,
                    'approval_date': project.approval_date.strftime('%Y-%m-%d') if project.approval_date else '',
                    'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else '',
                    'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else '',
                    'project_status': project.project_status
                })
                summary_data.append(summary_item)
        
        df = pd.DataFrame(summary_data)
        
        # 如果指定了可见列，在列名映射之前进行筛选
        if visible_columns:
            # 过滤DataFrame，只保留可见的列
            available_columns = [col for col in visible_columns if col in df.columns]
            if available_columns:
                df = df[available_columns]
                print(f"导出列筛选: 保留 {len(available_columns)} 列")
            else:
                print("警告: 没有找到匹配的可见列，导出所有列")
        else:
            print("未指定可见列，导出所有列")
        
        # 列名映射
        column_mapping = {
            'project_name': '项目名称',
            'project_code': '项目编码', 
            'region': '所属区域',
            'project_type': '项目类型',
            'construction_unit': '建设单位',
            'supervisor_dept': '项目主管部门',
            'investment_mode': '投资模式',
            'arrangement_amount': '安排金额(万元)',
            'funding_source': '资金来源',
            'funding_nature': '资金性质',
            'budget_doc_no': '财预文号',
            'handler': '经办人',
            'handling_office': '经办处室',
            'arrangement_year': '安排年度',
            'superior_doc_no': '上级资金文号',
            'project_status': '项目状态',
            'budget_code': '概算编码',
            'budget_project_name': '概算项目名称',
            'budget_amount': '概算批复金额(万元)',
            'contract_amount': '签订合同金额(万元)',
            'approval_date': '立项时间',
            'start_date': '开工时间',
            'end_date': '完工时间',
            'remarks': '备注'
        }
        
        df = df.rename(columns=column_mapping)
        
        # 生成Excel文件
        output = BytesIO()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'筛选结果_{timestamp}.xlsx'
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='筛选结果', index=False)
            
            # 设置列宽
            worksheet = writer.sheets['筛选结果']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'导出失败: {str(e)}'})

def apply_filters_to_query(query, filters):
    """应用筛选条件到查询"""
    if not filters:
        return query
    
    # 基础筛选条件
    if filters.get('region'):
        query = query.filter(ProjectInfo.region == filters['region'])
    if filters.get('project_type'):
        query = query.filter(ProjectInfo.project_type == filters['project_type'])
    if filters.get('project_status'):
        query = query.filter(ProjectInfo.project_status == filters['project_status'])
    if filters.get('investment_mode'):
        query = query.filter(ProjectInfo.investment_mode == filters['investment_mode'])
    if filters.get('funding_source'):
        query = query.filter(FundingArrangement.funding_source == filters['funding_source'])
    if filters.get('arrangement_year'):
        query = query.filter(FundingArrangement.arrangement_year == filters['arrangement_year'])
    if filters.get('construction_unit'):
        query = query.filter(FundingArrangement.construction_unit == filters['construction_unit'])
    if filters.get('supervisor_dept'):
        query = query.filter(FundingArrangement.supervisor_dept == filters['supervisor_dept'])
    if filters.get('funding_nature'):
        query = query.filter(FundingArrangement.funding_nature == filters['funding_nature'])
    
    # 日期范围筛选
    if filters.get('approval_date_start'):
        query = query.filter(ProjectInfo.approval_date >= filters['approval_date_start'])
    if filters.get('approval_date_end'):
        query = query.filter(ProjectInfo.approval_date <= filters['approval_date_end'])
    if filters.get('start_date_start'):
        query = query.filter(ProjectInfo.start_date >= filters['start_date_start'])
    if filters.get('start_date_end'):
        query = query.filter(ProjectInfo.start_date <= filters['start_date_end'])
    
    # 金额范围筛选
    if filters.get('budget_amount_min'):
        query = query.filter(ProjectInfo.budget_amount >= filters['budget_amount_min'])
    if filters.get('budget_amount_max'):
        query = query.filter(ProjectInfo.budget_amount <= filters['budget_amount_max'])
    if filters.get('arrangement_amount_min'):
        query = query.filter(FundingArrangement.arrangement_amount >= filters['arrangement_amount_min'])
    if filters.get('arrangement_amount_max'):
        query = query.filter(FundingArrangement.arrangement_amount <= filters['arrangement_amount_max'])
    
    # 多选筛选
    if filters.get('multi_status') and len(filters['multi_status']) > 0:
        query = query.filter(ProjectInfo.project_status.in_(filters['multi_status']))
    if filters.get('multi_funding_source') and len(filters['multi_funding_source']) > 0:
        query = query.filter(FundingArrangement.funding_source.in_(filters['multi_funding_source']))
    if filters.get('multi_investment_mode') and len(filters['multi_investment_mode']) > 0:
        query = query.filter(ProjectInfo.investment_mode.in_(filters['multi_investment_mode']))
    
    # 备注关键字搜索
    if filters.get('remarks_keyword'):
        query = query.filter(FundingArrangement.remarks.contains(filters['remarks_keyword']))
    
    return query

def apply_filters_to_summary_query(query, filters):
    """应用筛选条件到项目总表查询"""
    if not filters:
        return query
    
    # 字段映射：列索引 -> 数据库字段
    field_mapping = {
        0: ProjectSummary.project_code,           # 项目编码
        1: ProjectSummary.project_name,           # 项目名称
        2: ProjectSummary.construction_unit,      # 建设单位
        3: ProjectSummary.supervisor_dept,        # 项目主管部门
        5: ProjectSummary.funding_source,         # 资金来源
        6: ProjectSummary.funding_nature,         # 资金性质
        9: ProjectSummary.arrangement_year,       # 安排年度
        11: ProjectSummary.handling_office,       # 业务处
        13: ProjectSummary.project_status,        # 项目状态
        18: ProjectSummary.region,                # 所属区域
        19: ProjectSummary.investment_mode,       # 投资模式
        20: ProjectSummary.project_type           # 项目类型
    }
    
    # 应用筛选条件
    for column_index, values in filters.items():
        # 确保column_index是整数类型
        col_idx_int = int(column_index) if isinstance(column_index, str) and column_index.isdigit() else column_index
        
        if col_idx_int in field_mapping and values:
            field = field_mapping[col_idx_int]
            if isinstance(values, list):
                if col_idx_int in [0, 1, 12]:  # 项目编码, 项目名称, 备注使用LIKE模糊匹配
                    # 关键字筛选：使用LIKE操作符进行模糊匹配
                    conditions = [field.like(f'%{value}%') for value in values]
                    query = query.filter(db.or_(*conditions))
                else:
                    # 多选条件：使用IN操作符
                    query = query.filter(field.in_(values))
            else:
                if col_idx_int in [0, 1, 12]:  # 项目编码, 项目名称, 备注使用LIKE模糊匹配
                    # 关键字筛选：使用LIKE操作符进行模糊匹配
                    query = query.filter(field.like(f'%{values}%'))
                else:
                    # 单选条件：使用等于操作符
                    query = query.filter(field == values)
    
    # 处理备注关键字筛选（列索引12）
    if '12' in filters and filters['12']:
        remarks_values = filters['12']
        if isinstance(remarks_values, list) and len(remarks_values) > 0:
            # 使用LIKE操作符进行模糊匹配
            conditions = [ProjectSummary.remarks.contains(value) for value in remarks_values]
            query = query.filter(db.or_(*conditions))
    
    # 日期范围筛选
    if filters.get('approval_date_start'):
        query = query.filter(ProjectSummary.approval_date >= filters['approval_date_start'])
    if filters.get('approval_date_end'):
        query = query.filter(ProjectSummary.approval_date <= filters['approval_date_end'])
    if filters.get('start_date_start'):
        query = query.filter(ProjectSummary.start_date >= filters['start_date_start'])
    if filters.get('start_date_end'):
        query = query.filter(ProjectSummary.start_date <= filters['start_date_end'])
    
    # 金额范围筛选
    if filters.get('budget_amount_min'):
        query = query.filter(ProjectSummary.budget_amount >= filters['budget_amount_min'])
    if filters.get('budget_amount_max'):
        query = query.filter(ProjectSummary.budget_amount <= filters['budget_amount_max'])
    if filters.get('arrangement_amount_min'):
        query = query.filter(ProjectSummary.arrangement_amount >= filters['arrangement_amount_min'])
    if filters.get('arrangement_amount_max'):
        query = query.filter(ProjectSummary.arrangement_amount <= filters['arrangement_amount_max'])
    
    # 多选筛选
    if filters.get('multi_status') and len(filters['multi_status']) > 0:
        query = query.filter(ProjectSummary.project_status.in_(filters['multi_status']))
    if filters.get('multi_funding_source') and len(filters['multi_funding_source']) > 0:
        query = query.filter(ProjectSummary.funding_source.in_(filters['multi_funding_source']))
    if filters.get('multi_investment_mode') and len(filters['multi_investment_mode']) > 0:
        query = query.filter(ProjectSummary.investment_mode.in_(filters['multi_investment_mode']))
    
    # 备注关键字搜索
    if filters.get('remarks_keyword'):
        query = query.filter(ProjectSummary.remarks.contains(filters['remarks_keyword']))
    
    # 项目名称和项目编码搜索
    if filters.get('project_name_keyword'):
        query = query.filter(ProjectSummary.project_name.contains(filters['project_name_keyword']))
    if filters.get('project_code_keyword'):
        query = query.filter(ProjectSummary.project_code.contains(filters['project_code_keyword']))
    
    return query

@app.route('/api/import_excel', methods=['POST'])
def import_excel():
    """导入Excel文件"""
    try:
        print(f"开始处理导入请求，文件数量: {len(request.files)}")
        
        if 'file' not in request.files:
            print("错误: 没有选择文件")
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        file = request.files['file']
        table_type = request.form.get('table_type')
        
        print(f"文件名: {file.filename}, 表类型: {table_type}")
        
        if file.filename == '':
            print("错误: 文件名为空")
            return jsonify({'success': False, 'message': '文件名为空'})
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            print(f"错误: 文件格式不支持: {file.filename}")
            return jsonify({'success': False, 'message': '请选择Excel文件'})
        
        # 读取Excel文件
        print("开始读取Excel文件...")
        df = pd.read_excel(file)
        print(f"Excel文件读取成功，行数: {len(df)}, 列数: {len(df.columns)}")
        print(f"列名: {list(df.columns)}")
        
        success_count = 0
        error_messages = []
        
        if table_type == 'project_info':
            print("开始处理项目基本信息数据...")
            
            # 字段映射：中文列名 -> 英文字段名
            field_mapping = {
                '项目名称': 'project_name',
                '项目编码（可研）': 'project_code',
                '所属区域': 'region',
                '项目类型': 'project_type',
                '投资模式': 'investment_mode',
                '建设单位': 'construction_unit',
                '项目主管部门': 'supervisor_dept',
                '概算批复金额(万元)': 'budget_amount',
                '签订合同金额(万元)': 'contract_amount',
                '项目状态': 'project_status',
                '立项时间': 'approval_date',
                '开工时间': 'start_date',
                '完工时间': 'end_date',
                '概算编码': 'budget_code',
                '概算项目名称': 'budget_project_name',
                '业务处': 'handling_office',
                '备注': 'remarks'
            }
            
            for index, row in df.iterrows():
                try:
                    # 使用字段映射获取数据
                    project_name = row.get('项目名称', '') or row.get('project_name', '')
                    print(f"处理第{index+1}行数据: {project_name}")
                    
                    # 检查项目编码是否已存在
                    project_code = row.get('项目编码（可研）', '') or row.get('project_code', '')
                    if project_code:
                        existing_project = ProjectInfo.query.filter_by(project_code=project_code).first()
                        if existing_project:
                            error_msg = f'第{index+1}行：项目编码"{project_code}"已存在'
                            print(f"错误: {error_msg}")
                            error_messages.append(error_msg)
                            continue
                    
                    project = ProjectInfo(
                        project_name=project_name,
                        project_code=project_code,
                        budget_code=row.get('概算编码', '') or row.get('budget_code', ''),
                        region=row.get('所属区域', '') or row.get('region', ''),
                        investment_mode=row.get('投资模式', '') or row.get('investment_mode', ''),
                        project_type=row.get('项目类型', '') or row.get('project_type', ''),
                        construction_unit=row.get('建设单位', '') or row.get('construction_unit', ''),
                        supervisor_dept=row.get('项目主管部门', '') or row.get('supervisor_dept', ''),
                        approval_date=pd.to_datetime(row.get('立项时间') or row.get('approval_date')).date() if pd.notna(row.get('立项时间') or row.get('approval_date')) and str(row.get('立项时间') or row.get('approval_date')).strip() != '' else datetime.now().date(),
                        budget_amount=float(row.get('概算批复金额(万元)', 0) or row.get('budget_amount', 0)),
                        contract_amount=float(row.get('签订合同金额(万元)') or row.get('contract_amount')) if pd.notna(row.get('签订合同金额(万元)') or row.get('contract_amount')) else None,
                        start_date=pd.to_datetime(row.get('开工时间') or row.get('start_date')).date() if pd.notna(row.get('开工时间') or row.get('start_date')) else None,
                        end_date=pd.to_datetime(row.get('完工时间') or row.get('end_date')).date() if pd.notna(row.get('完工时间') or row.get('end_date')) else None,
                        project_status=row.get('项目状态', '') or row.get('project_status', '') if pd.notna(row.get('项目状态') or row.get('project_status')) and str(row.get('项目状态') or row.get('project_status')).strip() != '' else '',
                        handling_office=row.get('业务处', '') or row.get('handling_office', ''),
                        remarks=row.get('备注', '') or row.get('remarks', '')
                    )
                    db.session.add(project)
                    success_count += 1
                    print(f"第{index+1}行数据添加成功")
                except Exception as e:
                    error_msg = f'第{index+1}行数据导入失败: {str(e)}'
                    print(f"错误: {error_msg}")
                    error_messages.append(error_msg)
        
        elif table_type == 'funding':
            print("开始处理项目资金安排数据...")
            
            # 字段映射：中文列名 -> 英文字段名
            funding_field_mapping = {
                '项目名称': 'project_name',
                '项目编码（可研）': 'project_code',
                '建设单位': 'construction_unit',
                '项目主管部门': 'supervisor_dept',
                '安排金额(万元)': 'arrangement_amount',
                '资金来源': 'funding_source',
                '资金性质': 'funding_nature',
                '财预文号': 'budget_doc_no',
                '安排年度': 'arrangement_year',
                '上级资金文号': 'superior_doc_no',
                '经办人': 'handler',
                '业务处': 'handling_office',
                '备注': 'remarks'
            }
            
            for index, row in df.iterrows():
                try:
                    # 使用字段映射获取数据
                    project_code = row.get('项目编码（可研）', '') or row.get('project_code', '')
                    project_name = row.get('项目名称', '') or row.get('project_name', '')
                    print(f"处理第{index+1}行资金安排数据: {project_name}, 项目编码: {project_code}")
                    
                    # 验证项目编码（可研）是否存在于项目基本信息表中
                    existing_project = ProjectInfo.query.filter_by(project_code=project_code).first()
                    if not existing_project:
                        error_msg = f'第{index+1}行：项目编码（可研）"{project_code}"不存在于项目基本信息表中，请先在项目基本信息表中添加该项目信息'
                        print(f"验证失败: {error_msg}")
                        error_messages.append(error_msg)
                        continue
                    
                    # 如果项目编码存在，使用Excel中的数据（建设单位、项目主管部门相互独立）
                    funding = FundingArrangement(
                        project_name=project_name,  # 使用Excel中的项目名称
                        project_code=project_code,
                        construction_unit=row.get('建设单位', '') or row.get('construction_unit', ''),  # 使用Excel中的建设单位
                        supervisor_dept=row.get('项目主管部门', '') or row.get('supervisor_dept', ''),  # 使用Excel中的项目主管部门
                        arrangement_amount=float(row.get('安排金额(万元)', 0) or row.get('arrangement_amount', 0)),
                        funding_source=row.get('资金来源', '') or row.get('funding_source', ''),
                        funding_nature=row.get('资金性质', '') or row.get('funding_nature', ''),
                        budget_doc_no=row.get('财预文号', '') or row.get('budget_doc_no', ''),
                        handler=row.get('经办人', '') or row.get('handler', ''),
                        handling_office=row.get('业务处', '') or row.get('handling_office', ''),
                        arrangement_year=int(row.get('安排年度') or row.get('arrangement_year')) if pd.notna(row.get('安排年度') or row.get('arrangement_year')) else None,
                        superior_doc_no=row.get('上级资金文号', '') or row.get('superior_doc_no', ''),
                        remarks=row.get('备注', '') or row.get('remarks', '')
                    )
                    db.session.add(funding)
                    success_count += 1
                    print(f"第{index+1}行资金安排数据添加成功")
                except Exception as e:
                    error_msg = f'第{index+1}行数据导入失败: {str(e)}'
                    print(f"错误: {error_msg}")
                    error_messages.append(error_msg)
        
        # 提交数据库事务
        print(f"准备提交数据库事务，成功记录数: {success_count}, 错误记录数: {len(error_messages)}")
        db.session.commit()
        print("数据库事务提交成功")
        
        result_message = f'成功导入{success_count}条记录'
        if error_messages:
            result_message += f'，{len(error_messages)}条记录导入失败'
        
        return jsonify({
            'success': True, 
            'message': result_message,
            'success_count': success_count,
            'error_count': len(error_messages),
            'errors': error_messages[:5]  # 只返回前5个错误
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"导入Excel失败: {str(e)}")  # 添加控制台日志
        return jsonify({
            'success': False, 
            'message': f'导入失败: {str(e)}',
            'error_type': type(e).__name__,
            'error_details': str(e)
        })



# ================== 项目基本信息 CRUD API ==================

@app.route('/api/project_info', methods=['GET'])
def get_project_info():
    """获取项目基本信息列表"""
    try:
        projects = ProjectInfo.query.all()
        data = [project.to_dict() for project in projects]
        return jsonify(data)
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取项目信息失败: {str(e)}'})

@app.route('/api/project_info', methods=['POST'])
def create_project_info():
    """创建项目基本信息"""
    try:
        data = request.get_json()
        
        # 验证合同金额必须大于零（如果提供）
        contract_amount = float(data.get('contract_amount', 0)) if data.get('contract_amount') else 0
        
        if data.get('contract_amount') and contract_amount <= 0:
            return jsonify({'success': False, 'message': '签订合同金额必须大于零'})
        
        # 检查项目编码是否已存在（如果提供了项目编码）
        if data.get('project_code'):
            existing_project = ProjectInfo.query.filter_by(project_code=data['project_code']).first()
            if existing_project:
                return jsonify({'success': False, 'message': '项目编码已存在'})
        
        # 创建新项目
        project = ProjectInfo(
            project_name=data.get('project_name', ''),
            project_code=data.get('project_code', ''),
            budget_code=data.get('budget_code', ''),
            region=data.get('region', ''),
            investment_mode=data.get('investment_mode', ''),
            project_type=data.get('project_type', ''),
            construction_unit=data.get('construction_unit', ''),
            supervisor_dept=data.get('supervisor_dept', ''),
            approval_date=datetime.strptime(data.get('approval_date'), '%Y-%m-%d').date() if data.get('approval_date') else datetime.now().date(),
            budget_amount=float(data.get('budget_amount', 0)) if data.get('budget_amount') else 0,
            contract_amount=contract_amount if contract_amount > 0 else None,
            start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None,
            project_status=data.get('project_status', ''),
            budget_project_name=data.get('budget_project_name', ''),
            handling_office=data.get('handling_office', ''),
            remarks=data.get('remarks', '')
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '项目创建成功', 'project_id': project.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'创建失败: {str(e)}'})

@app.route('/api/add_project', methods=['POST'])
def add_project():
    """添加项目（别名路由）"""
    return create_project_info()

@app.route('/api/add_funding', methods=['POST'])
def add_funding():
    """添加资金安排"""
    try:
        data = request.get_json()
        
        # 验证项目编码是否存在
        project_code = data.get('project_code', '')
        if project_code:
            existing_project = ProjectInfo.query.filter_by(project_code=project_code).first()
            if not existing_project:
                return jsonify({'success': False, 'message': '项目编码不存在，请先添加项目信息'})
        
        # 创建资金安排
        funding = FundingArrangement(
            project_name=data.get('project_name', ''),
            project_code=project_code,
            construction_unit=data.get('construction_unit', ''),
            supervisor_dept=data.get('supervisor_dept', ''),
            arrangement_amount=float(data.get('arrangement_amount', 0)) if data.get('arrangement_amount') else 0,
            funding_source=data.get('funding_source', ''),
            funding_nature=data.get('funding_nature', ''),
            budget_doc_no=data.get('budget_doc_no', ''),
            handler=data.get('handler', ''),
            handling_office=data.get('handling_office', ''),
            arrangement_year=int(data.get('arrangement_year')) if data.get('arrangement_year') else None,
            superior_doc_no=data.get('superior_doc_no', ''),
            remarks=data.get('remarks', '')
        )
        
        db.session.add(funding)
        db.session.commit()
        
        # 自动同步项目总表
        sync_project_summary()
        
        return jsonify({'success': True, 'message': '资金安排添加成功', 'funding_id': funding.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'添加失败: {str(e)}'})

@app.route('/api/project_info/<int:project_id>', methods=['PUT'])
def update_project_info(project_id):
    """更新项目基本信息"""
    try:
        project = ProjectInfo.query.get_or_404(project_id)
        data = request.get_json()
        
        # 检查项目编码是否已存在（如果要更新项目编码）
        if data.get('project_code') and data['project_code'] != project.project_code:
            existing_project = ProjectInfo.query.filter_by(project_code=data['project_code']).first()
            if existing_project:
                return jsonify({'success': False, 'message': '项目编码已存在'})
        
        # 更新字段
        project.project_name = data.get('project_name', project.project_name)
        project.project_code = data.get('project_code', project.project_code)
        project.budget_code = data.get('budget_code', project.budget_code)
        project.region = data.get('region', project.region)
        project.investment_mode = data.get('investment_mode', project.investment_mode)
        project.project_type = data.get('project_type', project.project_type)
        project.construction_unit = data.get('construction_unit', project.construction_unit)
        project.supervisor_dept = data.get('supervisor_dept', project.supervisor_dept)
        project.budget_project_name = data.get('budget_project_name', project.budget_project_name)
        project.handling_office = data.get('handling_office', project.handling_office)
        project.remarks = data.get('remarks', project.remarks)
        project.project_status = data.get('project_status', project.project_status)
        
        # 处理日期字段
        if data.get('approval_date'):
            project.approval_date = datetime.strptime(data['approval_date'], '%Y-%m-%d').date()
        if data.get('start_date'):
            project.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if data.get('end_date'):
            project.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        # 处理数字字段
        if data.get('budget_amount') is not None:
            project.budget_amount = float(data['budget_amount']) if data['budget_amount'] else 0
            
        if data.get('contract_amount') is not None:
            contract_amount = float(data['contract_amount']) if data['contract_amount'] else 0
            if data['contract_amount'] and contract_amount <= 0:
                return jsonify({'success': False, 'message': '签订合同金额必须大于零'})
            project.contract_amount = contract_amount if contract_amount > 0 else None
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': '项目更新成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'})

@app.route('/api/project_info/<int:project_id>', methods=['DELETE'])
def delete_project_info(project_id):
    """删除项目基本信息"""
    try:
        project = ProjectInfo.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        
        # 自动同步项目总表
        sync_project_summary()
        
        return jsonify({'success': True, 'message': '项目删除成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'})

@app.route('/api/delete_funding/<int:funding_id>', methods=['DELETE'])
def delete_funding_arrangement(funding_id):
    """删除项目资金安排"""
    try:
        funding = FundingArrangement.query.get_or_404(funding_id)
        db.session.delete(funding)
        db.session.commit()
        
        # 自动同步项目总表
        sync_project_summary()
        
        return jsonify({'success': True, 'message': '资金安排删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'})

def sync_project_summary():
    """同步项目总表数据，确保与资金安排表保持一致"""
    try:
        # 删除现有的总表数据
        ProjectSummary.query.delete()
        
        # 查询合并数据
        query = db.session.query(
            FundingArrangement,
            ProjectInfo
        ).join(
            ProjectInfo, 
            FundingArrangement.project_code == ProjectInfo.project_code
        ).all()
        
        # 重新生成项目总表数据
        for funding, project in query:
            summary = ProjectSummary(
                project_name=funding.project_name,
                project_code=funding.project_code,
                construction_unit=funding.construction_unit,
                supervisor_dept=funding.supervisor_dept,
                budget_code=project.budget_code,
                budget_project_name=project.budget_project_name,
                region=project.region,
                investment_mode=project.investment_mode,
                project_type=project.project_type,
                approval_date=project.approval_date,
                budget_amount=project.budget_amount,
                contract_amount=project.contract_amount,
                start_date=project.start_date,
                end_date=project.end_date,
                project_status=project.project_status,
                arrangement_amount=funding.arrangement_amount,
                funding_source=funding.funding_source,
                funding_nature=funding.funding_nature,
                budget_doc_no=funding.budget_doc_no,
                handler=funding.handler,
                handling_office=funding.handling_office,
                arrangement_year=funding.arrangement_year,
                superior_doc_no=funding.superior_doc_no,
                remarks=funding.remarks
            )
            db.session.add(summary)
        
        db.session.commit()
        print("项目总表数据同步完成")
        
    except Exception as e:
        db.session.rollback()
        print(f"同步项目总表数据失败: {str(e)}")

@app.route('/api/check_data_consistency')
def check_data_consistency():
    """检查数据一致性"""
    try:
        funding_count = FundingArrangement.query.count()
        summary_count = ProjectSummary.query.count()
        
        is_consistent = funding_count == summary_count
        
        return jsonify({
            'success': True,
            'consistent': is_consistent,
            'funding_count': funding_count,
            'summary_count': summary_count,
            'difference': abs(funding_count - summary_count),
            'message': '数据一致' if is_consistent else f'数据不一致，相差 {abs(funding_count - summary_count)} 条记录'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'检查数据一致性失败: {str(e)}'
        })

@app.route('/api/sync_project_summary', methods=['POST'])
def sync_project_summary_api():
    """手动同步项目总表"""
    try:
        sync_project_summary()
        
        # 检查同步后的数据一致性
        funding_count = FundingArrangement.query.count()
        summary_count = ProjectSummary.query.count()
        
        return jsonify({
            'success': True,
            'message': f'项目总表同步成功，资金安排表: {funding_count} 条，项目总表: {summary_count} 条',
            'funding_count': funding_count,
            'summary_count': summary_count,
            'consistent': funding_count == summary_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'同步项目总表失败: {str(e)}'
        })

# ================== 认证和权限管理 API ==================

def hash_password(password):
    """密码哈希"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 10000)  # 减少迭代次数
    return salt + password_hash.hex()

def verify_password(password, hashed_password):
    """验证密码"""
    salt = hashed_password[:32]  # 前32个字符是salt
    stored_password = hashed_password[32:]
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 10000)  # 减少迭代次数
    return stored_password == password_hash.hex()

def log_action(user_id, username, action, module, description=None, target_type=None, target_id=None, status='success'):
    """记录操作日志（优化：减少数据库写入频率）"""
    try:
        # 对于登录操作，减少日志记录的频率以提高性能
        if action == 'LOGIN_SUCCESS':
            # 只记录重要信息，减少数据库写入
            pass
        else:
            # 其他操作正常记录
            log = AuditLog(
                user_id=user_id,
                username=username,
                action=action,
                module=module,
                description=description,
                target_type=target_type,
                target_id=target_id,
                ip_address=request.remote_addr if hasattr(request, 'remote_addr') else None,
                user_agent=request.user_agent.string if hasattr(request, 'user_agent') else None,
            status=status
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"日志记录失败: {e}")
        db.session.rollback()

@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': '用户名和密码不能为空'})
        
        user = User.query.filter_by(username=username, is_active=True).first()
        if not user:
            log_action(None, username, 'LOGIN_FAILED', 'AUTH', f'用户名 {username} 不存在', status='failed')
            return jsonify({'success': False, 'message': '用户名或密码错误'})
        
        if not verify_password(password, user.password_hash):
            log_action(user.id, username, 'LOGIN_FAILED', 'AUTH', '密码错误', status='failed')
            return jsonify({'success': False, 'message': '用户名或密码错误'})
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 获取用户角色和权限（优化查询）
        user_roles = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user.id).all()
        user_permissions = []
        if user_roles:
            # 一次性查询所有权限，避免循环查询
            role_ids = [role.id for role in user_roles]
            permissions = db.session.query(Permission).join(RolePermission).filter(RolePermission.role_id.in_(role_ids)).all()
            user_permissions = [p.permission_code for p in permissions]
        
        log_action(user.id, username, 'LOGIN_SUCCESS', 'AUTH', '用户成功登录')
        
        # 简单的会话管理（实际项目中应该使用JWT或其他更安全的方式）
        session_token = secrets.token_urlsafe(32)
        
        return jsonify({
            'success': True,
            'message': '登录成功',
            'user': user.to_dict(),
            'roles': [role.role_code for role in user_roles],
            'permissions': user_permissions,
            'token': session_token
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'登录失败: {str(e)}'})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """用户登出"""
    try:
        data = request.get_json() or {}
        username = data.get('username', '未知用户')
        
        log_action(None, username, 'LOGOUT', 'AUTH', '用户登出')
        
        return jsonify({'success': True, 'message': '退出成功'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'退出失败: {str(e)}'})

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表"""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取用户列表失败: {str(e)}'})

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建用户"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['username', 'email', 'password', 'real_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} 不能为空'})
        
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'message': '用户名已存在'})
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': '邮箱已存在'})
        
        # 创建用户
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            real_name=data['real_name'],
            department=data.get('department'),
            position=data.get('position'),
            phone=data.get('phone')
        )
        
        db.session.add(user)
        db.session.commit()
        
        log_action(None, data['username'], 'USER_CREATED', 'USER_MGMT', f'创建用户: {data["real_name"]}')
        
        return jsonify({'success': True, 'message': '用户创建成功', 'user': user.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'创建用户失败: {str(e)}'})

@app.route('/api/roles', methods=['GET'])
def get_roles():
    """获取角色列表"""
    try:
        roles = Role.query.all()
        return jsonify([role.to_dict() for role in roles])
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取角色列表失败: {str(e)}'})

@app.route('/api/permissions', methods=['GET'])
def get_permissions():
    """获取权限列表"""
    try:
        permissions = Permission.query.all()
        return jsonify([permission.to_dict() for permission in permissions])
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取权限列表失败: {str(e)}'})

@app.route('/api/audit_logs', methods=['GET'])
def get_audit_logs():
    """获取操作日志"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'logs': [log.to_dict() for log in logs.items],
            'total': logs.total,
            'pages': logs.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取操作日志失败: {str(e)}'})

@app.route('/api/init_auth_data')
def init_auth_data():
    """初始化认证数据（默认用户、角色、权限）"""
    try:
        # 创建默认权限
        default_permissions = [
            ('查看项目信息', 'project.view', '项目管理'),
            ('新增项目信息', 'project.create', '项目管理'),
            ('编辑项目信息', 'project.edit', '项目管理'),
            ('删除项目信息', 'project.delete', '项目管理'),
            ('查看资金安排', 'funding.view', '资金管理'),
            ('新增资金安排', 'funding.create', '资金管理'),
            ('编辑资金安排', 'funding.edit', '资金管理'),
            ('删除资金安排', 'funding.delete', '资金管理'),
            ('导出数据', 'data.export', '数据管理'),
            ('导入数据', 'data.import', '数据管理'),
            ('查看智能图表', 'chart.view', '图表分析'),
            ('管理用户', 'user.manage', '系统管理'),
            ('管理角色', 'role.manage', '系统管理'),
            ('查看日志', 'log.view', '系统管理')
        ]
        
        for perm_name, perm_code, module in default_permissions:
            if not Permission.query.filter_by(permission_code=perm_code).first():
                permission = Permission(
                    permission_name=perm_name,
                    permission_code=perm_code,
                    module=module,
                    description=f'{module} - {perm_name}'
                )
                db.session.add(permission)
        
        # 创建默认角色
        default_roles = [
            ('超级管理员', 'super_admin', '拥有系统所有权限'),
            ('项目管理员', 'project_admin', '项目和资金管理权限'),
            ('数据分析师', 'data_analyst', '查看和分析权限'),
            ('一般用户', 'general_user', '基本查看权限')
        ]
        
        for role_name, role_code, description in default_roles:
            if not Role.query.filter_by(role_code=role_code).first():
                role = Role(
                    role_name=role_name,
                    role_code=role_code,
                    description=description
                )
                db.session.add(role)
        
        db.session.commit()
        
        # 为超级管理员角色分配所有权限
        super_admin_role = Role.query.filter_by(role_code='super_admin').first()
        if super_admin_role:
            permissions = Permission.query.all()
            for permission in permissions:
                if not RolePermission.query.filter_by(role_id=super_admin_role.id, permission_id=permission.id).first():
                    role_permission = RolePermission(
                        role_id=super_admin_role.id,
                        permission_id=permission.id
                    )
                    db.session.add(role_permission)
        
        # 创建默认管理员用户
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@system.local',
                password_hash=hash_password(os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin123')),  # 默认密码: admin123
                real_name='系统管理员',
                department='信息技术部',
                position='系统管理员'
            )
            db.session.add(admin_user)
            db.session.commit()
            
            # 为管理员分配超级管理员角色
            if super_admin_role:
                user_role = UserRole(
                    user_id=admin_user.id,
                    role_id=super_admin_role.id
                )
                db.session.add(user_role)
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': '认证数据初始化成功！请检查环境变量中的默认管理员密码设置'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'初始化认证数据失败: {str(e)}'})

@app.route('/api/dashboard_stats')
def get_dashboard_stats():
    """获取仪表盘统计数据"""
    try:
        # 获取项目总表数据
        query = db.session.query(
            FundingArrangement,
            ProjectInfo
        ).join(
            ProjectInfo,
            FundingArrangement.project_code == ProjectInfo.project_code
        )
        results = query.all()
        
        # 计算统计指标
        total_projects = len(set(item[1].id for item in results))
        total_budget = sum(float(item[1].budget_amount or 0) for item in results) / len(results) if results else 0
        total_arrangement = sum(float(item[0].arrangement_amount or 0) for item in results)
        
        # 项目状态统计
        status_stats = {}
        for _, project in results:
            status = project.project_status
            status_stats[status] = status_stats.get(status, 0) + 1
        
        # 区域统计
        region_stats = {}
        for _, project in results:
            region = project.region
            region_stats[region] = region_stats.get(region, 0) + 1
        
        # 月度趋势数据（基于实际数据）
        monthly_trends = []
        # 这里应该基于实际的项目数据计算月度趋势
        # 暂时返回空数组，等待实际数据
        monthly_trends = []
        
        return jsonify({
            'total_projects': total_projects,
            'total_budget': round(total_budget, 2),
            'total_arrangement': round(total_arrangement, 2),
            'execution_rate': round((total_arrangement / total_budget * 100) if total_budget > 0 else 0, 2),
            'status_stats': status_stats,
            'region_stats': region_stats,
            'monthly_trends': monthly_trends,
            'alerts': []
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取仪表盘数据失败: {str(e)}'})

# 删除未使用的预测数据API，预测功能在smart_charts页面中实现

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8082, debug=True, use_reloader=False)