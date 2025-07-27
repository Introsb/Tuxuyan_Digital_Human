#!/usr/bin/env python3
"""
简单的后端测试
"""

import requests
import json

def test_backend():
    """测试后端"""
    print("🧪 简单后端测试")
    print("=" * 30)
    
    try:
        # 测试健康检查
        print("1. 测试健康检查...")
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功")
            print(f"   版本: {data.get('version')}")
            print(f"   功能: {data.get('features')}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
        
        # 测试聊天功能
        print("\n2. 测试聊天功能...")
        chat_response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": "你好"},
            timeout=20
        )
        
        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            print(f"✅ 聊天功能成功")
            print(f"   回复: {chat_data.get('answer', '')[:50]}...")
        else:
            print(f"❌ 聊天功能失败: {chat_response.status_code}")
            print(f"   错误: {chat_response.text}")
        
        print("\n🎉 后端测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_backend()
