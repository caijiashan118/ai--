#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能图表模块加载过程模拟测试
"""

import requests
import json
import time

def simulate_charts_loading():
    """模拟智能图表模块的完整加载过程"""
    base_url = "http://localhost:8080"
    
    print("🔍 开始模拟智能图表模块加载过程...")
    
    # 1. 模拟页面加载
    print("\n1. 模拟页面加载...")
    try:
        response = requests.get(f"{base_url}/smart_charts", timeout=10)
        if response.status_code == 200:
            print("✅ 智能图表页面加载成功")
            
            # 检查关键元素是否存在
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
                
        else:
            print(f"❌ 页面加载失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 页面加载异常: {e}")
        return False
    
    # 2. 模拟API调用（模拟loadChartsData函数）
    print("\n2. 模拟API调用...")
    try:
        response = requests.get(f"{base_url}/api/charts_data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API调用成功，状态码: {response.status_code}")
            
            # 模拟前端的数据处理逻辑
            if data.get('success') and data.get('data'):
                chartsData = data['data']
                pivotData = data['data']
                print(f"✅ 数据解析成功: {len(chartsData)}条记录")
                
                # 检查数据字段
                if chartsData:
                    sample_item = chartsData[0]
                    required_fields = ['project_name', 'arrangement_amount', 'region', 'project_type']
                    missing_fields = [field for field in required_fields if field not in sample_item]
                    
                    if missing_fields:
                        print(f"❌ 缺少必要字段: {missing_fields}")
                        return False
                    else:
                        print("✅ 数据字段完整")
                        
                        # 模拟图表生成前的数据统计
                        status_counts = {}
                        for item in chartsData:
                            status = item.get('project_status', '未知')
                            status_counts[status] = status_counts.get(status, 0) + 1
                        
                        print(f"✅ 数据统计完成: {len(status_counts)}种项目状态")
                        print(f"   状态分布: {status_counts}")
                        
                        return True
                else:
                    print("❌ 数据为空")
                    return False
            else:
                print(f"❌ API数据格式错误: success={data.get('success')}, hasData={bool(data.get('data'))}")
                return False
        else:
            print(f"❌ API调用失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API调用异常: {e}")
        return False
    
    # 3. 模拟刷新数据功能
    print("\n3. 模拟刷新数据功能...")
    try:
        # 模拟多次API调用（模拟用户点击刷新按钮）
        for i in range(3):
            response = requests.get(f"{base_url}/api/charts_data", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    print(f"✅ 刷新测试 {i+1}/3 成功: {len(data['data'])}条记录")
                else:
                    print(f"❌ 刷新测试 {i+1}/3 失败: 数据格式错误")
                    return False
            else:
                print(f"❌ 刷新测试 {i+1}/3 失败: HTTP {response.status_code}")
                return False
            time.sleep(0.5)  # 模拟用户操作间隔
    except Exception as e:
        print(f"❌ 刷新测试异常: {e}")
        return False
    
    # 4. 测试其他相关API
    print("\n4. 测试其他相关API...")
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
                if api_name == '仪表盘统计API':
                    if 'total_projects' in data:
                        print(f"✅ {api_name} 正常")
                    else:
                        print(f"❌ {api_name} 数据格式错误")
                        return False
                elif data.get('success'):
                    print(f"✅ {api_name} 正常")
                else:
                    print(f"❌ {api_name} 返回错误")
                    return False
            else:
                print(f"❌ {api_name} 请求失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {api_name} 请求异常: {e}")
            return False
    
    print("\n🎉 智能图表模块加载过程模拟完成！")
    print("✅ 所有测试通过，模块应该能正常工作")
    return True

if __name__ == "__main__":
    simulate_charts_loading()

