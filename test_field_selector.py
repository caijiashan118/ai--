#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字段筛选器功能测试脚本
"""

import requests
import json
import time

def test_field_selector():
    """测试字段筛选器功能"""
    base_url = "http://localhost:8080"
    
    print("🔍 开始测试字段筛选器功能...")
    
    # 1. 测试基础数据页面加载
    print("\n1. 测试基础数据页面加载...")
    try:
        response = requests.get(f"{base_url}/basic_data", timeout=10)
        if response.status_code == 200:
            print("✅ 基础数据页面加载成功")
            if "字段选择器" in response.text:
                print("✅ 字段选择器HTML元素存在")
            else:
                print("❌ 字段选择器HTML元素不存在")
        else:
            print(f"❌ 基础数据页面加载失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 基础数据页面加载异常: {e}")
        return False
    
    # 2. 测试项目总表API
    print("\n2. 测试项目总表API...")
    try:
        response = requests.get(f"{base_url}/api/project_summary_page?draw=1&start=0&length=5", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 项目总表API响应成功，返回 {len(data.get('data', []))} 条记录")
            
            # 检查字段结构
            if data.get('data'):
                first_record = data['data'][0]
                print("📋 可用字段:")
                for key in sorted(first_record.keys()):
                    print(f"   - {key}")
        else:
            print(f"❌ 项目总表API失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 项目总表API异常: {e}")
        return False
    
    # 3. 测试字段筛选功能
    print("\n3. 测试字段筛选功能...")
    try:
        # 测试不同的筛选条件
        test_cases = [
            {"region": "雄县", "length": 3},
            {"project_type": "基础设施", "length": 3},
            {"funding_source": "中央财政", "length": 3},
            {"search[value]": "雄安", "length": 3}
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            params = {"draw": 1, "start": 0, "length": test_case["length"]}
            params.update({k: v for k, v in test_case.items() if k != "length"})
            
            response = requests.get(f"{base_url}/api/project_summary_page", params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 筛选测试 {i} 成功: {test_case} -> {len(data.get('data', []))} 条记录")
            else:
                print(f"❌ 筛选测试 {i} 失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 字段筛选测试异常: {e}")
    
    # 4. 测试数据导出功能
    print("\n4. 测试数据导出功能...")
    try:
        response = requests.get(f"{base_url}/api/export_excel/summary", timeout=30)
        if response.status_code == 200:
            print("✅ 数据导出功能正常")
            print(f"📁 导出文件大小: {len(response.content)} 字节")
        else:
            print(f"❌ 数据导出失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 数据导出异常: {e}")
    
    # 5. 测试数据一致性
    print("\n5. 测试数据一致性...")
    try:
        response = requests.get(f"{base_url}/api/check_data_consistency", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 数据一致性检查通过: {data.get('message')}")
            else:
                print(f"❌ 数据一致性检查失败: {data.get('message')}")
        else:
            print(f"❌ 数据一致性检查API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 数据一致性检查异常: {e}")
    
    print("\n🎉 字段筛选器功能测试完成！")
    return True

if __name__ == "__main__":
    test_field_selector()

