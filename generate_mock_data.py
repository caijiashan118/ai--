#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟数据生成脚本
为项目基本信息表和资金安排表生成测试数据
"""

import random
import string
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

# 初始化Faker
fake = Faker('zh_CN')

# 模拟数据配置
PROJECT_COUNT = 100
FUNDING_COUNT = 1000

# 预定义的数据选项
REGIONS = ['雄县', '容城县', '安新县', '雄安新区核心区', '启动区', '起步区', '其他区域']
INVESTMENT_MODES = ['政府投资', '社会投资', '政府和社会资本合作(PPP)', '混合投资', '其他']
PROJECT_TYPES = ['基础设施', '公共服务', '产业园区', '住宅建设', '商业开发', '交通设施', '水利工程', '环保工程', '其他']
CONSTRUCTION_UNITS = [
    '雄安新区管委会', '雄安集团', '中国建筑', '中国铁建', '中国交建', '中国电建',
    '中建八局', '中铁建工', '中交一公局', '中电建路桥', '北京建工', '上海建工',
    '广东建工', '浙江建工', '河北建工', '雄安新区建设投资集团', '其他建设单位'
]
SUPERVISOR_DEPTS = [
    '雄安新区管委会', '雄安新区规划建设局', '雄安新区经济发展局', '雄安新区公共服务局',
    '雄安新区生态环境局', '雄安新区交通局', '雄安新区水务局', '雄安新区住房和城乡建设局',
    '雄安新区财政局', '雄安新区审计局', '其他部门'
]
FUNDING_SOURCES = [
    '中央财政', '省级财政', '市级财政', '县级财政', '政府债券', '银行贷款',
    '社会资本', 'PPP项目资金', '专项基金', '其他资金'
]
FUNDING_NATURES = [
    '基本建设投资', '技术改造投资', '设备购置', '人员经费', '运营维护费',
    '前期费用', '其他费用'
]
HANDLING_OFFICES = [
    '规划建设处', '经济发展处', '公共服务处', '生态环境处', '交通处',
    '水务处', '住房建设处', '财政处', '审计处', '其他处室'
]
PROJECT_STATUSES = ['前期准备', '在建', '已完工', '暂停', '延期', '其他']

def generate_project_code():
    """生成项目编码"""
    year = random.randint(2020, 2025)
    region_code = random.choice(['XA', 'XC', 'XX', 'XQ', 'QD', 'QB', 'QT'])
    type_code = random.choice(['JC', 'GG', 'CY', 'ZZ', 'SY', 'JT', 'SL', 'HB', 'QT'])
    sequence = random.randint(1000, 9999)
    return f"{year}{region_code}{type_code}{sequence}"

def generate_budget_code():
    """生成预算编码"""
    year = random.randint(2020, 2025)
    dept_code = random.choice(['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'])
    sequence = random.randint(10000, 99999)
    return f"{year}{dept_code}{sequence}"

def generate_project_name(project_type):
    """生成项目名称"""
    prefixes = {
        '基础设施': ['雄安新区', '容城县', '安新县', '雄县'],
        '公共服务': ['雄安新区', '容城县', '安新县', '雄县'],
        '产业园区': ['雄安新区', '容城县', '安新县', '雄县'],
        '住宅建设': ['雄安新区', '容城县', '安新县', '雄县'],
        '商业开发': ['雄安新区', '容城县', '安新县', '雄县'],
        '交通设施': ['雄安新区', '容城县', '安新县', '雄县'],
        '水利工程': ['雄安新区', '容城县', '安新县', '雄县'],
        '环保工程': ['雄安新区', '容城县', '安新县', '雄县'],
        '其他': ['雄安新区', '容城县', '安新县', '雄县']
    }
    
    suffixes = {
        '基础设施': ['道路建设', '桥梁工程', '管网建设', '电力设施', '通信设施'],
        '公共服务': ['学校建设', '医院建设', '文化中心', '体育设施', '社区服务中心'],
        '产业园区': ['科技园区', '产业基地', '创新中心', '孵化器', '总部基地'],
        '住宅建设': ['安置房', '商品房', '保障房', '人才公寓', '社区住宅'],
        '商业开发': ['商业综合体', '购物中心', '写字楼', '酒店', '商业街'],
        '交通设施': ['高速公路', '城市道路', '轨道交通', '公交枢纽', '停车场'],
        '水利工程': ['河道治理', '水库建设', '供水工程', '排水工程', '水环境治理'],
        '环保工程': ['污水处理', '垃圾处理', '生态修复', '环境监测', '绿化工程'],
        '其他': ['综合项目', '改造项目', '维护项目', '升级项目', '其他工程']
    }
    
    prefix = random.choice(prefixes.get(project_type, prefixes['其他']))
    suffix = random.choice(suffixes.get(project_type, suffixes['其他']))
    return f"{prefix}{suffix}项目"

def generate_project_data():
    """生成项目基本信息数据"""
    projects = []
    
    for i in range(PROJECT_COUNT):
        project_type = random.choice(PROJECT_TYPES)
        project_name = generate_project_name(project_type)
        
        # 生成日期
        approval_date = fake.date_between(start_date=datetime(2020, 1, 1), end_date=datetime(2025, 12, 31))
        start_date = approval_date + timedelta(days=random.randint(30, 180))
        end_date = start_date + timedelta(days=random.randint(180, 1095))
        
        # 生成金额
        budget_amount = random.randint(1000000, 500000000)  # 100万到5亿
        contract_amount = budget_amount * random.uniform(0.8, 1.2)
        
        project = {
            'project_name': project_name,
            'project_code': generate_project_code(),
            'budget_code': generate_budget_code(),
            'budget_project_name': f"{project_name}（预算）",
            'region': random.choice(REGIONS),
            'investment_mode': random.choice(INVESTMENT_MODES),
            'project_type': project_type,
            'construction_unit': random.choice(CONSTRUCTION_UNITS),
            'supervisor_dept': random.choice(SUPERVISOR_DEPTS),
            'approval_date': approval_date.strftime('%Y-%m-%d'),
            'budget_amount': budget_amount,
            'contract_amount': round(contract_amount, 2),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'project_status': random.choice(PROJECT_STATUSES)
        }
        projects.append(project)
    
    return projects

def generate_funding_data(projects):
    """生成资金安排数据"""
    funding_arrangements = []
    
    for i in range(FUNDING_COUNT):
        # 随机选择一个项目
        project = random.choice(projects)
        
        # 生成资金安排
        arrangement_amount = random.randint(100000, 50000000)  # 10万到5000万
        arrangement_year = random.randint(2020, 2025)
        
        funding = {
            'project_name': project['project_name'],
            'project_code': project['project_code'],
            'construction_unit': project['construction_unit'],
            'supervisor_dept': project['supervisor_dept'],
            'arrangement_amount': arrangement_amount,
            'funding_source': random.choice(FUNDING_SOURCES),
            'funding_nature': random.choice(FUNDING_NATURES),
            'budget_doc_no': f"XA{arrangement_year}{random.randint(1000, 9999)}",
            'handler': fake.name(),
            'handling_office': random.choice(HANDLING_OFFICES),
            'arrangement_year': arrangement_year,
            'superior_doc_no': f"上级{arrangement_year}{random.randint(100, 999)}",
            'remarks': fake.sentence(nb_words=random.randint(5, 15))
        }
        funding_arrangements.append(funding)
    
    return funding_arrangements

def main():
    """主函数"""
    print("🚀 开始生成模拟数据...")
    
    # 生成项目数据
    print(f"📊 生成 {PROJECT_COUNT} 条项目基本信息...")
    projects = generate_project_data()
    
    # 生成资金安排数据
    print(f"💰 生成 {FUNDING_COUNT} 条资金安排数据...")
    funding_arrangements = generate_funding_data(projects)
    
    # 保存为Excel文件
    print("💾 保存数据到Excel文件...")
    
    # 保存项目数据
    projects_df = pd.DataFrame(projects)
    projects_df.to_excel('mock_projects.xlsx', index=False, sheet_name='项目基本信息')
    
    # 保存资金安排数据
    funding_df = pd.DataFrame(funding_arrangements)
    funding_df.to_excel('mock_funding.xlsx', index=False, sheet_name='资金安排')
    
    # 保存合并数据
    with pd.ExcelWriter('mock_data_all.xlsx', engine='openpyxl') as writer:
        projects_df.to_excel(writer, sheet_name='项目基本信息', index=False)
        funding_df.to_excel(writer, sheet_name='资金安排', index=False)
    
    print("✅ 数据生成完成！")
    print(f"📁 生成的文件:")
    print(f"   - mock_projects.xlsx ({len(projects)} 条项目数据)")
    print(f"   - mock_funding.xlsx ({len(funding_arrangements)} 条资金数据)")
    print(f"   - mock_data_all.xlsx (合并数据)")
    
    # 显示统计信息
    print("\n📈 数据统计:")
    print(f"项目类型分布:")
    project_types = pd.Series([p['project_type'] for p in projects]).value_counts()
    for ptype, count in project_types.items():
        print(f"  {ptype}: {count} 个")
    
    print(f"\n区域分布:")
    regions = pd.Series([p['region'] for p in projects]).value_counts()
    for region, count in regions.items():
        print(f"  {region}: {count} 个")
    
    print(f"\n资金来源分布:")
    funding_sources = pd.Series([f['funding_source'] for f in funding_arrangements]).value_counts()
    for source, count in funding_sources.items():
        print(f"  {source}: {count} 个")

if __name__ == "__main__":
    main()
