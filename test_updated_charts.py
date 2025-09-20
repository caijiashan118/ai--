#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新后的智能图表模块测试脚本
"""

import requests
import json
import time

def test_updated_charts():
    """测试更新后的智能图表模块功能"""
    base_url = "http://localhost:8080"
    
    print("🔍 开始测试更新后的智能图表模块...")
    
    # 等待应用启动
    time.sleep(3)
    
    # 1. 测试图表数据API（基于项目总表）
    print("\n1. 测试图表数据API...")
    try:
        response = requests.get(f"{base_url}/api/charts_data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 图表数据API正常，共{data.get('total', 0)}条记录")
                print(f"   数据示例: {data['data'][0]['project_name'] if data['data'] else '无数据'}")
                print(f"   字段数量: {len(data['data'][0]) if data['data'] else 0}个字段")
            else:
                print(f"❌ 图表数据API返回错误: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ 图表数据API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 图表数据API请求异常: {e}")
        return False
    
    # 2. 测试图表分析API
    print("\n2. 测试图表分析API...")
    try:
        response = requests.get(f"{base_url}/api/charts_analysis", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis_data = data['data']
                print(f"✅ 图表分析API正常")
                print(f"   项目状态分布: {len(analysis_data['status_distribution'])}种状态")
                print(f"   区域分布: {len(analysis_data['region_distribution'])}个区域")
                print(f"   项目类型分布: {len(analysis_data['type_distribution'])}种类型")
                print(f"   总投资金额: {analysis_data['total_funding']:,.2f}万元")
                print(f"   总概算金额: {analysis_data['total_budget']:,.2f}万元")
            else:
                print(f"❌ 图表分析API返回错误: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ 图表分析API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 图表分析API请求异常: {e}")
        return False
    
    # 3. 测试透视表API（默认参数）
    print("\n3. 测试透视表API（默认参数）...")
    try:
        response = requests.get(f"{base_url}/api/pivot_table", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                pivot_data = data['data']
                print(f"✅ 透视表API正常")
                print(f"   分组字段: {pivot_data['group_by_title']} ({pivot_data['group_by']})")
                print(f"   值字段: {pivot_data['value_field_title']} ({pivot_data['value_field']})")
                print(f"   聚合函数: {pivot_data['agg_func']}")
                print(f"   分组数量: {pivot_data['total_groups']}")
                print(f"   可用字段数: {len(pivot_data['available_fields'])}")
            else:
                print(f"❌ 透视表API返回错误: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ 透视表API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 透视表API请求异常: {e}")
        return False
    
    # 4. 测试透视表API（不同参数组合）
    print("\n4. 测试透视表API（不同参数组合）...")
    test_params = [
        {'group_by': 'project_type', 'value_field': 'budget_amount', 'agg_func': 'sum'},
        {'group_by': 'funding_source', 'value_field': 'arrangement_amount', 'agg_func': 'avg'},
        {'group_by': 'investment_mode', 'value_field': 'contract_amount', 'agg_func': 'count'}
    ]
    
    for i, params in enumerate(test_params):
        try:
            response = requests.get(f"{base_url}/api/pivot_table", params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    pivot_data = data['data']
                    print(f"✅ 透视表测试 {i+1} 成功: {pivot_data['group_by_title']} × {pivot_data['value_field_title']} ({pivot_data['agg_func']})")
                    print(f"   分组数量: {pivot_data['total_groups']}")
                else:
                    print(f"❌ 透视表测试 {i+1} 失败: {data.get('message', '未知错误')}")
                    return False
            else:
                print(f"❌ 透视表测试 {i+1} 请求失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 透视表测试 {i+1} 请求异常: {e}")
            return False
    
    # 5. 测试字段映射一致性
    print("\n5. 测试字段映射一致性...")
    try:
        response = requests.get(f"{base_url}/api/pivot_table", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                available_fields = data['data']['available_fields']
                print(f"✅ 字段映射正常，共{len(available_fields)}个字段")
                
                # 检查关键字段是否存在
                key_fields = ['project_name', 'arrangement_amount', 'region', 'project_type', 'funding_source']
                for field in key_fields:
                    field_info = next((f for f in available_fields if f['key'] == field), None)
                    if field_info:
                        print(f"   ✅ {field}: {field_info['title']} ({field_info['type']})")
                    else:
                        print(f"   ❌ 缺少字段: {field}")
                        return False
            else:
                print(f"❌ 字段映射检查失败: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ 字段映射检查请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 字段映射检查请求异常: {e}")
        return False
    
    print("\n🎉 更新后的智能图表模块测试完成！")
    return True

if __name__ == "__main__":
    test_updated_charts()

