#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试导出功能
"""

from app import app, db, ProjectInfo, FundingArrangement
import pandas as pd

def debug_export():
    """调试导出功能"""
    with app.app_context():
        print("=== 调试导出功能 ===")
        
        # 检查项目基本信息表数据
        print("\n1. 项目基本信息表数据:")
        projects = ProjectInfo.query.limit(1).all()
        if projects:
            project = projects[0]
            print(f"项目名称: {project.project_name}")
            print(f"项目编码: {project.project_code}")
            
            # 转换为字典
            project_dict = project.to_dict()
            print(f"to_dict()结果: {project_dict}")
            
            # 创建DataFrame
            df = pd.DataFrame([project_dict])
            print(f"DataFrame列名: {list(df.columns)}")
            print(f"DataFrame形状: {df.shape}")
        
        # 检查项目资金安排表数据
        print("\n2. 项目资金安排表数据:")
        arrangements = FundingArrangement.query.limit(1).all()
        if arrangements:
            arrangement = arrangements[0]
            print(f"项目名称: {arrangement.project_name}")
            print(f"项目编码: {arrangement.project_code}")
            
            # 转换为字典
            arrangement_dict = arrangement.to_dict()
            print(f"to_dict()结果: {arrangement_dict}")
            
            # 创建DataFrame
            df = pd.DataFrame([arrangement_dict])
            print(f"DataFrame列名: {list(df.columns)}")
            print(f"DataFrame形状: {df.shape}")

if __name__ == "__main__":
    debug_export()

