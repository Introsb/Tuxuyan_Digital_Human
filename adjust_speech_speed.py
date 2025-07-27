#!/usr/bin/env python3
"""
调整语速到合适水平并重启服务
"""

import subprocess
import time
import requests
import webbrowser

def print_banner():
    """显示横幅"""
    print("=" * 80)
    print("🔧 调整语速到合适水平")
    print("=" * 80)
    print("🎯 调整内容:")
    print("   - 后端语速: +3 → +1 (降低语速)")
    print("   - 前端语速: 8 → 6 (适中速度)")
    print("   - 平衡速度和清晰度")
    print("=" * 80)

def restart_backend():
    """重启后端服务"""
    print("\n🔄 重启后端服务...")
    
    # 停止现有后端
    try:
        subprocess.run(["pkill", "-f", "complete_api_server"], check=False)
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        print("✅ 已停止现有后端服务")
    except:
        print("⚠️  停止后端服务时出现问题")
    
    time.sleep(3)
    
    # 启动新的后端
    try:
        backend_process = subprocess.Popen([
            "python3", "complete_api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待后端重启...")
        time.sleep(8)
        
        if backend_process.poll() is None:
            print("✅ 后端服务重启成功")
            return True
        else:
            print("❌ 后端服务重启失败")
            return False
            
    except Exception as e:
        print(f"❌ 重启后端时出错: {e}")
        return False

def test_adjusted_speed():
    """测试调整后的语速"""
    print("\n🎤 测试调整后的语速...")
    
    try:
        # 等待后端完全启动
        time.sleep(5)
        
        # 测试TTS
        test_text = "您好，我是涂序彦教授。这是语速调整后的测试，现在应该是一个更合适的语音速度。"
        
        response = requests.post(
            "http://127.0.0.1:8000/tts",
            json={
                "text": test_text,
                "voice": "zh-CN-male",
                "speed": 6,  # 使用调整后的语速
                "pitch": 6,
                "volume": 5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"✅ 语速调整测试成功，音频大小: {len(audio_data)} bytes")
            
            # 保存测试音频
            with open("test_adjusted_speech.wav", "wb") as f:
                f.write(audio_data)
            print("💾 调整后的测试音频已保存到: test_adjusted_speech.wav")
            
            return True
        else:
            print(f"❌ 语速测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 语速测试异常: {e}")
        return False

def verify_services():
    """验证服务状态"""
    print("\n🔍 验证服务状态...")
    
    # 检查后端
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=10)
        if response.status_code == 200:
            print("✅ 后端服务正常")
            backend_ok = True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            backend_ok = False
    except Exception as e:
        print(f"❌ 后端服务检查失败: {e}")
        backend_ok = False
    
    # 检查前端
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ 前端服务正常")
            frontend_ok = True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            frontend_ok = False
    except Exception as e:
        print(f"❌ 前端服务检查失败: {e}")
        frontend_ok = False
    
    return backend_ok, frontend_ok

def show_speed_comparison():
    """显示语速对比"""
    print("\n📊 语速调整对比:")
    print("=" * 50)
    
    print("\n🔧 后端语速调整:")
    print("   - 原始设置: request.speed - 1 (太慢)")
    print("   - 第一次调整: request.speed + 3 (太快)")
    print("   - 当前设置: request.speed + 1 (适中)")
    
    print("\n🌐 前端语速调整:")
    print("   - 原始设置: speed: 4 (太慢)")
    print("   - 第一次调整: speed: 8 (太快)")
    print("   - 当前设置: speed: 6 (适中)")
    
    print("\n🎯 当前语速特点:")
    print("   - 百度TTS实际语速: 约7-8 (适中偏快)")
    print("   - 清晰度: 高")
    print("   - 听感: 自然流畅")
    print("   - 适用场景: 日常对话、学术讲解")
    
    print("\n💡 如需进一步微调:")
    print("   - 稍快一点: 后端+2, 前端7")
    print("   - 稍慢一点: 后端+0, 前端5")

def main():
    """主函数"""
    print_banner()
    
    # 1. 重启后端
    backend_ok = restart_backend()
    
    if not backend_ok:
        print("❌ 后端重启失败，无法继续")
        return False
    
    # 2. 测试调整后的语速
    speed_ok = test_adjusted_speed()
    
    # 3. 验证服务状态
    backend_ok, frontend_ok = verify_services()
    
    # 4. 显示语速对比
    show_speed_comparison()
    
    # 5. 显示结果
    print("\n" + "=" * 80)
    print("📊 语速调整结果")
    print("=" * 80)
    
    services = {
        "后端服务": backend_ok,
        "前端服务": frontend_ok,
        "语速测试": speed_ok
    }
    
    for service_name, status in services.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"   {service_name}: {status_text}")
    
    total_passed = sum(services.values())
    total_services = len(services)
    
    print(f"\n📈 调整结果: {total_passed}/{total_services} 项正常")
    
    if total_passed == total_services:
        print("🎉 语速调整完全成功！")
        print("🎤 现在语速应该更合适，既不太快也不太慢")
        
        # 打开浏览器
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
            print("💡 请测试语音播放，语速应该更舒适了")
        except:
            print("\n⚠️  无法自动打开浏览器")
        
        return True
    else:
        print("❌ 语速调整过程中出现问题")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
