#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出功能修复脚本
"""

from app import app, db, FundingArrangement, ProjectInfo
import pandas as pd
from io import BytesIO
from flask import send_file

def export_funding_simple():
    """简化的资金安排表导出"""
    with app.app_context():
        try:
            # 获取数据
            arrangements = FundingArrangement.query.all()
            data = [a.to_dict() for a in arrangements]
            
            # 创建DataFrame
            df = pd.DataFrame(data)
            
            # 列名映射
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
            
            # 应用列名映射
            existing_mapping = {k: v for k, v in column_mapping.items() if k in df.columns}
            df = df.rename(columns=existing_mapping)
            
            # 创建Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='项目资金安排表')
                
                # 设置列宽
                worksheet = writer.sheets['项目资金安排表']
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
            
            # 保存到文件进行测试
            with open('/tmp/funding_export_fixed.xlsx', 'wb') as f:
                f.write(output.getvalue())
            
            print(f"导出完成，文件大小: {len(output.getvalue())} 字节")
            
            # 验证
            df_verify = pd.read_excel('/tmp/funding_export_fixed.xlsx')
            print(f"验证文件行数: {len(df_verify)}")
            print(f"验证文件列数: {len(df_verify.columns)}")
            
            if len(df_verify) > 0:
                print("✅ 导出成功！")
                print("前3行数据:")
                print(df_verify.head(3).to_string())
                return True
            else:
                print("❌ 导出失败")
                return False
                
        except Exception as e:
            print(f"导出失败: {e}")
            return False

if __name__ == "__main__":
    export_funding_simple()
