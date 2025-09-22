#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI城建系统数据统计脚本
"""

import requests
import json
from collections import Counter

BASE_URL = "http://localhost:8082"

def get_data(endpoint):
    """获取数据"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 获取数据失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []

def analyze_projects(projects):
    """分析项目数据"""
    print("📊 项目信息统计")
    print("=" * 40)
    print(f"总项目数: {len(projects)}")
    
    if not projects:
        return
    
    # 按区域统计
    regions = [p.get('region', '未知') for p in projects]
    region_count = Counter(regions)
    print(f"\n🏢 按区域分布:")
    for region, count in region_count.most_common():
        print(f"  {region}: {count} 个")
    
    # 按项目类型统计
    types = [p.get('project_type', '未知') for p in projects]
    type_count = Counter(types)
    print(f"\n🏗️ 按项目类型分布:")
    for ptype, count in type_count.most_common():
        print(f"  {ptype}: {count} 个")
    
    # 按投资模式统计
    modes = [p.get('investment_mode', '未知') for p in projects]
    mode_count = Counter(modes)
    print(f"\n💰 按投资模式分布:")
    for mode, count in mode_count.most_common():
        print(f"  {mode}: {count} 个")
    
    # 按项目状态统计
    statuses = [p.get('project_status', '未知') for p in projects]
    status_count = Counter(statuses)
    print(f"\n📈 按项目状态分布:")
    for status, count in status_count.most_common():
        print(f"  {status}: {count} 个")
    
    # 预算金额统计
    budget_amounts = [p.get('budget_amount', 0) for p in projects if p.get('budget_amount')]
    if budget_amounts:
        total_budget = sum(budget_amounts)
        avg_budget = total_budget / len(budget_amounts)
        max_budget = max(budget_amounts)
        min_budget = min(budget_amounts)
        print(f"\n💵 预算金额统计:")
        print(f"  总预算: {total_budget:,.2f} 万元")
        print(f"  平均预算: {avg_budget:,.2f} 万元")
        print(f"  最大预算: {max_budget:,.2f} 万元")
        print(f"  最小预算: {min_budget:,.2f} 万元")

def analyze_funding(funding_data):
    """分析资金安排数据"""
    print("\n💰 资金安排统计")
    print("=" * 40)
    print(f"总资金安排数: {len(funding_data)}")
    
    if not funding_data:
        return
    
    # 按资金来源统计
    sources = [f.get('funding_source', '未知') for f in funding_data]
    source_count = Counter(sources)
    print(f"\n🏦 按资金来源分布:")
    for source, count in source_count.most_common():
        print(f"  {source}: {count} 个")
    
    # 按资金性质统计
    natures = [f.get('funding_nature', '未知') for f in funding_data]
    nature_count = Counter(natures)
    print(f"\n📋 按资金性质分布:")
    for nature, count in nature_count.most_common():
        print(f"  {nature}: {count} 个")
    
    # 按安排年度统计
    years = [f.get('arrangement_year') for f in funding_data if f.get('arrangement_year')]
    year_count = Counter(years)
    print(f"\n📅 按安排年度分布:")
    for year, count in sorted(year_count.items()):
        print(f"  {year}年: {count} 个")
    
    # 资金金额统计
    amounts = [f.get('arrangement_amount', 0) for f in funding_data if f.get('arrangement_amount')]
    if amounts:
        total_amount = sum(amounts)
        avg_amount = total_amount / len(amounts)
        max_amount = max(amounts)
        min_amount = min(amounts)
        print(f"\n💵 资金金额统计:")
        print(f"  总安排金额: {total_amount:,.2f} 万元")
        print(f"  平均安排金额: {avg_amount:,.2f} 万元")
        print(f"  最大安排金额: {max_amount:,.2f} 万元")
        print(f"  最小安排金额: {min_amount:,.2f} 万元")

def analyze_summary(summary_data):
    """分析项目总表数据"""
    print("\n📊 项目总表统计")
    print("=" * 40)
    print(f"总记录数: {len(summary_data)}")
    
    if not summary_data:
        return
    
    # 按项目编码统计（查看每个项目有多少条资金安排）
    project_codes = [s.get('project_code', '') for s in summary_data]
    code_count = Counter(project_codes)
    print(f"\n🔗 项目资金安排分布:")
    for code, count in code_count.most_common(10):  # 显示前10个
        print(f"  {code}: {count} 条资金安排")

def main():
    """主函数"""
    print("🔍 AI城建系统数据统计分析")
    print("=" * 50)
    
    # 获取数据
    print("📥 正在获取数据...")
    projects = get_data("/api/project_info")
    funding_data = get_data("/api/funding_arrangement")
    summary_data = get_data("/api/project_summary")
    
    # 分析数据
    analyze_projects(projects)
    analyze_funding(funding_data)
    analyze_summary(summary_data)
    
    print("\n" + "=" * 50)
    print("✅ 数据分析完成！")
    print(f"🌐 访问系统: {BASE_URL}")

if __name__ == "__main__":
    main()
