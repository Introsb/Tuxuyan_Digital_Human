#!/usr/bin/env python3
"""
涂序彦教授数字人项目 - 最终启动脚本
简单、可靠、直接的启动方案
"""

import subprocess
import time
import sys
import signal
import requests
from pathlib import Path

class ProjectStarter:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.frontend_process = None
        
    def print_banner(self):
        """显示启动横幅"""
        print("=" * 70)
        print("🎯 涂序彦教授数字人项目 - 最终启动器")
        print("=" * 70)
        print("📡 后端端口: 8000 (DeepSeek API服务器)")
        print("🌐 前端端口: 3000 (React开发服务器)")
        print("🔧 启动方式: 直接uvicorn命令")
        print("=" * 70)
    
    def start_backend(self):
        """启动后端服务器"""
        print("🚀 启动后端API服务器...")
        
        try:
            # 使用uvicorn直接启动simple_api_server
            cmd = ["uvicorn", "simple_api_server:app", "--host", "0.0.0.0", "--port", "8000"]
            
            print(f"📡 执行命令: {' '.join(cmd)}")
            
            self.backend_process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            
            # 等待后端启动
            print("⏳ 等待后端服务启动...")
            for i in range(30):  # 等待30秒
                try:
                    response = requests.get("http://127.0.0.1:8000/", timeout=2)
                    if response.status_code == 200:
                        print("✅ 后端API服务启动成功")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"   等待中... ({i+1}/30)")
            
            print("❌ 后端启动超时")
            return False
            
        except Exception as e:
            print(f"❌ 后端启动失败: {e}")
            return False
    
    def start_frontend(self):
        """启动前端服务器"""
        print("🌐 启动前端React开发服务器...")
        
        try:
            frontend_dir = self.project_root / "react-version"
            
            if not frontend_dir.exists():
                print("❌ 前端目录不存在")
                return False
            
            # 启动React开发服务器
            cmd = ["npm", "start"]
            
            self.frontend_process = subprocess.Popen(
                cmd,
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            
            # 等待前端启动
            print("⏳ 等待前端服务启动...")
            for i in range(60):  # 等待60秒
                try:
                    response = requests.get("http://localhost:3000", timeout=2)
                    if response.status_code == 200:
                        print("✅ 前端React服务启动成功")
                        return True
                except:
                    pass
                time.sleep(1)
                if i % 10 == 9:  # 每10秒显示一次进度
                    print(f"   等待中... ({i+1}/60)")
            
            print("❌ 前端启动超时")
            return False
            
        except Exception as e:
            print(f"❌ 前端启动失败: {e}")
            return False
    
    def test_api(self):
        """测试API功能"""
        print("🧪 测试API功能...")
        
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask_professor",
                json={"prompt": "你好"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                source = result.get('source', 'unknown')
                tokens = result.get('tokens_used', 0)
                
                print(f"✅ API测试成功")
                print(f"📊 数据源: {source}")
                print(f"🔢 使用tokens: {tokens}")
                
                if source == 'deepseek' and tokens > 0:
                    print("✅ 确认：真实DeepSeek API调用")
                    return True
                else:
                    print("⚠️  警告：可能不是真实API调用")
                    return False
            else:
                print(f"❌ API测试失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API测试异常: {e}")
            return False
    
    def show_status(self):
        """显示服务状态"""
        print("\n📊 服务状态:")
        print("=" * 40)
        
        # 检查后端
        try:
            response = requests.get("http://127.0.0.1:8000/", timeout=2)
            print("✅ 后端API服务: 正常运行")
            print("   - 地址: http://127.0.0.1:8000")
        except:
            print("❌ 后端API服务: 无法访问")
        
        # 检查前端
        try:
            response = requests.get("http://localhost:3000", timeout=2)
            print("✅ 前端React服务: 正常运行")
            print("   - 地址: http://localhost:3000")
        except:
            print("❌ 前端React服务: 无法访问")
        
        print("=" * 40)
    
    def stop_all(self):
        """停止所有服务"""
        print("\n🛑 正在停止所有服务...")
        
        if self.backend_process:
            print("🛑 停止后端服务器...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except:
                self.backend_process.kill()
        
        if self.frontend_process:
            print("🛑 停止前端服务器...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except:
                self.frontend_process.kill()
        
        print("✅ 所有服务已停止")
    
    def run(self):
        """运行项目"""
        self.print_banner()
        
        # 设置信号处理
        def signal_handler(signum, frame):
            self.stop_all()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # 启动后端
        if not self.start_backend():
            print("❌ 后端启动失败，退出")
            return False
        
        # 测试API
        if not self.test_api():
            print("⚠️  API测试失败，但继续启动前端")
        
        # 启动前端
        if not self.start_frontend():
            print("❌ 前端启动失败")
            self.stop_all()
            return False
        
        # 显示状态
        self.show_status()
        
        print("\n🎉 所有服务启动成功！")
        print("💡 使用说明:")
        print("   - 前端界面: http://localhost:3000")
        print("   - 后端API: http://127.0.0.1:8000")
        print("   - 按 Ctrl+C 停止所有服务")
        print("\n⏳ 服务运行中，按 Ctrl+C 停止...")
        
        # 保持运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_all()
        
        return True

def main():
    """主函数"""
    starter = ProjectStarter()
    success = starter.run()
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
