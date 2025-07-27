#!/usr/bin/env python3
"""
简单的ASR测试脚本
测试前端录音格式与百度云ASR的兼容性
"""

import requests
import os
from baidu_speech_api import BaiduSpeechAPI

def test_baidu_asr_with_different_formats():
    """测试百度云ASR对不同格式的支持"""
    print("🧪 测试百度云ASR格式兼容性")
    
    # 初始化百度云API
    api_key = os.getenv('BAIDU_API_KEY', 'oOynRSSJJx0HReZxWpghwfdh')
    secret_key = os.getenv('BAIDU_SECRET_KEY', 'syqCl5ME2ZlkUJLUHRkJZQGCepH4QNa4')
    
    speech_api = BaiduSpeechAPI(api_key, secret_key)
    
    # 查找现有的音频文件
    audio_files = []
    for ext in ['wav', 'mp3', 'webm', 'ogg']:
        files = [f for f in os.listdir('.') if f.endswith(f'.{ext}')]
        audio_files.extend([(f, ext) for f in files])
    
    if not audio_files:
        print("❌ 没有找到音频文件进行测试")
        return
    
    print(f"📁 找到 {len(audio_files)} 个音频文件")
    
    for filename, format_type in audio_files[:3]:  # 只测试前3个文件
        print(f"\n🎤 测试文件: {filename} (格式: {format_type})")
        
        try:
            with open(filename, 'rb') as f:
                audio_data = f.read()
            
            print(f"📊 文件大小: {len(audio_data)} bytes")
            
            # 测试ASR识别
            result = speech_api.asr(audio_data, format_type, 16000)
            
            if result.get('err_no') == 0:
                recognized_text = ''.join(result.get('result', []))
                print(f"✅ 识别成功: {recognized_text}")
            else:
                print(f"❌ 识别失败: 错误码 {result.get('err_no')}, {result.get('err_msg', '未知错误')}")
                
        except Exception as e:
            print(f"❌ 处理异常: {e}")

def test_frontend_recording_simulation():
    """模拟前端录音格式测试"""
    print("\n🎭 模拟前端录音格式测试")
    
    # 查找WebM格式的文件（前端常用格式）
    webm_files = [f for f in os.listdir('.') if f.endswith('.webm')]
    
    if not webm_files:
        print("⚠️ 没有找到WebM格式文件，无法模拟前端录音测试")
        return
    
    webm_file = webm_files[0]
    print(f"📁 使用文件: {webm_file}")
    
    # 模拟前端发送请求
    try:
        with open(webm_file, 'rb') as f:
            files = {'audio_file': (webm_file, f, 'audio/webm')}
            
            print("📤 发送ASR请求到后端...")
            response = requests.post(
                'http://127.0.0.1:8000/asr',
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 后端ASR成功: {result}")
            else:
                print(f"❌ 后端ASR失败: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def main():
    print("=" * 80)
    print("🔍 ASR格式兼容性测试")
    print("=" * 80)
    
    # 测试1: 直接测试百度云ASR
    test_baidu_asr_with_different_formats()
    
    # 测试2: 模拟前端录音
    test_frontend_recording_simulation()
    
    print("\n" + "=" * 80)
    print("📋 测试建议:")
    print("1. 如果WebM格式识别失败，需要音频格式转换")
    print("2. 如果WAV格式正常，建议前端直接录制WAV")
    print("3. 检查音频采样率是否为16kHz")
    print("=" * 80)

if __name__ == "__main__":
    main()
