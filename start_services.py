#!/usr/bin/env python3
"""
启动前后端服务
"""

import subprocess
import time
import requests
import webbrowser
from pathlib import Path

def print_banner():
    """显示启动横幅"""
    print("=" * 80)
    print("🚀 启动涂序彦教授数字人项目")
    print("=" * 80)
    print("🎯 启动服务:")
    print("   - 后端API服务器 (端口8000)")
    print("   - 前端React应用 (端口3000)")
    print("   - 验证服务状态")
    print("=" * 80)

def stop_existing_services():
    """停止现有服务"""
    print("\n🛑 停止现有服务...")
    
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        subprocess.run(["pkill", "-f", "complete_api_server"], check=False)
        print("✅ 已停止现有后端服务")
    except:
        print("ℹ️  没有运行中的后端服务")
    
    try:
        subprocess.run(["pkill", "-f", "react-scripts"], check=False)
        print("✅ 已停止现有前端服务")
    except:
        print("ℹ️  没有运行中的前端服务")
    
    time.sleep(3)

def start_backend():
    """启动后端服务"""
    print("\n🔧 启动后端API服务器...")
    
    try:
        # 使用uvicorn启动，更稳定
        backend_process = subprocess.Popen([
            "uvicorn", "complete_api_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待后端启动...")
        time.sleep(10)
        
        if backend_process.poll() is None:
            print("✅ 后端服务启动成功")
            return True, backend_process
        else:
            print("❌ 后端服务启动失败")
            stdout, stderr = backend_process.communicate()
            if stderr:
                print(f"错误信息: {stderr.decode()}")
            return False, None
            
    except Exception as e:
        print(f"❌ 启动后端时出错: {e}")
        return False, None

def start_frontend():
    """启动前端服务"""
    print("\n🌐 启动前端React应用...")
    
    frontend_dir = Path("react-version")
    if not frontend_dir.exists():
        print("❌ react-version 目录不存在")
        return False, None
    
    try:
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待前端启动...")
        time.sleep(20)
        
        if frontend_process.poll() is None:
            print("✅ 前端服务启动成功")
            return True, frontend_process
        else:
            print("❌ 前端服务启动失败")
            stdout, stderr = frontend_process.communicate()
            if stderr:
                print(f"错误信息: {stderr.decode()}")
            return False, None
            
    except Exception as e:
        print(f"❌ 启动前端时出错: {e}")
        return False, None

def verify_services():
    """验证服务状态"""
    print("\n🔍 验证服务状态...")
    
    # 检查后端
    backend_ok = False
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ 后端服务正常")
            print(f"   版本: {data.get('version', '未知')}")
            print(f"   功能: {data.get('features', [])}")
            backend_ok = True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 后端服务检查失败: {e}")
    
    # 检查前端
    frontend_ok = False
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ 前端服务正常")
            print(f"   页面大小: {len(response.content)} bytes")
            frontend_ok = True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 前端服务检查失败: {e}")
    
    return backend_ok, frontend_ok

def test_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    # 测试聊天功能
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": "你好，测试启动"},
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天功能正常")
            print(f"   回复: {result.get('answer', '无回复')[:50]}...")
            chat_ok = True
        else:
            print(f"❌ 聊天功能异常: {response.status_code}")
            chat_ok = False
    except Exception as e:
        print(f"❌ 聊天功能测试失败: {e}")
        chat_ok = False
    
    # 测试语音状态
    try:
        response = requests.get("http://127.0.0.1:8000/speech_status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("✅ 语音功能状态正常")
            print(f"   百度语音: {'✅' if status.get('baidu_speech_available') else '❌'}")
            speech_ok = status.get('baidu_speech_available', False)
        else:
            print(f"❌ 语音功能状态异常: {response.status_code}")
            speech_ok = False
    except Exception as e:
        print(f"❌ 语音功能测试失败: {e}")
        speech_ok = False
    
    return chat_ok, speech_ok

def show_results(backend_ok, frontend_ok, chat_ok, speech_ok):
    """显示启动结果"""
    print("\n" + "=" * 80)
    print("📊 服务启动结果")
    print("=" * 80)
    
    services = {
        "后端API服务": backend_ok,
        "前端React应用": frontend_ok,
        "聊天功能": chat_ok,
        "语音功能": speech_ok
    }
    
    for service_name, status in services.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"   {service_name}: {status_text}")
    
    total_passed = sum(services.values())
    total_services = len(services)
    
    print(f"\n📈 启动结果: {total_passed}/{total_services} 项正常")
    
    if total_passed == total_services:
        print("🎉 所有服务启动成功！")
        status_level = "完美"
    elif total_passed >= 3:
        print("✅ 主要服务启动成功")
        status_level = "良好"
    elif total_passed >= 2:
        print("⚠️  部分服务启动成功")
        status_level = "一般"
    else:
        print("❌ 服务启动失败")
        status_level = "失败"
    
    print(f"🏆 启动状态: {status_level}")
    
    print("\n🌐 服务地址:")
    print("   前端界面: http://localhost:3000")
    print("   后端API: http://127.0.0.1:8000")
    print("   API文档: http://127.0.0.1:8000/docs")
    
    print("\n💡 使用说明:")
    if chat_ok:
        print("   ✅ 可以进行文字聊天对话")
    if speech_ok:
        print("   ✅ 可以使用语音输入和播放")
    
    print("\n🛑 停止服务:")
    print("   pkill -f uvicorn")
    print("   pkill -f 'npm start'")
    
    return total_passed >= 2

def main():
    """主函数"""
    print_banner()
    
    # 1. 停止现有服务
    stop_existing_services()
    
    # 2. 启动后端
    backend_ok, backend_process = start_backend()
    
    # 3. 启动前端
    frontend_ok, frontend_process = start_frontend()
    
    # 4. 验证服务
    if backend_ok or frontend_ok:
        backend_verified, frontend_verified = verify_services()
        backend_ok = backend_ok and backend_verified
        frontend_ok = frontend_ok and frontend_verified
    
    # 5. 测试功能
    if backend_ok:
        chat_ok, speech_ok = test_functionality()
    else:
        chat_ok, speech_ok = False, False
    
    # 6. 显示结果
    success = show_results(backend_ok, frontend_ok, chat_ok, speech_ok)
    
    # 7. 打开浏览器
    if success:
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
        except:
            print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
