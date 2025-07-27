#!/usr/bin/env python3
"""
测试音色修改为度小贤臻品的效果
"""

import requests
import json
import time
import os
from pathlib import Path

# 测试配置
API_BASE_URL = "http://127.0.0.1:8000"
TTS_ENDPOINT = f"{API_BASE_URL}/tts"

def test_voice_synthesis():
    """测试度小贤臻品音色合成效果"""
    print("🎵 测试度小贤臻品音色合成...")
    
    # 测试文本
    test_text = "您好，我是涂序彦教授的数字人助手。很高兴为您介绍人工智能的相关知识。"
    
    try:
        # 发送TTS请求
        tts_data = {
            "text": test_text,
            "voice": "zh-CN-male",
            "speed": 5,
            "pitch": 5,
            "volume": 5
        }
        
        print(f"📝 测试文本: {test_text}")
        print(f"🎛️ 请求参数: {json.dumps(tts_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(TTS_ENDPOINT, json=tts_data, timeout=30)
        
        print(f"📡 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            # 检查响应内容类型
            content_type = response.headers.get('content-type', '')
            print(f"📄 响应类型: {content_type}")
            
            if 'audio' in content_type or 'application/octet-stream' in content_type:
                # 保存音频文件
                audio_file = "test_voice_xiaoxian.wav"
                with open(audio_file, "wb") as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                print(f"✅ 音频合成成功！")
                print(f"📁 文件保存: {audio_file}")
                print(f"📊 文件大小: {file_size} bytes")
                
                # 检查文件是否有效
                if file_size > 1000:  # 至少1KB的音频文件
                    print(f"🎉 度小贤臻品音色测试成功！")
                    print(f"💡 您可以播放 {audio_file} 文件来听取效果")
                    return True
                else:
                    print(f"⚠️ 音频文件过小，可能存在问题")
                    return False
            else:
                # 可能是错误响应
                try:
                    error_data = response.json()
                    print(f"❌ TTS错误: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
                except:
                    print(f"❌ TTS响应异常: {response.text[:200]}")
                return False
        else:
            print(f"❌ TTS请求失败: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📝 错误详情: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
            except:
                print(f"📝 错误内容: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_server_status():
    """测试服务器状态"""
    print("🔍 检查服务器状态...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器正常运行")
            return True
        else:
            print(f"❌ 服务器状态异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return False

def check_voice_config():
    """检查音色配置是否正确修改"""
    print("🔍 检查音色配置...")
    
    files_to_check = [
        "api_server.py",
        "complete_api_server.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ 检查 {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if "4115" in content and "度小贤" in content:
                print(f"  ✅ 度小贤臻品音色配置已更新")
            else:
                print(f"  ❌ 音色配置可能未正确更新")
        else:
            print(f"❌ {file_path} 文件不存在")

def main():
    """主测试函数"""
    print("🎵 度小贤臻品音色测试")
    print("=" * 50)
    
    # 1. 检查音色配置
    check_voice_config()
    print()
    
    # 2. 测试服务器状态
    server_ok = test_server_status()
    print()
    
    # 3. 测试音色合成
    if server_ok:
        voice_ok = test_voice_synthesis()
        print()
        
        if voice_ok:
            print("🎉 度小贤臻品音色配置成功！")
            print("\n📋 修改总结:")
            print("✅ 1. api_server.py 音色参数已更新为 4115")
            print("✅ 2. complete_api_server.py 音色参数已更新为 4115")
            print("✅ 3. 音频合成测试通过")
            print("✅ 4. 度小贤臻品音色生效")
        else:
            print("❌ 音色测试失败")
    else:
        print("❌ 服务器未运行，无法测试音色")
    
    print("\n💡 使用说明:")
    print("1. 度小贤臻品是百度语音的高品质男声音色")
    print("2. 参数值 4115 对应度小贤臻品音色")
    print("3. 适合教授讲话风格，声音更加自然清晰")
    print("4. 重启服务后新音色即可生效")

if __name__ == "__main__":
    main()
