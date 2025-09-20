#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟数据导入脚本
将生成的模拟数据导入到数据库中
"""

import pandas as pd
from datetime import datetime
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, ProjectInfo, FundingArrangement

def import_projects_data():
    """导入项目基本信息数据"""
    print("📊 开始导入项目基本信息数据...")
    
    try:
        # 读取Excel文件
        df = pd.read_excel('mock_projects.xlsx')
        print(f"📁 读取到 {len(df)} 条项目数据")
        
        # 清空现有数据（可选）
        # ProjectInfo.query.delete()
        # db.session.commit()
        # print("🗑️ 已清空现有项目数据")
        
        # 导入新数据
        imported_count = 0
        for index, row in df.iterrows():
            try:
                # 检查项目编码是否已存在
                existing_project = ProjectInfo.query.filter_by(project_code=row['project_code']).first()
                if existing_project:
                    print(f"⚠️ 项目编码 {row['project_code']} 已存在，跳过")
                    continue
                
                # 创建新项目记录
                project = ProjectInfo(
                    project_name=row['project_name'],
                    project_code=row['project_code'],
                    budget_code=row['budget_code'],
                    budget_project_name=row['budget_project_name'],
                    region=row['region'],
                    investment_mode=row['investment_mode'],
                    project_type=row['project_type'],
                    construction_unit=row['construction_unit'],
                    supervisor_dept=row['supervisor_dept'],
                    approval_date=datetime.strptime(row['approval_date'], '%Y-%m-%d').date(),
                    budget_amount=float(row['budget_amount']),
                    contract_amount=float(row['contract_amount']) if pd.notna(row['contract_amount']) else None,
                    start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date() if pd.notna(row['start_date']) else None,
                    end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date() if pd.notna(row['end_date']) else None,
                    project_status=row['project_status']
                )
                
                db.session.add(project)
                imported_count += 1
                
                if imported_count % 50 == 0:
                    print(f"📈 已导入 {imported_count} 条项目数据...")
                    
            except Exception as e:
                print(f"❌ 导入项目 {row['project_code']} 失败: {str(e)}")
                continue
        
        # 提交到数据库
        db.session.commit()
        print(f"✅ 成功导入 {imported_count} 条项目基本信息数据")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ 导入项目数据失败: {str(e)}")
        return False
    
    return True

def import_funding_data():
    """导入资金安排数据"""
    print("💰 开始导入资金安排数据...")
    
    try:
        # 读取Excel文件
        df = pd.read_excel('mock_funding.xlsx')
        print(f"📁 读取到 {len(df)} 条资金安排数据")
        
        # 清空现有数据（可选）
        # FundingArrangement.query.delete()
        # db.session.commit()
        # print("🗑️ 已清空现有资金安排数据")
        
        # 导入新数据
        imported_count = 0
        for index, row in df.iterrows():
            try:
                # 创建新资金安排记录
                funding = FundingArrangement(
                    project_name=row['project_name'],
                    project_code=row['project_code'],
                    construction_unit=row['construction_unit'],
                    supervisor_dept=row['supervisor_dept'],
                    arrangement_amount=float(row['arrangement_amount']),
                    funding_source=row['funding_source'],
                    funding_nature=row['funding_nature'],
                    budget_doc_no=row['budget_doc_no'] if pd.notna(row['budget_doc_no']) else None,
                    handler=row['handler'] if pd.notna(row['handler']) else None,
                    handling_office=row['handling_office'] if pd.notna(row['handling_office']) else None,
                    arrangement_year=int(row['arrangement_year']) if pd.notna(row['arrangement_year']) else None,
                    superior_doc_no=row['superior_doc_no'] if pd.notna(row['superior_doc_no']) else None,
                    remarks=row['remarks'] if pd.notna(row['remarks']) else None
                )
                
                db.session.add(funding)
                imported_count += 1
                
                if imported_count % 100 == 0:
                    print(f"📈 已导入 {imported_count} 条资金安排数据...")
                    
            except Exception as e:
                print(f"❌ 导入资金安排 {row['project_code']} 失败: {str(e)}")
                continue
        
        # 提交到数据库
        db.session.commit()
        print(f"✅ 成功导入 {imported_count} 条资金安排数据")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ 导入资金安排数据失败: {str(e)}")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 开始导入模拟数据到数据库...")
    
    with app.app_context():
        # 创建数据库表（如果不存在）
        db.create_all()
        print("📋 数据库表已准备就绪")
        
        # 导入项目数据
        if not import_projects_data():
            print("❌ 项目数据导入失败，停止导入")
            return
        
        # 导入资金安排数据
        if not import_funding_data():
            print("❌ 资金安排数据导入失败")
            return
        
        # 显示最终统计
        print("\n📊 导入完成统计:")
        project_count = ProjectInfo.query.count()
        funding_count = FundingArrangement.query.count()
        print(f"📈 项目基本信息: {project_count} 条")
        print(f"💰 资金安排: {funding_count} 条")
        
        print("\n✅ 所有模拟数据导入完成！")
        print("🌐 请访问 http://localhost:8080 查看数据")

if __name__ == "__main__":
    main()
