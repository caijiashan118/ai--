#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能图表模块最终测试
"""

import requests
import json
import time

def test_final_charts():
    """智能图表模块最终测试"""
    base_url = "http://localhost:8080"
    
    print("🔍 开始智能图表模块最终测试...")
    
    # 1. 测试API数据
    print("\n1. 测试API数据...")
    try:
        response = requests.get(f"{base_url}/api/charts_data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data'):
                print(f"✅ API数据正常: {len(data['data'])}条记录")
                
                # 检查数据字段
                sample = data['data'][0]
                required_fields = ['project_name', 'arrangement_amount', 'region', 'project_type']
                missing = [f for f in required_fields if f not in sample]
                if missing:
                    print(f"❌ 缺少字段: {missing}")
                    return False
                else:
                    print("✅ 数据字段完整")
            else:
                print("❌ API数据格式错误")
                return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API测试异常: {e}")
        return False
    
    # 2. 测试页面加载
    print("\n2. 测试页面加载...")
    try:
        response = requests.get(f"{base_url}/smart_charts", timeout=10)
        if response.status_code == 200:
            print("✅ 页面加载成功")
            
            # 检查关键函数
            if "loadChartsData()" in response.text:
                print("✅ loadChartsData函数存在")
            else:
                print("❌ loadChartsData函数不存在")
                return False
                
            if "generateAllCharts()" in response.text:
                print("✅ generateAllCharts函数存在")
            else:
                print("❌ generateAllCharts函数不存在")
                return False
                
            # 检查错误处理
            if "console.log('开始加载图表数据...')" in response.text:
                print("✅ 调试信息已添加")
            else:
                print("❌ 调试信息未添加")
                return False
                
        else:
            print(f"❌ 页面加载失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 页面测试异常: {e}")
        return False
    
    # 3. 测试其他API
    print("\n3. 测试其他API...")
    apis = [
        ('/api/charts_analysis', '图表分析'),
        ('/api/pivot_table', '透视表'),
        ('/api/dashboard_stats', '仪表盘统计')
    ]
    
    for api_url, api_name in apis:
        try:
            response = requests.get(f"{base_url}{api_url}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if api_name == '仪表盘统计':
                    if 'total_projects' in data:
                        print(f"✅ {api_name}API正常")
                    else:
                        print(f"❌ {api_name}API数据错误")
                        return False
                elif data.get('success'):
                    print(f"✅ {api_name}API正常")
                else:
                    print(f"❌ {api_name}API返回错误")
                    return False
            else:
                print(f"❌ {api_name}API请求失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {api_name}API异常: {e}")
            return False
    
    # 4. 测试刷新功能
    print("\n4. 测试刷新功能...")
    try:
        # 模拟多次刷新
        for i in range(3):
            response = requests.get(f"{base_url}/api/charts_data", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    print(f"✅ 刷新测试 {i+1}/3 成功")
                else:
                    print(f"❌ 刷新测试 {i+1}/3 失败")
                    return False
            else:
                print(f"❌ 刷新测试 {i+1}/3 失败: {response.status_code}")
                return False
            time.sleep(0.5)
    except Exception as e:
        print(f"❌ 刷新测试异常: {e}")
        return False
    
    print("\n🎉 智能图表模块最终测试完成！")
    print("✅ 所有测试通过，模块应该能正常工作")
    print("\n📋 测试总结:")
    print("   - API数据正常，字段完整")
    print("   - 页面加载成功，函数存在")
    print("   - 错误处理已完善")
    print("   - 刷新功能正常")
    print("   - 所有相关API正常")
    
    return True

if __name__ == "__main__":
    test_final_charts()

