#!/usr/bin/env python3
"""
涂序彦教授数字人项目 - 统一启动脚本
同时启动后端语音API服务器和前端React开发服务器
"""

import subprocess
import time
import os
import signal
import sys
import threading
import requests
from pathlib import Path

class UnifiedLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.project_root = Path(__file__).parent
        self.backend_port = 8000
        self.frontend_port = 3000
        self.shutdown_flag = threading.Event()
        
    def print_banner(self):
        """显示启动横幅"""
        print("=" * 70)
        print("🎯 涂序彦教授数字人项目 - 统一启动器 v2.0")
        print("=" * 70)
        print("📡 后端端口: 8000 (真实DeepSeek API服务器)")
        print("🌐 前端端口: 3000 (React开发服务器)")
        print("🔧 API类型: 真实DeepSeek API集成")
        print("=" * 70)
        
    def check_port_available(self, port):
        """检查端口是否可用"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result != 0
        except:
            return True
            
    def wait_for_service(self, url, timeout=30, service_name="服务"):
        """等待服务启动"""
        print(f"⏳ 等待{service_name}启动...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    print(f"✅ {service_name}启动成功")
                    return True
            except:
                pass
            time.sleep(1)
            
        print(f"❌ {service_name}启动超时")
        return False

    def verify_real_api_server(self):
        """验证启动的是真实API服务器"""
        try:
            print("🔍 验证API服务器类型...")

            # 发送测试请求
            test_data = {"prompt": "测试"}
            response = requests.post(
                f"http://127.0.0.1:{self.backend_port}/ask_professor",
                json=test_data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                source = result.get('source', 'unknown')
                thinking_time = result.get('thinking_time', 0)
                tokens_used = result.get('tokens_used', 0)

                print(f"📊 API响应分析:")
                print(f"   - 数据源: {source}")
                print(f"   - 响应时间: {thinking_time:.2f}秒")
                print(f"   - 使用tokens: {tokens_used}")

                # 判断是否为真实API
                if source == 'deepseek' and thinking_time > 1.0 and tokens_used > 0:
                    print("✅ 确认：真实DeepSeek API服务器")
                    return True
                else:
                    print("⚠️  警告：可能是模拟服务器")
                    return False
            else:
                print(f"❌ API测试失败: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ API验证异常: {e}")
            return False

    def start_backend(self):
        """启动后端服务器 - 真实DeepSeek API服务器"""
        print("🚀 启动后端真实DeepSeek API服务器...")

        # 检查端口
        if not self.check_port_available(self.backend_port):
            print(f"❌ 端口 {self.backend_port} 已被占用")
            return False

        try:
            # 使用uvicorn直接启动API服务器
            backend_module = "simple_api_server:app"

            # 检查服务器文件是否存在
            if not (self.project_root / "simple_api_server.py").exists():
                backend_module = "debug_server:app"
                if not (self.project_root / "debug_server.py").exists():
                    print(f"❌ 后端服务器文件不存在")
                    return False

            print(f"📡 启动模块: {backend_module}")
            print("🔧 服务器类型: DeepSeek API集成服务器")

            # 确保使用正确的Python环境
            import os
            env = os.environ.copy()

            # 使用uvicorn命令启动
            self.backend_process = subprocess.Popen(
                ["uvicorn", backend_module, "--host", "0.0.0.0", "--port", str(self.backend_port)],
                cwd=self.project_root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env
            )

            # 等待后端服务启动
            if self.wait_for_service(f"http://127.0.0.1:{self.backend_port}/",
                                   service_name="后端API服务"):
                # 验证是否为真实API服务器
                if self.verify_real_api_server():
                    return True
                else:
                    print("❌ 启动的不是真实API服务器")
                    self.stop_backend()
                    return False
            else:
                self.stop_backend()
                return False
                
        except Exception as e:
            print(f"❌ 后端启动失败: {e}")
            return False
            
    def start_frontend(self):
        """启动前端服务器"""
        print("🌐 启动前端React开发服务器...")
        
        frontend_dir = self.project_root / "react-version"
        if not frontend_dir.exists():
            print("❌ 前端目录不存在")
            return False
            
        # 检查端口
        if not self.check_port_available(self.frontend_port):
            print(f"❌ 端口 {self.frontend_port} 已被占用")
            return False
            
        # 检查package.json
        if not (frontend_dir / "package.json").exists():
            print("❌ 前端package.json不存在")
            return False
            
        try:
            # 设置环境变量避免自动打开浏览器
            env = os.environ.copy()
            env['BROWSER'] = 'none'
            
            self.frontend_process = subprocess.Popen(
                ["npm", "start"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            # 等待前端服务启动
            if self.wait_for_service(f"http://localhost:{self.frontend_port}/", 
                                   timeout=60, service_name="前端React服务"):
                return True
            else:
                self.stop_frontend()
                return False
                
        except Exception as e:
            print(f"❌ 前端启动失败: {e}")
            return False
            
    def stop_backend(self):
        """停止后端服务器"""
        if self.backend_process:
            print("🛑 停止后端服务器...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
            self.backend_process = None
            
    def stop_frontend(self):
        """停止前端服务器"""
        if self.frontend_process:
            print("🛑 停止前端服务器...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
            self.frontend_process = None
            
    def stop_all(self):
        """停止所有服务"""
        print("\n🛑 正在停止所有服务...")
        self.shutdown_flag.set()
        self.stop_backend()
        self.stop_frontend()
        print("✅ 所有服务已停止")
        
    def monitor_services(self):
        """监控服务状态"""
        while not self.shutdown_flag.is_set():
            time.sleep(5)
            
            # 检查后端进程
            if self.backend_process and self.backend_process.poll() is not None:
                print("⚠️  后端服务意外停止")
                break
                
            # 检查前端进程
            if self.frontend_process and self.frontend_process.poll() is not None:
                print("⚠️  前端服务意外停止")
                break
                
    def show_status(self):
        """显示服务状态"""
        print("\n📊 服务状态:")
        print("=" * 40)
        
        # 后端状态
        try:
            response = requests.get(f"http://127.0.0.1:{self.backend_port}/", timeout=2)
            print("✅ 后端API服务: 正常运行")
            print(f"   - 地址: http://127.0.0.1:{self.backend_port}")
            print(f"   - API文档: http://127.0.0.1:{self.backend_port}/docs")
        except:
            print("❌ 后端API服务: 未运行")
            
        # 前端状态
        try:
            response = requests.get(f"http://localhost:{self.frontend_port}/", timeout=2)
            print("✅ 前端React服务: 正常运行")
            print(f"   - 地址: http://localhost:{self.frontend_port}")
        except:
            print("❌ 前端React服务: 未运行")
            
        print("=" * 40)
        
    def run(self):
        """运行统一启动器"""
        self.print_banner()
        
        # 设置信号处理
        def signal_handler(signum, frame):
            self.stop_all()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # 启动后端
            if not self.start_backend():
                print("❌ 后端启动失败，退出")
                return False
                
            # 启动前端
            if not self.start_frontend():
                print("❌ 前端启动失败，停止后端并退出")
                self.stop_backend()
                return False
                
            # 显示状态
            self.show_status()
            
            print("\n🎉 所有服务启动成功！")
            print("💡 使用说明:")
            print("   - 前端界面: http://localhost:3000")
            print("   - 后端API: http://127.0.0.1:8000")
            print("   - 按 Ctrl+C 停止所有服务")
            
            # 监控服务
            self.monitor_services()
            
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()
            
        return True

def main():
    """主函数"""
    launcher = UnifiedLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
