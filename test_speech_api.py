#!/usr/bin/env python3
"""
语音API测试脚本
测试ASR和TTS端点的功能
"""

import requests
import json
import time
import os

# API基础URL
BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_speech_status():
    """测试语音服务状态"""
    print("\n🔍 测试语音服务状态...")
    try:
        response = requests.get(f"{BASE_URL}/speech_status")
        if response.status_code == 200:
            data = response.json()
            print("✅ 语音服务状态:")
            print(f"   - ASR可用: {data.get('asr_enabled', False)}")
            print(f"   - TTS可用: {data.get('tts_enabled', False)}")
            print(f"   - 消息: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ 语音服务状态检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 语音服务状态检查异常: {e}")
        return False

def test_tts():
    """测试TTS端点"""
    print("\n🔍 测试TTS端点...")
    try:
        # 测试数据
        test_data = {
            "text": "你好，我是涂序彦教授。很高兴与您交流人工智能相关的话题。",
            "voice": "zh-CN-male",
            "speed": 5,
            "pitch": 5,
            "volume": 5
        }
        
        print(f"📝 发送TTS请求: {test_data['text'][:30]}...")
        
        response = requests.post(
            f"{BASE_URL}/tts",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            # 检查响应头
            content_type = response.headers.get('content-type', '')
            if 'audio' in content_type:
                audio_size = len(response.content)
                print(f"✅ TTS成功，音频大小: {audio_size} bytes")
                
                # 保存音频文件用于测试
                with open('test_tts_output.wav', 'wb') as f:
                    f.write(response.content)
                print("💾 音频已保存为 test_tts_output.wav")
                return True
            else:
                print(f"❌ TTS返回了非音频内容: {content_type}")
                return False
        else:
            print(f"❌ TTS请求失败: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误详情: {error_data}")
            except:
                print(f"   响应内容: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ TTS测试异常: {e}")
        return False

def test_asr():
    """测试ASR端点"""
    print("\n🔍 测试ASR端点...")
    try:
        # 创建一个模拟音频文件
        mock_audio_data = b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x80\x3e\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'
        mock_audio_data += b'\x00' * 1024  # 添加一些音频数据
        
        # 保存为临时文件
        with open('test_audio.wav', 'wb') as f:
            f.write(mock_audio_data)
        
        print("📝 发送ASR请求...")
        
        # 发送文件
        with open('test_audio.wav', 'rb') as f:
            files = {'audio_file': ('test_audio.wav', f, 'audio/wav')}
            response = requests.post(
                f"{BASE_URL}/asr",
                files=files,
                timeout=30
            )
        
        # 清理临时文件
        if os.path.exists('test_audio.wav'):
            os.remove('test_audio.wav')
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success', False):
                print(f"✅ ASR成功: {data.get('text', 'N/A')}")
                print(f"   置信度: {data.get('confidence', 0):.2f}")
                return True
            else:
                print(f"❌ ASR失败: {data.get('message', 'N/A')}")
                return False
        else:
            print(f"❌ ASR请求失败: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误详情: {error_data}")
            except:
                print(f"   响应内容: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ ASR测试异常: {e}")
        return False

def test_ai_chat():
    """测试AI聊天端点"""
    print("\n🔍 测试AI聊天端点...")
    try:
        test_data = {
            "prompt": "请简单介绍一下您自己"
        }
        
        print(f"📝 发送聊天请求: {test_data['prompt']}")
        
        response = requests.post(
            f"{BASE_URL}/ask_professor",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            print(f"✅ AI聊天成功: {answer[:100]}...")
            return True
        else:
            print(f"❌ AI聊天失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI聊天测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🎯 涂序彦教授数字人 - 语音API测试")
    print("=" * 60)
    
    # 测试结果统计
    results = []
    
    # 执行测试
    results.append(("健康检查", test_health_check()))
    results.append(("语音服务状态", test_speech_status()))
    results.append(("TTS端点", test_tts()))
    results.append(("ASR端点", test_asr()))
    results.append(("AI聊天端点", test_ai_chat()))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<15} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！语音API功能正常。")
    else:
        print("⚠️  部分测试失败，请检查服务器状态和配置。")
    
    print("\n💡 提示:")
    print("- 确保后端服务器运行在 http://127.0.0.1:8000")
    print("- 如果使用模拟端点，ASR和TTS会返回模拟数据")
    print("- 生成的音频文件: test_tts_output.wav")

if __name__ == "__main__":
    main()
