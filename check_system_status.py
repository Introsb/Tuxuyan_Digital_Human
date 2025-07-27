#!/usr/bin/env python3
"""
系统状态检查脚本
验证前后端服务是否正常运行
"""

import requests
import time
import webbrowser

def print_banner():
    """显示检查横幅"""
    print("=" * 80)
    print("🔍 涂序彦教授数字人项目 - 系统状态检查")
    print("=" * 80)

def check_backend_status():
    """检查后端状态"""
    print("\n🔧 检查后端状态...")
    
    try:
        # 检查健康状态
        response = requests.get("http://127.0.0.1:8000/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 后端服务正常")
            print(f"   服务器版本: {data.get('version', '未知')}")
            print(f"   服务器类型: {data.get('server_type', '未知')}")
            print(f"   可用功能: {data.get('features', [])}")
            
            # 检查API状态
            api_response = requests.get("http://127.0.0.1:8000/api_status", timeout=10)
            if api_response.status_code == 200:
                api_data = api_response.json()
                print(f"   DeepSeek可用: {'✅' if api_data.get('deepseek_available') else '❌'}")
                print(f"   聊天启用: {'✅' if api_data.get('chat_enabled') else '❌'}")
                print(f"   语音可用: {'✅' if api_data.get('speech_available') else '❌'}")
            
            return True
        else:
            print(f"❌ 后端服务异常，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 后端服务无法访问: {e}")
        return False

def check_frontend_status():
    """检查前端状态"""
    print("\n🌐 检查前端状态...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        
        if response.status_code == 200:
            print("✅ 前端服务正常")
            print(f"   页面大小: {len(response.content)} bytes")
            print(f"   内容类型: {response.headers.get('content-type', '未知')}")
            return True
        else:
            print(f"❌ 前端服务异常，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 前端服务无法访问: {e}")
        return False

def test_chat_function():
    """测试聊天功能"""
    print("\n💬 测试聊天功能...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": "你好，请简单回复一下"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天功能正常")
            print(f"📝 回复内容: {result.get('answer', '无回复')[:80]}...")
            print(f"🤖 回复来源: {result.get('source', '未知')}")
            print(f"⏱️  响应时间: {result.get('thinking_time', 0):.2f}秒")
            return True
        else:
            print(f"❌ 聊天功能异常，状态码: {response.status_code}")
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

def test_tts_function():
    """测试TTS功能"""
    print("\n🔊 测试TTS功能...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/tts",
            json={
                "text": "系统状态检查完成",
                "voice": "zh-CN-male",
                "speed": 5,
                "pitch": 6,
                "volume": 5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"✅ TTS功能正常，音频大小: {len(audio_data)} bytes")
            return True
        else:
            print(f"❌ TTS功能异常，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ TTS功能测试失败: {e}")
        return False

def show_system_summary(backend_ok, frontend_ok, chat_ok, speech_ok, tts_ok):
    """显示系统总结"""
    print("\n" + "=" * 80)
    print("📊 系统状态总结")
    print("=" * 80)
    
    services = {
        "后端API服务": backend_ok,
        "前端React应用": frontend_ok,
        "聊天功能": chat_ok,
        "语音状态": speech_ok,
        "TTS功能": tts_ok
    }
    
    for service_name, status in services.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"   {service_name}: {status_text}")
    
    total_passed = sum(services.values())
    total_services = len(services)
    
    print(f"\n📈 总体状态: {total_passed}/{total_services} 项服务正常")
    
    if total_passed == total_services:
        print("🎉 系统完全正常！所有功能都可以使用")
        status_level = "完美"
    elif total_passed >= 4:
        print("✅ 系统基本正常，个别功能可能需要调整")
        status_level = "良好"
    elif total_passed >= 2:
        print("⚠️  系统部分正常，部分功能有问题")
        status_level = "一般"
    else:
        print("❌ 系统存在严重问题")
        status_level = "异常"
    
    print(f"🏆 系统状态等级: {status_level}")
    
    print("\n🌐 服务地址:")
    print("   前端界面: http://localhost:3000")
    print("   后端API: http://127.0.0.1:8000")
    print("   API文档: http://127.0.0.1:8000/docs")
    print("   语音状态: http://127.0.0.1:8000/speech_status")
    
    print("\n💡 功能说明:")
    if chat_ok:
        print("   ✅ 可以进行文字聊天对话")
    if speech_ok:
        print("   ✅ 可以使用语音输入（ASR）")
    if tts_ok:
        print("   ✅ 可以听取语音回复（TTS）")
    
    if frontend_ok and backend_ok:
        print("\n🚀 系统已准备就绪，可以开始使用！")
        return True
    else:
        print("\n❌ 系统未完全启动，请检查服务状态")
        return False

def main():
    """主函数"""
    print_banner()
    
    # 检查各项服务
    backend_ok = check_backend_status()
    frontend_ok = check_frontend_status()
    chat_ok = test_chat_function() if backend_ok else False
    speech_ok = test_speech_function() if backend_ok else False
    tts_ok = test_tts_function() if backend_ok else False
    
    # 显示总结
    system_ready = show_system_summary(backend_ok, frontend_ok, chat_ok, speech_ok, tts_ok)
    
    # 如果系统正常，打开浏览器
    if system_ready:
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
        except:
            print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
    
    return system_ready

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
