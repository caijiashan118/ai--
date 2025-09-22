#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试页面加载脚本
"""

import requests
import re

def test_page_load():
    """测试页面加载"""
    base_url = "http://localhost:8082"
    
    print("🔍 测试页面加载...")
    
    # 测试基础数据页面
    try:
        response = requests.get(f"{base_url}/basic_data")
        if response.status_code == 200:
            print("✅ 基础数据页面加载成功")
            
            # 检查是否包含修改后的代码
            if 'fetch(\'/api/project_info_page\')' in response.text:
                print("✅ 页面包含修改后的分页API调用")
            else:
                print("❌ 页面不包含修改后的分页API调用")
                
            if 'console.log(\'开始加载项目信息，使用分页API...\')' in response.text:
                print("✅ 页面包含调试日志代码")
            else:
                print("❌ 页面不包含调试日志代码")
                
        else:
            print(f"❌ 基础数据页面加载失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 测试API端点
    print("\n🔍 测试API端点...")
    
    apis = [
        ('/api/project_info', '旧API'),
        ('/api/project_info_page', '新分页API'),
        ('/api/funding_arrangement', '旧资金API'),
        ('/api/funding_arrangement_page', '新资金分页API')
    ]
    
    for api, name in apis:
        try:
            response = requests.get(f"{base_url}{api}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ {name}: {len(data)} 条记录")
                elif isinstance(data, dict) and 'data' in data:
                    print(f"✅ {name}: {len(data['data'])} 条记录")
                else:
                    print(f"✅ {name}: 响应格式异常")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: 错误 - {e}")

if __name__ == "__main__":
    test_page_load()
