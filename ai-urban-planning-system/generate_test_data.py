#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统测试数据生成脚本
生成10条项目信息和30条资金安排信息
"""

import requests
import json
import random
from datetime import datetime, timedelta

# 配置
BASE_URL = "http://localhost:8082"
API_ENDPOINTS = {
    'add_project': f"{BASE_URL}/api/add_project",
    'add_funding': f"{BASE_URL}/api/add_funding"
}

# 模拟数据
REGIONS = ["雄安新区", "石家庄市", "唐山市", "秦皇岛市", "邯郸市", "邢台市", "保定市", "张家口市", "承德市", "沧州市"]
INVESTMENT_MODES = ["政府投资", "社会投资", "PPP模式", "混合投资"]
PROJECT_TYPES = ["基础设施", "公共服务", "产业园区", "交通设施", "环保工程", "智慧城市", "民生工程"]
CONSTRUCTION_UNITS = ["雄安集团", "河北建投", "中建集团", "中铁建", "中交集团", "华润集团", "保利集团", "万科集团"]
SUPERVISOR_DEPTS = ["雄安新区管委会", "河北省发改委", "河北省住建厅", "河北省交通厅", "河北省环保厅", "雄安新区规建局"]
PROJECT_STATUSES = ["前期准备", "在建", "已完工", "暂停", "延期"]
FUNDING_SOURCES = ["中央财政", "省级财政", "市级财政", "县级财政", "专项债券", "银行贷款", "社会资本"]
FUNDING_NATURES = ["建设资金", "运营资金", "维护资金", "设备采购", "人员费用", "其他费用"]
HANDLERS = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
HANDLING_OFFICES = ["规划建设处", "投资发展处", "项目管理处", "资金管理处", "综合协调处"]

def generate_project_data():
    """生成项目信息数据"""
    projects = []
    
    for i in range(10):
        project_code = f"XA{2024:04d}{i+1:03d}"
        project_name = f"雄安新区{random.choice(['基础设施', '公共服务', '产业园区', '交通设施', '环保工程'])}项目{i+1}"
        
        # 随机生成日期
        start_date = datetime.now() - timedelta(days=random.randint(30, 365))
        end_date = start_date + timedelta(days=random.randint(180, 720))
        approval_date = start_date - timedelta(days=random.randint(30, 90))
        
        project = {
            "project_name": project_name,
            "project_code": project_code,
            "budget_code": f"BUD{project_code}",
            "budget_project_name": f"概算-{project_name}",
            "region": random.choice(REGIONS),
            "investment_mode": random.choice(INVESTMENT_MODES),
            "project_type": random.choice(PROJECT_TYPES),
            "construction_unit": random.choice(CONSTRUCTION_UNITS),
            "supervisor_dept": random.choice(SUPERVISOR_DEPTS),
            "approval_date": approval_date.strftime('%Y-%m-%d'),
            "budget_amount": round(random.uniform(1000, 50000), 2),
            "contract_amount": round(random.uniform(800, 45000), 2),
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "project_status": random.choice(PROJECT_STATUSES),
            "handling_office": random.choice(HANDLING_OFFICES),
            "remarks": f"测试项目{i+1}的备注信息"
        }
        projects.append(project)
    
    return projects

def generate_funding_data(projects):
    """生成资金安排数据"""
    funding_arrangements = []
    
    for i in range(30):
        # 随机选择一个项目
        project = random.choice(projects)
        
        # 为同一个项目生成多个资金安排
        funding = {
            "project_name": project["project_name"],
            "project_code": project["project_code"],
            "construction_unit": project["construction_unit"],
            "supervisor_dept": project["supervisor_dept"],
            "arrangement_amount": round(random.uniform(100, project["budget_amount"] * 0.8), 2),
            "funding_source": random.choice(FUNDING_SOURCES),
            "funding_nature": random.choice(FUNDING_NATURES),
            "budget_doc_no": f"财预{2024}第{i+1:04d}号",
            "handler": random.choice(HANDLERS),
            "handling_office": random.choice(HANDLING_OFFICES),
            "arrangement_year": random.randint(2023, 2025),
            "superior_doc_no": f"上级{2024}第{i+1:03d}号",
            "remarks": f"资金安排{i+1}的备注信息"
        }
        funding_arrangements.append(funding)
    
    return funding_arrangements

def send_data(endpoint, data):
    """发送数据到API"""
    try:
        response = requests.post(
            endpoint,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data, ensure_ascii=False)
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return True, result.get('message', '成功')
            else:
                return False, result.get('message', '未知错误')
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
            
    except Exception as e:
        return False, f"请求失败: {str(e)}"

def main():
    """主函数"""
    print("🚀 开始生成测试数据...")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ 服务器未运行，请先启动应用")
            return
    except:
        print("❌ 无法连接到服务器，请确保应用正在运行")
        return
    
    # 生成项目数据
    print("📊 生成项目信息数据...")
    projects = generate_project_data()
    
    success_count = 0
    error_count = 0
    
    # 添加项目数据
    for i, project in enumerate(projects, 1):
        print(f"添加项目 {i}/10: {project['project_name']}")
        success, message = send_data(API_ENDPOINTS['add_project'], project)
        
        if success:
            print(f"  ✅ {message}")
            success_count += 1
        else:
            print(f"  ❌ {message}")
            error_count += 1
    
    print(f"\n📈 项目数据添加完成: 成功 {success_count} 条, 失败 {error_count} 条")
    
    # 生成资金安排数据
    print("\n💰 生成资金安排数据...")
    funding_data = generate_funding_data(projects)
    
    success_count = 0
    error_count = 0
    
    # 添加资金安排数据
    for i, funding in enumerate(funding_data, 1):
        print(f"添加资金安排 {i}/30: {funding['project_name']}")
        success, message = send_data(API_ENDPOINTS['add_funding'], funding)
        
        if success:
            print(f"  ✅ {message}")
            success_count += 1
        else:
            print(f"  ❌ {message}")
            error_count += 1
    
    print(f"\n📈 资金安排数据添加完成: 成功 {success_count} 条, 失败 {error_count} 条")
    
    print("\n" + "=" * 50)
    print("🎉 测试数据生成完成！")
    print(f"📊 项目信息: {len(projects)} 条")
    print(f"💰 资金安排: {len(funding_data)} 条")
    print(f"🌐 访问地址: {BASE_URL}")
    print("=" * 50)

if __name__ == "__main__":
    main()
