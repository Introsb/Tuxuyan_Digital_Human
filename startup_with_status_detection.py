#!/usr/bin/env python3
"""
带状态检测的系统启动脚本
"""

import subprocess
import time
import requests
import sys
import webbrowser
from pathlib import Path

def print_banner():
    """显示启动横幅"""
    print("=" * 80)
    print("🚀 涂序彦教授数字人项目 - 智能启动")
    print("=" * 80)
    print("🎯 启动流程:")
    print("   1. 停止现有服务")
    print("   2. 启动后端API服务器")
    print("   3. DeepSeek后端状态检测")
    print("   4. 启动前端React应用")
    print("   5. 系统功能验证")
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
        backend_process = subprocess.Popen([
            "uvicorn", "complete_api_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待后端启动...")
        time.sleep(10)
        
        if backend_process.poll() is None:
            print("✅ 后端API服务器启动成功")
            return True, backend_process
        else:
            print("❌ 后端API服务器启动失败")
            stdout, stderr = backend_process.communicate()
            if stderr:
                print(f"错误信息: {stderr.decode()}")
            return False, None
            
    except Exception as e:
        print(f"❌ 启动后端时出错: {e}")
        return False, None

def detect_deepseek_backend_status():
    """检测DeepSeek后端状态"""
    print("\n🔍 DeepSeek后端状态检测...")
    
    # 基础健康检查
    try:
        print("   📡 检查后端连通性...")
        health_response = requests.get("http://127.0.0.1:8000/", timeout=10)
        
        if health_response.status_code != 200:
            print(f"   ❌ 后端健康检查失败: {health_response.status_code}")
            return False, "后端服务不可用"
        
        health_data = health_response.json()
        print(f"   ✅ 后端服务正常 (v{health_data.get('version', '未知')})")
        
    except Exception as e:
        print(f"   ❌ 后端连通性检查失败: {e}")
        return False, f"连接失败: {e}"
    
    # API状态检查
    try:
        print("   🔌 检查API状态...")
        api_response = requests.get("http://127.0.0.1:8000/api_status", timeout=10)
        
        if api_response.status_code != 200:
            print(f"   ❌ API状态检查失败: {api_response.status_code}")
            return False, "API状态端点不可用"
        
        api_data = api_response.json()
        deepseek_available = api_data.get('deepseek_available', False)
        chat_enabled = api_data.get('chat_enabled', False)
        
        print(f"   📊 DeepSeek API: {'✅ 可用' if deepseek_available else '❌ 不可用'}")
        print(f"   💬 聊天功能: {'✅ 启用' if chat_enabled else '❌ 禁用'}")
        
        if not deepseek_available:
            return False, "DeepSeek API不可用"
        
        if not chat_enabled:
            return False, "聊天功能未启用"
        
    except Exception as e:
        print(f"   ❌ API状态检查失败: {e}")
        return False, f"API检查失败: {e}"
    
    # 功能测试
    try:
        print("   🧪 测试聊天功能...")
        chat_response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": "系统启动测试"},
            timeout=30
        )
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            print(f"   ✅ 聊天功能正常")
            print(f"   📝 测试回复: {result.get('answer', '无回复')[:50]}...")
            return True, "DeepSeek后端完全正常"
        else:
            print(f"   ❌ 聊天功能测试失败: {chat_response.status_code}")
            return False, f"聊天测试失败: {chat_response.status_code}"
        
    except Exception as e:
        print(f"   ❌ 聊天功能测试异常: {e}")
        return False, f"聊天测试异常: {e}"

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
            print("✅ 前端React应用启动成功")
            return True, frontend_process
        else:
            print("❌ 前端React应用启动失败")
            stdout, stderr = frontend_process.communicate()
            if stderr:
                print(f"错误信息: {stderr.decode()}")
            return False, None
            
    except Exception as e:
        print(f"❌ 启动前端时出错: {e}")
        return False, None

def verify_system_integration():
    """验证系统集成"""
    print("\n🔗 验证系统集成...")
    
    # 检查前端页面
    try:
        print("   🌐 检查前端页面...")
        frontend_response = requests.get("http://localhost:3000", timeout=10)
        
        if frontend_response.status_code == 200:
            print("   ✅ 前端页面正常")
        else:
            print(f"   ❌ 前端页面异常: {frontend_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ 前端页面检查失败: {e}")
        return False
    
    # 检查语音功能
    try:
        print("   🎤 检查语音功能...")
        speech_response = requests.get("http://127.0.0.1:8000/speech_status", timeout=10)
        
        if speech_response.status_code == 200:
            speech_data = speech_response.json()
            speech_available = speech_data.get('baidu_speech_available', False)
            print(f"   🔊 语音功能: {'✅ 可用' if speech_available else '⚠️  不可用'}")
        else:
            print(f"   ❌ 语音状态检查失败: {speech_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 语音功能检查失败: {e}")
    
    return True

def show_startup_summary(backend_ok, deepseek_ok, deepseek_msg, frontend_ok, integration_ok):
    """显示启动总结"""
    print("\n" + "=" * 80)
    print("📊 系统启动结果总结")
    print("=" * 80)
    
    components = {
        "后端API服务": backend_ok,
        "DeepSeek后端": deepseek_ok,
        "前端React应用": frontend_ok,
        "系统集成": integration_ok
    }
    
    for component_name, status in components.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"   {component_name}: {status_text}")
    
    # DeepSeek状态详情
    print(f"   DeepSeek状态: {deepseek_msg}")
    
    total_passed = sum(components.values())
    total_components = len(components)
    
    print(f"\n📈 启动结果: {total_passed}/{total_components} 项正常")
    
    if total_passed == total_components:
        print("🎉 系统启动完全成功！")
        print("🤖 涂序彦教授数字人已准备就绪")
        status_level = "完美"
    elif total_passed >= 3:
        print("✅ 系统启动基本成功")
        print("🤖 主要功能可以正常使用")
        status_level = "良好"
    elif total_passed >= 2:
        print("⚠️  系统启动部分成功")
        print("🤖 部分功能可能有问题")
        status_level = "一般"
    else:
        print("❌ 系统启动失败")
        status_level = "失败"
    
    print(f"🏆 启动状态: {status_level}")
    
    print("\n🌐 服务地址:")
    print("   前端界面: http://localhost:3000")
    print("   后端API: http://127.0.0.1:8000")
    print("   API文档: http://127.0.0.1:8000/docs")
    
    print("\n🎯 优化功能:")
    print("   ✅ 移除了侧边栏消息emoji图标")
    print("   ✅ 添加了DeepSeek后端状态检测")
    print("   ✅ 替换了模型卡片的在线/离线状态指示器")
    
    print("\n💡 使用说明:")
    if deepseek_ok:
        print("   ✅ 可以进行智能对话")
        print("   ✅ 后端状态实时监控")
        print("   ✅ 优化的用户界面")
    
    if not deepseek_ok:
        print("\n🔧 故障排除:")
        print("   - 检查DeepSeek API密钥配置")
        print("   - 确认网络连接正常")
        print("   - 验证后端服务日志")
    
    return total_passed >= 2

def main():
    """主函数"""
    print_banner()
    
    # 1. 停止现有服务
    stop_existing_services()
    
    # 2. 启动后端
    backend_ok, backend_process = start_backend()
    
    # 3. DeepSeek后端状态检测
    deepseek_ok = False
    deepseek_msg = "未检测"
    
    if backend_ok:
        deepseek_ok, deepseek_msg = detect_deepseek_backend_status()
    
    # 4. 启动前端
    frontend_ok, frontend_process = start_frontend()
    
    # 5. 验证系统集成
    integration_ok = False
    if backend_ok and frontend_ok:
        integration_ok = verify_system_integration()
    
    # 6. 显示启动总结
    success = show_startup_summary(backend_ok, deepseek_ok, deepseek_msg, frontend_ok, integration_ok)
    
    # 7. 打开浏览器
    if success:
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
            print("💡 现在可以体验优化后的功能")
        except:
            print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
