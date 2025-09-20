#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据透视表功能
"""

import requests
import json

def test_pivot_table():
    """测试数据透视表功能"""
    print("=== 测试数据透视表功能 ===")
    
    base_url = "http://localhost:8080"
    
    # 测试透视表API
    print("\n1. 测试透视表API...")
    try:
        response = requests.get(f"{base_url}/api/pivot_table")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                available_fields = data['data']['available_fields']
                
                print(f"✓ 透视表API调用成功")
                print(f"可用字段总数: {len(available_fields)}")
                
                # 检查关键字段是否存在
                field_names = [field['title'] for field in available_fields]
                key_fields = ['项目名称', '项目编码（可研）', '建设单位', '项目主管部门']
                
                print("\n关键字段检查:")
                for field in key_fields:
                    if field in field_names:
                        print(f"✓ {field}: 存在")
                    else:
                        print(f"✗ {field}: 缺失")
                
                # 显示前10个字段
                print(f"\n前10个字段:")
                for i, field in enumerate(available_fields[:10], 1):
                    print(f"  {i:2d}. {field['title']} ({field['key']}) - {field['type']}")
                
            else:
                print(f"✗ API返回错误: {data.get('message', '未知错误')}")
        else:
            print(f"✗ HTTP请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
    
    # 测试透视表数据生成
    print("\n2. 测试透视表数据生成...")
    try:
        # 测试按区域分组
        response = requests.get(f"{base_url}/api/pivot_table?group_by=region&value_field=arrangement_amount&agg_func=sum")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                pivot_data = data['data']['pivot_data']
                print(f"✓ 透视表数据生成成功")
                print(f"分组数量: {len(pivot_data)}")
                
                # 显示前5个分组结果
                print(f"\n前5个分组结果:")
                for i, item in enumerate(pivot_data[:5], 1):
                    print(f"  {i}. {item['group']}: {item['value']:,.2f}万元")
                
            else:
                print(f"✗ 数据生成失败: {data.get('message', '未知错误')}")
        else:
            print(f"✗ HTTP请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")

if __name__ == "__main__":
    test_pivot_table()

