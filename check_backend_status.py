#!/usr/bin/env python3
"""
检查后端状态并测试功能
"""

import requests
import time
import json

def check_backend_health():
    """检查后端健康状态"""
    print("🔍 检查后端健康状态...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 后端服务正常运行")
            print(f"   服务器版本: {data.get('version', '未知')}")
            print(f"   服务器类型: {data.get('server_type', '未知')}")
            print(f"   可用功能: {data.get('features', [])}")
            print(f"   时间戳: {data.get('timestamp', '未知')}")
            return True
        else:
            print(f"❌ 后端服务异常，状态码: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务（连接被拒绝）")
        return False
    except requests.exceptions.Timeout:
        print("❌ 后端服务响应超时")
        return False
    except Exception as e:
        print(f"❌ 检查后端时出现异常: {e}")
        return False

def check_api_endpoints():
    """检查API端点"""
    print("\n🧪 检查API端点...")
    
    endpoints = [
        ("/", "健康检查"),
        ("/api_status", "API状态"),
        ("/speech_status", "语音状态")
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://127.0.0.1:8000{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description} ({endpoint}): 正常")
                results[endpoint] = True
            else:
                print(f"❌ {description} ({endpoint}): 状态码 {response.status_code}")
                results[endpoint] = False
                
        except Exception as e:
            print(f"❌ {description} ({endpoint}): 异常 {e}")
            results[endpoint] = False
    
    return results

def test_chat_function():
    """测试聊天功能"""
    print("\n💬 测试聊天功能...")
    
    try:
        test_message = "你好，这是后端测试"
        
        response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": test_message},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天功能正常")
            print(f"   测试消息: {test_message}")
            print(f"   AI回复: {result.get('answer', '无回复')[:100]}...")
            print(f"   回复来源: {result.get('source', '未知')}")
            print(f"   响应时间: {result.get('thinking_time', 0):.2f}秒")
            return True
        elif response.status_code == 422:
            print("❌ 聊天功能422错误（数据格式问题）")
            print(f"   错误详情: {response.text}")
            return False
        else:
            print(f"❌ 聊天功能异常，状态码: {response.status_code}")
            print(f"   错误详情: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天功能测试失败: {e}")
        return False

def test_speech_function():
    """测试语音功能"""
    print("\n🎤 测试语音功能...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/speech_status", timeout=10)
        
        if response.status_code == 200:
            status = response.json()
            print("✅ 语音状态端点正常")
            print(f"   百度语音可用: {'✅' if status.get('baidu_speech_available') else '❌'}")
            print(f"   ASR启用: {'✅' if status.get('asr_enabled') else '❌'}")
            print(f"   TTS启用: {'✅' if status.get('tts_enabled') else '❌'}")
            print(f"   状态信息: {status.get('message', '无信息')}")
            
            return status.get('baidu_speech_available', False)
        else:
            print(f"❌ 语音状态异常，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 语音功能测试失败: {e}")
        return False

def show_startup_guide():
    """显示启动指南"""
    print("\n📋 后端启动指南:")
    print("=" * 50)
    
    print("\n🚀 启动命令:")
    print("   方法1: python3 complete_api_server.py")
    print("   方法2: uvicorn complete_api_server:app --host 0.0.0.0 --port 8000")
    
    print("\n🔍 检查命令:")
    print("   curl http://127.0.0.1:8000/")
    print("   python3 check_backend_status.py")
    
    print("\n🛠️ 故障排除:")
    print("   1. 检查端口8000是否被占用: lsof -i :8000")
    print("   2. 检查Python依赖: pip list | grep fastapi")
    print("   3. 检查API密钥配置")
    print("   4. 查看详细错误日志")
    
    print("\n🛑 停止服务:")
    print("   pkill -f uvicorn")
    print("   pkill -f complete_api_server")

def main():
    """主函数"""
    print("🔧 后端状态检查工具")
    print("=" * 50)
    
    # 1. 检查后端健康状态
    backend_healthy = check_backend_health()
    
    if not backend_healthy:
        print("\n❌ 后端服务未正常运行")
        show_startup_guide()
        return False
    
    # 2. 检查API端点
    endpoint_results = check_api_endpoints()
    
    # 3. 测试聊天功能
    chat_ok = test_chat_function()
    
    # 4. 测试语音功能
    speech_ok = test_speech_function()
    
    # 5. 显示总结
    print("\n" + "=" * 50)
    print("📊 后端功能测试总结")
    print("=" * 50)
    
    total_tests = 4
    passed_tests = sum([
        backend_healthy,
        all(endpoint_results.values()),
        chat_ok,
        speech_ok
    ])
    
    print(f"   后端健康: {'✅' if backend_healthy else '❌'}")
    print(f"   API端点: {'✅' if all(endpoint_results.values()) else '❌'}")
    print(f"   聊天功能: {'✅' if chat_ok else '❌'}")
    print(f"   语音功能: {'✅' if speech_ok else '❌'}")
    
    print(f"\n📈 测试结果: {passed_tests}/{total_tests} 项通过")
    
    if passed_tests == total_tests:
        print("🎉 后端完全正常！所有功能都可用")
        print("\n🌐 服务地址:")
        print("   后端API: http://127.0.0.1:8000")
        print("   API文档: http://127.0.0.1:8000/docs")
        print("   语音状态: http://127.0.0.1:8000/speech_status")
        return True
    elif backend_healthy:
        print("⚠️  后端基本正常，部分功能可能有问题")
        return True
    else:
        print("❌ 后端存在严重问题")
        show_startup_guide()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
