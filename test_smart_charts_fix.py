#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能图表模块修复验证脚本
"""

import requests
import json
import time

def test_smart_charts_fix():
    """测试智能图表模块修复后的功能"""
    base_url = "http://localhost:8080"
    
    print("🔍 开始测试智能图表模块修复...")
    
    # 1. 测试API数据格式
    print("\n1. 测试API数据格式...")
    try:
        response = requests.get(f"{base_url}/api/charts_data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'data' in data:
                print(f"✅ API数据格式正确")
                print(f"   成功标志: {data.get('success')}")
                print(f"   数据条数: {len(data.get('data', []))}")
                print(f"   总条数: {data.get('total', 0)}")
                
                # 检查数据字段
                if data.get('data'):
                    sample_item = data['data'][0]
                    required_fields = ['project_name', 'arrangement_amount', 'region', 'project_type']
                    missing_fields = [field for field in required_fields if field not in sample_item]
                    if missing_fields:
                        print(f"❌ 缺少必要字段: {missing_fields}")
                        return False
                    else:
                        print(f"✅ 数据字段完整")
            else:
                print(f"❌ API数据格式错误: {data}")
                return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API请求异常: {e}")
        return False
    
    # 2. 测试智能图表页面加载
    print("\n2. 测试智能图表页面加载...")
    try:
        response = requests.get(f"{base_url}/smart_charts", timeout=10)
        if response.status_code == 200:
            print("✅ 智能图表页面加载成功")
            
            # 检查关键JavaScript函数是否存在
            if "loadChartsData()" in response.text:
                print("✅ loadChartsData函数存在")
            else:
                print("❌ loadChartsData函数不存在")
                return False
                
            if "data.success && data.data" in response.text:
                print("✅ 数据格式检查逻辑已修复")
            else:
                print("❌ 数据格式检查逻辑未修复")
                return False
                
        else:
            print(f"❌ 智能图表页面加载失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 智能图表页面加载异常: {e}")
        return False
    
    # 3. 测试其他相关API
    print("\n3. 测试其他相关API...")
    apis = [
        ('/api/charts_analysis', '图表分析API'),
        ('/api/pivot_table', '透视表API'),
        ('/api/dashboard_stats', '仪表盘统计API')
    ]
    
    for api_url, api_name in apis:
        try:
            response = requests.get(f"{base_url}{api_url}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                # 仪表盘统计API没有success字段，直接检查是否有数据
                if api_name == '仪表盘统计API':
                    if 'total_projects' in data:
                        print(f"✅ {api_name} 正常")
                    else:
                        print(f"❌ {api_name} 数据格式错误")
                        return False
                elif data.get('success'):
                    print(f"✅ {api_name} 正常")
                else:
                    print(f"❌ {api_name} 返回错误: {data.get('message', '未知错误')}")
                    return False
            else:
                print(f"❌ {api_name} 请求失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {api_name} 请求异常: {e}")
            return False
    
    print("\n🎉 智能图表模块修复验证完成！")
    print("✅ 所有测试通过，智能图表模块现在应该能正常加载数据")
    return True

if __name__ == "__main__":
    test_smart_charts_fix()
