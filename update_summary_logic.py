#!/usr/bin/env python3
"""
更新项目总表生成逻辑
使用LEFT JOIN显示所有项目，包括只有资金安排的项目
"""

def update_summary_logic():
    """更新项目总表生成逻辑"""
    
    # 读取当前的app.py文件
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找migrate_to_summary函数
    old_join = '''        # 查询合并数据
        query = db.session.query(
            FundingArrangement,
            ProjectInfo
        ).join(
            ProjectInfo, 
            FundingArrangement.project_code == ProjectInfo.project_code
        ).all()'''
    
    new_join = '''        # 查询合并数据 - 使用LEFT JOIN显示所有资金安排项目
        query = db.session.query(
            FundingArrangement,
            ProjectInfo
        ).outerjoin(
            ProjectInfo, 
            FundingArrangement.project_code == ProjectInfo.project_code
        ).all()'''
    
    # 替换JOIN逻辑
    if old_join in content:
        content = content.replace(old_join, new_join)
        
        # 更新处理逻辑，处理ProjectInfo为None的情况
        old_processing = '''        migrated_count = 0
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
            )'''
        
        new_processing = '''        migrated_count = 0
        for funding, project in query:
            # 处理没有项目基本信息的情况
            if project is None:
                # 使用默认值或资金安排表中的信息
                summary = ProjectSummary(
                    project_name=funding.project_name,
                    project_code=funding.project_code,
                    construction_unit=funding.construction_unit,
                    supervisor_dept=funding.supervisor_dept,
                    budget_code=f"BUD{funding.project_code}",
                    budget_project_name=funding.project_name,
                    region="未知区域",
                    investment_mode="未知模式",
                    project_type="未知类型",
                    approval_date=None,
                    budget_amount=None,
                    contract_amount=None,
                    start_date=None,
                    end_date=None,
                    project_status="未知状态",
                    arrangement_amount=funding.arrangement_amount,
                    funding_source=funding.funding_source,
                    funding_nature=funding.funding_nature,
                    budget_doc_no=funding.budget_doc_no,
                    handler=funding.handler,
                    handling_office=funding.handling_office,
                    arrangement_year=funding.arrangement_year,
                    superior_doc_no=funding.superior_doc_no,
                    remarks=f"只有资金安排记录 - {funding.remarks or ''}"
                )
            else:
                # 正常情况，两个表都有数据
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
                )'''
        
        if old_processing in content:
            content = content.replace(old_processing, new_processing)
            
            # 保存更新后的文件
            with open('app.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 已更新项目总表生成逻辑，使用LEFT JOIN")
            print("现在项目总表将显示所有资金安排项目，包括没有基本信息的项目")
        else:
            print("❌ 未找到处理逻辑，请手动更新")
    else:
        print("❌ 未找到JOIN逻辑，请手动更新")

if __name__ == "__main__":
    update_summary_logic()
