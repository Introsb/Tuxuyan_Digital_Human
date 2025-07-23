#!/usr/bin/env python3
"""
API连接测试脚本
用于验证后端API是否正常工作
"""

import requests
import json
import time

def test_api_connection():
    """测试API连接"""
    api_url = "http://127.0.0.1:8000/ask_professor"
    
    # 测试数据
    test_questions = [
        "您好，请简单介绍一下您自己",
        "什么是控制论？",
        "人工智能的未来发展趋势如何？"
    ]
    
    print("🔍 开始测试API连接...")
    print(f"📡 API地址: {api_url}")
    print("-" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 测试 {i}: {question}")
        
        try:
            # 发送请求
            response = requests.post(
                api_url,
                headers={"Content-Type": "application/json"},
                json={"prompt": question},
                timeout=30
            )
            
            # 检查响应状态
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "")
                print(f"✅ 成功! 响应长度: {len(answer)} 字符")
                print(f"📄 回复预览: {answer[:100]}...")
            else:
                print(f"❌ 错误! 状态码: {response.status_code}")
                print(f"📄 错误信息: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ 连接错误: 无法连接到API服务器")
            print("💡 请确保后端服务器正在运行: python3 api_server.py")
            break
        except requests.exceptions.Timeout:
            print("⏰ 超时错误: API响应时间过长")
        except Exception as e:
            print(f"❌ 未知错误: {str(e)}")
        
        # 等待一下再发送下一个请求
        if i < len(test_questions):
            time.sleep(2)
    
    print("\n" + "=" * 50)
    print("🎯 测试完成!")

def test_health_check():
    """测试健康检查端点"""
    health_url = "http://127.0.0.1:8000/"
    
    print("🏥 测试健康检查端点...")
    
    try:
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功: {data}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 健康检查错误: {str(e)}")

if __name__ == "__main__":
    print("🚀 API连接测试工具")
    print("=" * 50)
    
    # 先测试健康检查
    test_health_check()
    print()
    
    # 再测试聊天API
    test_api_connection()
