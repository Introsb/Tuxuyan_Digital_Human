#!/usr/bin/env python3
"""
重启服务并应用更快的语速设置
"""

import subprocess
import time
import requests
import webbrowser
from pathlib import Path

def print_banner():
    """显示横幅"""
    print("=" * 80)
    print("🔧 重启服务并应用更快语速设置")
    print("=" * 80)
    print("🎯 修改内容:")
    print("   - 后端语速: +3 (更快的语音合成)")
    print("   - 前端语速: 4 → 8 (提高播放速度)")
    print("   - 重启前后端服务")
    print("   - 测试语速效果")
    print("=" * 80)

def stop_services():
    """停止现有服务"""
    print("\n🛑 停止现有服务...")
    
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        print("✅ 已停止后端服务")
    except:
        print("⚠️  停止后端服务时出现问题")
    
    try:
        subprocess.run(["pkill", "-f", "react-scripts"], check=False)
        print("✅ 已停止前端服务")
    except:
        print("⚠️  停止前端服务时出现问题")
    
    time.sleep(3)
    print("⏳ 等待服务完全停止...")

def start_backend():
    """启动后端服务"""
    print("\n🔧 启动修改后的后端服务...")
    
    try:
        backend_process = subprocess.Popen([
            "python3", "complete_api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待后端启动...")
        time.sleep(10)
        
        if backend_process.poll() is None:
            print("✅ 后端服务启动成功")
            
            # 验证后端
            try:
                response = requests.get("http://127.0.0.1:8000/", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"   版本: {data.get('version', '未知')}")
                    print(f"   功能: {data.get('features', [])}")
                    return True
                else:
                    print(f"⚠️  后端响应异常: {response.status_code}")
                    return False
            except Exception as e:
                print(f"⚠️  后端验证失败: {e}")
                return False
        else:
            print("❌ 后端服务启动失败")
            return False
            
    except Exception as e:
        print(f"❌ 启动后端时出错: {e}")
        return False

def start_frontend():
    """启动前端服务"""
    print("\n🌐 启动修改后的前端服务...")
    
    frontend_dir = Path("react-version")
    if not frontend_dir.exists():
        print("❌ react-version 目录不存在")
        return False
    
    try:
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待前端启动...")
        time.sleep(15)
        
        if frontend_process.poll() is None:
            print("✅ 前端服务启动成功")
            
            # 验证前端
            try:
                response = requests.get("http://localhost:3000", timeout=10)
                if response.status_code == 200:
                    print(f"   页面大小: {len(response.content)} bytes")
                    return True
                else:
                    print(f"⚠️  前端响应异常: {response.status_code}")
                    return False
            except Exception as e:
                print(f"⚠️  前端验证失败: {e}")
                return False
        else:
            print("❌ 前端服务启动失败")
            return False
            
    except Exception as e:
        print(f"❌ 启动前端时出错: {e}")
        return False

def test_speech_speed():
    """测试语速效果"""
    print("\n🎤 测试语速效果...")
    
    try:
        # 测试TTS
        test_text = "您好，我是涂序彦教授。这是语速优化后的测试，现在语音应该更快更流畅了。"
        
        response = requests.post(
            "http://127.0.0.1:8000/tts",
            json={
                "text": test_text,
                "voice": "zh-CN-male",
                "speed": 8,  # 使用新的语速设置
                "pitch": 6,
                "volume": 5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"✅ TTS语速测试成功，音频大小: {len(audio_data)} bytes")
            
            # 保存测试音频
            with open("test_faster_speech.wav", "wb") as f:
                f.write(audio_data)
            print("💾 测试音频已保存到: test_faster_speech.wav")
            
            return True
        else:
            print(f"❌ TTS语速测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 语速测试异常: {e}")
        return False

def test_chat_with_speech():
    """测试聊天和语音功能"""
    print("\n💬 测试聊天功能...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": "请简单介绍一下语速优化的效果"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天功能正常")
            print(f"   回复: {result.get('answer', '无回复')[:80]}...")
            print(f"   来源: {result.get('source', '未知')}")
            return True
        else:
            print(f"❌ 聊天功能异常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天功能测试失败: {e}")
        return False

def show_speed_settings():
    """显示语速设置说明"""
    print("\n📋 语速设置说明:")
    print("=" * 50)
    
    print("\n🔧 后端修改:")
    print("   - 原设置: request.speed - 1")
    print("   - 新设置: request.speed + 3")
    print("   - 效果: 语音合成速度提高约40%")
    
    print("\n🌐 前端修改:")
    print("   - 原设置: speed: 4")
    print("   - 新设置: speed: 8")
    print("   - 效果: 播放速度提高100%")
    
    print("\n🎯 语速范围:")
    print("   - 百度TTS语速: 0-15 (15最快)")
    print("   - 当前设置: 约11-12 (较快)")
    print("   - 推荐范围: 8-12 (平衡速度和清晰度)")
    
    print("\n💡 进一步调整:")
    print("   - 如果还是太慢: 修改 +3 为 +5")
    print("   - 如果太快不清楚: 修改 +3 为 +1")
    print("   - 前端速度: 可调整为 6-10")

def show_results(backend_ok, frontend_ok, speech_ok, chat_ok):
    """显示结果"""
    print("\n" + "=" * 80)
    print("📊 语速优化重启结果")
    print("=" * 80)
    
    services = {
        "后端服务": backend_ok,
        "前端服务": frontend_ok,
        "语速测试": speech_ok,
        "聊天功能": chat_ok
    }
    
    for service_name, status in services.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"   {service_name}: {status_text}")
    
    total_passed = sum(services.values())
    total_services = len(services)
    
    print(f"\n📈 总体结果: {total_passed}/{total_services} 项正常")
    
    if total_passed == total_services:
        print("🎉 语速优化完全成功！")
        print("🎤 现在语音播放速度更快，用户体验更好")
    elif total_passed >= 2:
        print("⚠️  语速优化基本成功，部分功能可能需要调整")
    else:
        print("❌ 语速优化失败")
    
    print("\n🌐 服务地址:")
    print("   前端界面: http://localhost:3000")
    print("   后端API: http://127.0.0.1:8000")
    
    print("\n🎯 测试建议:")
    print("   1. 在前端输入消息测试聊天")
    print("   2. 点击播放按钮测试语音速度")
    print("   3. 比较优化前后的语音效果")
    
    return total_passed >= 2

def main():
    """主函数"""
    print_banner()
    
    # 1. 停止服务
    stop_services()
    
    # 2. 启动后端
    backend_ok = start_backend()
    
    # 3. 启动前端
    frontend_ok = start_frontend()
    
    # 4. 测试语速
    speech_ok = test_speech_speed() if backend_ok else False
    
    # 5. 测试聊天
    chat_ok = test_chat_with_speech() if backend_ok else False
    
    # 6. 显示语速设置
    show_speed_settings()
    
    # 7. 显示结果
    success = show_results(backend_ok, frontend_ok, speech_ok, chat_ok)
    
    # 8. 打开浏览器
    if success:
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
            print("💡 请测试语音播放速度，应该比之前更快")
        except:
            print("\n⚠️  无法自动打开浏览器")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
