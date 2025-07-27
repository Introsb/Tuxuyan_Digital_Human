#!/usr/bin/env python3
"""
测试百度云语音功能的脚本
包括ASR和TTS端点测试
"""

import requests
import json
import time
import os

def test_tts_endpoint():
    """测试TTS端点"""
    print("🔊 测试TTS端点...")
    
    url = "http://127.0.0.1:8000/tts"
    data = {
        "text": "你好，我是涂序彦教授，很高兴与您交流人工智能的话题。",
        "speed": 5,
        "pitch": 5,
        "volume": 5
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=data, timeout=30)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            # 保存音频文件
            with open('test_tts_endpoint.wav', 'wb') as f:
                f.write(response.content)
            
            print(f"✅ TTS测试成功")
            print(f"   - 耗时: {elapsed_time:.2f}秒")
            print(f"   - 音频大小: {len(response.content)} bytes")
            print(f"   - 文件已保存: test_tts_endpoint.wav")
            return True
        else:
            print(f"❌ TTS测试失败，状态码: {response.status_code}")
            print(f"   - 响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ TTS测试异常: {e}")
        return False

def test_asr_endpoint():
    """测试ASR端点"""
    print("\n🎤 测试ASR端点...")
    
    # 使用之前生成的音频文件
    audio_file = 'test_tts_endpoint.wav'
    if not os.path.exists(audio_file):
        print(f"❌ 音频文件不存在: {audio_file}")
        return False
    
    url = "http://127.0.0.1:8000/asr"
    
    try:
        start_time = time.time()
        with open(audio_file, 'rb') as f:
            files = {'audio_file': (audio_file, f, 'audio/wav')}
            response = requests.post(url, files=files, timeout=30)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ASR测试成功")
            print(f"   - 耗时: {elapsed_time:.2f}秒")
            print(f"   - 识别文本: {result.get('text', '')}")
            print(f"   - 置信度: {result.get('confidence', 0)}")
            print(f"   - 成功状态: {result.get('success', False)}")
            return True
        else:
            print(f"❌ ASR测试失败，状态码: {response.status_code}")
            print(f"   - 响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ASR测试异常: {e}")
        return False

def test_chat_endpoint():
    """测试聊天端点"""
    print("\n💬 测试聊天端点...")
    
    url = "http://127.0.0.1:8000/ask_professor"
    data = {
        "prompt": "请简单介绍一下人工智能的发展历程"
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=data, timeout=60)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 聊天测试成功")
            print(f"   - 耗时: {elapsed_time:.2f}秒")
            print(f"   - 回答长度: {len(result.get('answer', ''))} 字符")
            print(f"   - 来源: {result.get('source', '')}")
            print(f"   - 使用tokens: {result.get('tokens_used', 0)}")
            return True
        else:
            print(f"❌ 聊天测试失败，状态码: {response.status_code}")
            print(f"   - 响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 80)
    print("🧪 涂序彦数字人API端点测试")
    print("=" * 80)
    
    # 测试服务器连接
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器连接正常")
        else:
            print("❌ 服务器连接失败")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        return
    
    # 运行测试
    results = []
    
    # 1. 测试TTS
    results.append(("TTS", test_tts_endpoint()))
    
    # 2. 测试ASR
    results.append(("ASR", test_asr_endpoint()))
    
    # 3. 测试聊天
    results.append(("Chat", test_chat_endpoint()))
    
    # 输出测试结果
    print("\n" + "=" * 80)
    print("📊 测试结果汇总")
    print("=" * 80)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:10} : {status}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    print(f"\n总计: {passed_tests}/{total_tests} 个测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试都通过了！")
    else:
        print("⚠️ 部分测试失败，请检查日志")

if __name__ == "__main__":
    main()
