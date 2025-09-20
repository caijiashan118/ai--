#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能图表模块数据测试脚本
"""

import requests
import json
import time

def test_smart_charts():
    """测试智能图表模块数据加载"""
    base_url = "http://localhost:8080"
    
    print("🔍 开始测试智能图表模块数据加载...")
    
    # 1. 测试图表数据API
    print("\n1. 测试图表数据API...")
    try:
        response = requests.get(f"{base_url}/api/charts_data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 图表数据API正常，共{data.get('total', 0)}条记录")
                print(f"   数据示例: {data['data'][0]['project_name'] if data['data'] else '无数据'}")
            else:
                print(f"❌ 图表数据API返回错误: {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ 图表数据API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 图表数据API请求异常: {e}")
        return False
    
    # 2. 测试项目信息API
    print("\n2. 测试项目信息API...")
    try:
        response = requests.get(f"{base_url}/api/project_info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 项目信息API正常，共{len(data)}条记录")
        else:
            print(f"❌ 项目信息API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 项目信息API请求异常: {e}")
        return False
    
    # 3. 测试项目总表API
    print("\n3. 测试项目总表API...")
    try:
        response = requests.get(f"{base_url}/api/project_summary", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 项目总表API正常，共{len(data)}条记录")
        else:
            print(f"❌ 项目总表API请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 项目总表API请求异常: {e}")
        return False
    
    # 4. 测试智能图表页面加载
    print("\n4. 测试智能图表页面加载...")
    try:
        response = requests.get(f"{base_url}/smart_charts", timeout=10)
        if response.status_code == 200:
            print("✅ 智能图表页面加载成功")
            if "数据概览" in response.text:
                print("✅ 数据概览模块存在")
            if "深度分析" in response.text:
                print("✅ 深度分析模块存在")
            if "Plotly" in response.text:
                print("✅ Plotly图表库已加载")
        else:
            print(f"❌ 智能图表页面加载失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 智能图表页面加载异常: {e}")
        return False
    
    print("\n🎉 智能图表模块数据测试完成！")
    return True

if __name__ == "__main__":
    test_smart_charts()

