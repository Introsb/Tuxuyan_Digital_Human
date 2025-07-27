#!/usr/bin/env python3
"""
重新启动前端和后端服务
"""

import subprocess
import time
import sys
import requests
import webbrowser
from pathlib import Path

class ServiceRestarter:
    def __init__(self):
        self.project_root = Path(__file__).parent
        
    def print_banner(self):
        """显示重启横幅"""
        print("=" * 80)
        print("🔄 涂序彦教授数字人项目 - 服务重启")
        print("=" * 80)
        print("🎯 重启内容:")
        print("   - 停止所有现有服务")
        print("   - 启动后端API服务器（完整功能）")
        print("   - 启动前端React应用")
        print("   - 验证服务正常运行")
        print("=" * 80)
    
    def stop_all_services(self):
        """停止所有服务"""
        print("\n🛑 停止所有现有服务...")
        
        # 停止uvicorn进程
        try:
            result = subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 已停止uvicorn进程")
            else:
                print("ℹ️  没有运行中的uvicorn进程")
        except Exception as e:
            print(f"⚠️  停止uvicorn时出现问题: {e}")
        
        # 停止npm进程
        try:
            result = subprocess.run(["pkill", "-f", "npm start"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 已停止npm进程")
            else:
                print("ℹ️  没有运行中的npm进程")
        except Exception as e:
            print(f"⚠️  停止npm时出现问题: {e}")
        
        # 停止node进程（React开发服务器）
        try:
            result = subprocess.run(["pkill", "-f", "react-scripts"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 已停止React开发服务器")
            else:
                print("ℹ️  没有运行中的React开发服务器")
        except Exception as e:
            print(f"⚠️  停止React服务器时出现问题: {e}")
        
        # 等待进程完全停止
        print("⏳ 等待进程完全停止...")
        time.sleep(5)
        
        # 检查端口是否释放
        self.check_ports_free()
    
    def check_ports_free(self):
        """检查端口是否释放"""
        print("\n🔍 检查端口状态...")
        
        # 检查8000端口（后端）
        try:
            requests.get("http://127.0.0.1:8000", timeout=2)
            print("⚠️  端口8000仍被占用")
        except:
            print("✅ 端口8000已释放")
        
        # 检查3000端口（前端）
        try:
            requests.get("http://localhost:3000", timeout=2)
            print("⚠️  端口3000仍被占用")
        except:
            print("✅ 端口3000已释放")
    
    def start_backend(self):
        """启动后端服务"""
        print("\n🔧 启动后端API服务器...")
        
        # 检查complete_api_server.py是否存在
        if not Path("complete_api_server.py").exists():
            print("❌ complete_api_server.py 不存在")
            return False, None
        
        try:
            # 启动后端
            backend_process = subprocess.Popen([
                "python3", "complete_api_server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print("⏳ 等待后端启动...")
            time.sleep(8)  # 等待8秒
            
            # 检查进程是否还在运行
            if backend_process.poll() is None:
                print("✅ 后端API服务器启动成功")
                
                # 验证后端响应
                try:
                    response = requests.get("http://127.0.0.1:8000/", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   服务器版本: {data.get('version', '未知')}")
                        print(f"   可用功能: {data.get('features', [])}")
                        return True, backend_process
                    else:
                        print(f"⚠️  后端响应异常: {response.status_code}")
                        return False, backend_process
                except Exception as e:
                    print(f"⚠️  后端验证失败: {e}")
                    return False, backend_process
            else:
                print("❌ 后端API服务器启动失败")
                # 打印错误信息
                stdout, stderr = backend_process.communicate()
                if stderr:
                    print(f"错误信息: {stderr.decode()}")
                return False, None
                
        except Exception as e:
            print(f"❌ 启动后端时出错: {e}")
            return False, None
    
    def start_frontend(self):
        """启动前端服务"""
        print("\n🌐 启动前端React应用...")
        
        frontend_dir = Path("react-version")
        if not frontend_dir.exists():
            print("❌ react-version 目录不存在")
            return False, None
        
        # 检查package.json是否存在
        if not (frontend_dir / "package.json").exists():
            print("❌ package.json 不存在")
            return False, None
        
        try:
            # 启动前端
            frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print("⏳ 等待前端启动...")
            time.sleep(20)  # 等待20秒，前端启动较慢
            
            # 检查进程是否还在运行
            if frontend_process.poll() is None:
                print("✅ 前端React应用启动成功")
                
                # 验证前端响应
                try:
                    response = requests.get("http://localhost:3000", timeout=10)
                    if response.status_code == 200:
                        print(f"   页面大小: {len(response.content)} bytes")
                        return True, frontend_process
                    else:
                        print(f"⚠️  前端响应异常: {response.status_code}")
                        return False, frontend_process
                except Exception as e:
                    print(f"⚠️  前端验证失败: {e}")
                    return False, frontend_process
            else:
                print("❌ 前端React应用启动失败")
                # 打印错误信息
                stdout, stderr = frontend_process.communicate()
                if stderr:
                    print(f"错误信息: {stderr.decode()}")
                return False, None
                
        except Exception as e:
            print(f"❌ 启动前端时出错: {e}")
            return False, None
    
    def test_functionality(self):
        """测试功能"""
        print("\n🧪 测试系统功能...")
        
        # 测试聊天功能
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask_professor",
                json={"message": "你好，重启测试"},
                timeout=30
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
        
        # 测试语音功能
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
    
    def show_startup_summary(self, backend_ok, frontend_ok, chat_ok, speech_ok):
        """显示启动总结"""
        print("\n" + "=" * 80)
        print("📊 服务重启结果总结")
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
        
        print(f"\n📈 总体状态: {total_passed}/{total_services} 项服务正常")
        
        if total_passed == total_services:
            print("🎉 服务重启完全成功！所有功能正常")
            status_level = "完美"
        elif total_passed >= 3:
            print("✅ 服务重启基本成功，个别功能可能需要调整")
            status_level = "良好"
        elif total_passed >= 2:
            print("⚠️  服务重启部分成功，部分功能有问题")
            status_level = "一般"
        else:
            print("❌ 服务重启失败")
            status_level = "失败"
        
        print(f"🏆 重启状态: {status_level}")
        
        print("\n🌐 服务地址:")
        print("   前端界面: http://localhost:3000")
        print("   后端API: http://127.0.0.1:8000")
        print("   API文档: http://127.0.0.1:8000/docs")
        print("   语音状态: http://127.0.0.1:8000/speech_status")
        
        print("\n💡 功能说明:")
        if chat_ok:
            print("   ✅ 可以进行文字聊天对话")
        if speech_ok:
            print("   ✅ 可以使用语音输入和播放")
        
        print("\n🛑 停止服务命令:")
        print("   pkill -f uvicorn")
        print("   pkill -f 'npm start'")
        
        return total_passed >= 2
    
    def restart_services(self):
        """重启所有服务"""
        self.print_banner()
        
        # 1. 停止所有服务
        self.stop_all_services()
        
        # 2. 启动后端
        backend_ok, backend_process = self.start_backend()
        
        # 3. 启动前端
        frontend_ok, frontend_process = self.start_frontend()
        
        # 4. 测试功能
        if backend_ok:
            chat_ok, speech_ok = self.test_functionality()
        else:
            chat_ok, speech_ok = False, False
        
        # 5. 显示总结
        success = self.show_startup_summary(backend_ok, frontend_ok, chat_ok, speech_ok)
        
        # 6. 打开浏览器
        if success:
            try:
                webbrowser.open("http://localhost:3000")
                print("\n🌐 已在浏览器中打开项目界面")
            except:
                print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
        
        return success

def main():
    """主函数"""
    restarter = ServiceRestarter()
    success = restarter.restart_services()
    
    if success:
        print("\n🎯 服务重启成功！")
        print("💡 现在可以使用聊天和语音功能")
    else:
        print("\n❌ 服务重启失败，请检查错误信息")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
