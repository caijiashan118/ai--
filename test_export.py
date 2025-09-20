#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Excel导出功能
"""

import requests
import os
from datetime import datetime

def test_export_function():
    """测试导出功能"""
    print("=== 测试Excel导出功能 ===")
    
    base_url = "http://localhost:8080"
    
    # 测试导出项目基本信息表
    print("\n1. 测试导出项目基本信息表...")
    try:
        response = requests.get(f"{base_url}/api/export_excel/project_info")
        
        if response.status_code == 200:
            # 检查Content-Type
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            # 检查文件大小
            file_size = len(response.content)
            print(f"文件大小: {file_size} 字节")
            
            # 保存文件进行验证
            filename = f"test_project_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ 项目基本信息表导出成功，文件保存为: {filename}")
            
            # 检查文件是否为有效的Excel文件
            if file_size > 0 and 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
                print("✓ 文件格式正确 (Excel格式)")
            else:
                print("✗ 文件格式可能不正确")
                
        else:
            print(f"✗ 导出失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
    
    # 测试导出项目资金安排表
    print("\n2. 测试导出项目资金安排表...")
    try:
        response = requests.get(f"{base_url}/api/export_excel/funding")
        
        if response.status_code == 200:
            # 检查Content-Type
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            # 检查文件大小
            file_size = len(response.content)
            print(f"文件大小: {file_size} 字节")
            
            # 保存文件进行验证
            filename = f"test_funding_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ 项目资金安排表导出成功，文件保存为: {filename}")
            
            # 检查文件是否为有效的Excel文件
            if file_size > 0 and 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
                print("✓ 文件格式正确 (Excel格式)")
            else:
                print("✗ 文件格式可能不正确")
                
        else:
            print(f"✗ 导出失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
    
    # 测试导出项目总表
    print("\n3. 测试导出项目总表...")
    try:
        response = requests.get(f"{base_url}/api/export_excel/summary")
        
        if response.status_code == 200:
            # 检查Content-Type
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            # 检查文件大小
            file_size = len(response.content)
            print(f"文件大小: {file_size} 字节")
            
            # 保存文件进行验证
            filename = f"test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ 项目总表导出成功，文件保存为: {filename}")
            
            # 检查文件是否为有效的Excel文件
            if file_size > 0 and 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
                print("✓ 文件格式正确 (Excel格式)")
            else:
                print("✗ 文件格式可能不正确")
                
        else:
            print(f"✗ 导出失败: HTTP {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")

if __name__ == "__main__":
    test_export_function()

