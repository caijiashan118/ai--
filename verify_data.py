#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证脚本
验证导入的模拟数据质量和完整性
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, ProjectInfo, FundingArrangement

def verify_projects_data():
    """验证项目基本信息数据"""
    print("📊 验证项目基本信息数据...")
    
    with app.app_context():
        projects = ProjectInfo.query.all()
        total_count = len(projects)
        print(f"📈 总项目数: {total_count}")
        
        # 检查数据完整性
        issues = []
        
        for project in projects:
            # 检查必填字段
            if not project.project_name:
                issues.append(f"项目 {project.id}: 项目名称为空")
            if not project.project_code:
                issues.append(f"项目 {project.id}: 项目编码为空")
            if not project.region:
                issues.append(f"项目 {project.id}: 所属区域为空")
            if not project.project_type:
                issues.append(f"项目 {project.id}: 项目类型为空")
            if not project.construction_unit:
                issues.append(f"项目 {project.id}: 建设单位为空")
            if not project.supervisor_dept:
                issues.append(f"项目 {project.id}: 项目主管部门为空")
            if not project.project_status:
                issues.append(f"项目 {project.id}: 项目状态为空")
            
            # 检查金额合理性
            if project.budget_amount and project.budget_amount <= 0:
                issues.append(f"项目 {project.id}: 预算金额不合理")
            if project.contract_amount and project.contract_amount <= 0:
                issues.append(f"项目 {project.id}: 合同金额不合理")
        
        # 统计信息
        print(f"✅ 数据完整性检查完成")
        if issues:
            print(f"⚠️ 发现 {len(issues)} 个问题:")
            for issue in issues[:10]:  # 只显示前10个问题
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... 还有 {len(issues) - 10} 个问题")
        else:
            print("✅ 所有项目数据完整")
        
        # 统计各字段分布
        print(f"\n📊 项目数据分布:")
        
        # 区域分布
        regions = {}
        for project in projects:
            region = project.region
            regions[region] = regions.get(region, 0) + 1
        
        print(f"  区域分布:")
        for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
            print(f"    {region}: {count} 个")
        
        # 项目类型分布
        types = {}
        for project in projects:
            ptype = project.project_type
            types[ptype] = types.get(ptype, 0) + 1
        
        print(f"  项目类型分布:")
        for ptype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"    {ptype}: {count} 个")
        
        # 投资模式分布
        modes = {}
        for project in projects:
            mode = project.investment_mode
            modes[mode] = modes.get(mode, 0) + 1
        
        print(f"  投资模式分布:")
        for mode, count in sorted(modes.items(), key=lambda x: x[1], reverse=True):
            print(f"    {mode}: {count} 个")
        
        return len(issues) == 0

def verify_funding_data():
    """验证资金安排数据"""
    print("\n💰 验证资金安排数据...")
    
    with app.app_context():
        fundings = FundingArrangement.query.all()
        total_count = len(fundings)
        print(f"📈 总资金安排数: {total_count}")
        
        # 检查数据完整性
        issues = []
        
        for funding in fundings:
            # 检查必填字段
            if not funding.project_name:
                issues.append(f"资金安排 {funding.id}: 项目名称为空")
            if not funding.project_code:
                issues.append(f"资金安排 {funding.id}: 项目编码为空")
            if not funding.funding_source:
                issues.append(f"资金安排 {funding.id}: 资金来源为空")
            if not funding.funding_nature:
                issues.append(f"资金安排 {funding.id}: 资金性质为空")
            
            # 检查金额合理性
            if not funding.arrangement_amount or funding.arrangement_amount <= 0:
                issues.append(f"资金安排 {funding.id}: 安排金额不合理")
        
        # 统计信息
        print(f"✅ 数据完整性检查完成")
        if issues:
            print(f"⚠️ 发现 {len(issues)} 个问题:")
            for issue in issues[:10]:  # 只显示前10个问题
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... 还有 {len(issues) - 10} 个问题")
        else:
            print("✅ 所有资金安排数据完整")
        
        # 统计各字段分布
        print(f"\n📊 资金安排数据分布:")
        
        # 资金来源分布
        sources = {}
        for funding in fundings:
            source = funding.funding_source
            sources[source] = sources.get(source, 0) + 1
        
        print(f"  资金来源分布:")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            print(f"    {source}: {count} 个")
        
        # 资金性质分布
        natures = {}
        for funding in fundings:
            nature = funding.funding_nature
            natures[nature] = natures.get(nature, 0) + 1
        
        print(f"  资金性质分布:")
        for nature, count in sorted(natures.items(), key=lambda x: x[1], reverse=True):
            print(f"    {nature}: {count} 个")
        
        # 年度分布
        years = {}
        for funding in fundings:
            year = funding.arrangement_year
            if year:
                years[year] = years.get(year, 0) + 1
        
        print(f"  安排年度分布:")
        for year, count in sorted(years.items(), key=lambda x: x[0], reverse=True):
            print(f"    {year}年: {count} 个")
        
        return len(issues) == 0

def verify_data_relationships():
    """验证数据关联性"""
    print("\n🔗 验证数据关联性...")
    
    with app.app_context():
        # 检查项目编码关联
        projects = ProjectInfo.query.all()
        fundings = FundingArrangement.query.all()
        
        project_codes = {p.project_code for p in projects}
        funding_project_codes = {f.project_code for f in fundings}
        
        # 找出资金安排中引用了不存在项目的编码
        orphaned_codes = funding_project_codes - project_codes
        
        if orphaned_codes:
            print(f"⚠️ 发现 {len(orphaned_codes)} 个孤立的项目编码:")
            for code in list(orphaned_codes)[:10]:
                print(f"  - {code}")
            if len(orphaned_codes) > 10:
                print(f"  ... 还有 {len(orphaned_codes) - 10} 个")
        else:
            print("✅ 所有资金安排都有对应的项目")
        
        # 统计每个项目的资金安排数量
        project_funding_count = {}
        for funding in fundings:
            code = funding.project_code
            project_funding_count[code] = project_funding_count.get(code, 0) + 1
        
        print(f"\n📊 项目资金安排统计:")
        print(f"  平均每个项目资金安排数: {sum(project_funding_count.values()) / len(project_funding_count):.1f}")
        print(f"  最多资金安排数: {max(project_funding_count.values())}")
        print(f"  最少资金安排数: {min(project_funding_count.values())}")
        
        return len(orphaned_codes) == 0

def main():
    """主函数"""
    print("🔍 开始验证模拟数据...")
    
    with app.app_context():
        # 验证项目数据
        projects_ok = verify_projects_data()
        
        # 验证资金安排数据
        funding_ok = verify_funding_data()
        
        # 验证数据关联性
        relationships_ok = verify_data_relationships()
        
        # 总结
        print(f"\n📋 验证结果总结:")
        print(f"  项目基本信息: {'✅ 通过' if projects_ok else '❌ 失败'}")
        print(f"  资金安排数据: {'✅ 通过' if funding_ok else '❌ 失败'}")
        print(f"  数据关联性: {'✅ 通过' if relationships_ok else '❌ 失败'}")
        
        if projects_ok and funding_ok and relationships_ok:
            print(f"\n🎉 所有数据验证通过！")
        else:
            print(f"\n⚠️ 部分数据验证失败，请检查上述问题")

if __name__ == "__main__":
    main()
