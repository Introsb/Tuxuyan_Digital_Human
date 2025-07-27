#!/usr/bin/env python3
"""
涂序彦教授数字人项目 - 快速启动脚本
最简单、最直接的启动方案
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🚀 涂序彦教授数字人项目 - 快速启动")
    print("=" * 60)

def check_dependencies():
    """检查基本依赖"""
    print("🔍 检查依赖...")
    
    try:
        import uvicorn
        print("✅ uvicorn 可用")
    except ImportError:
        print("❌ 缺少 uvicorn，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn"], check=True)
    
    try:
        import fastapi
        print("✅ fastapi 可用")
    except ImportError:
        print("❌ 缺少 fastapi，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi"], check=True)
    
    try:
        import openai
        print("✅ openai 可用")
    except ImportError:
        print("❌ 缺少 openai，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai"], check=True)

def start_backend():
    """启动后端"""
    print("\n🔧 启动后端服务器...")
    
    # 检查simple_api_server.py是否存在
    if not Path("simple_api_server.py").exists():
        print("❌ simple_api_server.py 不存在")
        return False
    
    try:
        # 使用subprocess启动后端，不等待
        backend_process = subprocess.Popen([
            "uvicorn", "simple_api_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("⏳ 等待后端启动...")
        time.sleep(5)  # 等待5秒
        
        # 检查进程是否还在运行
        if backend_process.poll() is None:
            print("✅ 后端服务器启动成功")
            return True
        else:
            print("❌ 后端服务器启动失败")
            return False
            
    except Exception as e:
        print(f"❌ 启动后端时出错: {e}")
        return False

def start_frontend():
    """启动前端"""
    print("\n🌐 启动前端服务器...")
    
    frontend_dir = Path("react-version")
    if not frontend_dir.exists():
        print("❌ react-version 目录不存在")
        return False
    
    try:
        # 检查是否已安装依赖
        if not (frontend_dir / "node_modules").exists():
            print("📦 安装前端依赖...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # 启动前端
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("⏳ 等待前端启动...")
        time.sleep(10)  # 等待10秒
        
        # 检查进程是否还在运行
        if frontend_process.poll() is None:
            print("✅ 前端服务器启动成功")
            return True
        else:
            print("❌ 前端服务器启动失败")
            return False
            
    except Exception as e:
        print(f"❌ 启动前端时出错: {e}")
        return False

def test_services():
    """测试服务"""
    print("\n🧪 测试服务...")
    
    try:
        import requests
        
        # 测试后端
        try:
            response = requests.get("http://127.0.0.1:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ 后端API正常")
            else:
                print("⚠️  后端API响应异常")
        except:
            print("❌ 后端API无法访问")
        
        # 测试前端
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务正常")
            else:
                print("⚠️  前端服务响应异常")
        except:
            print("❌ 前端服务无法访问")
            
    except ImportError:
        print("⚠️  无法测试服务（缺少requests库）")

def show_instructions():
    """显示使用说明"""
    print("\n" + "=" * 60)
    print("🎉 启动完成！")
    print("=" * 60)
    print("📱 前端界面: http://localhost:3000")
    print("🔧 后端API: http://127.0.0.1:8000")
    print("📚 API文档: http://127.0.0.1:8000/docs")
    print("=" * 60)
    print("💡 使用提示:")
    print("   1. 在浏览器中打开 http://localhost:3000")
    print("   2. 与涂序彦教授AI进行对话")
    print("   3. 如果遇到问题，请检查终端输出")
    print("=" * 60)

def main():
    """主函数"""
    print_header()
    
    # 1. 检查依赖
    check_dependencies()
    
    # 2. 启动后端
    backend_ok = start_backend()
    
    # 3. 启动前端
    frontend_ok = start_frontend()
    
    # 4. 测试服务
    test_services()
    
    # 5. 显示说明
    show_instructions()
    
    if backend_ok and frontend_ok:
        print("\n✅ 所有服务启动成功！")
        print("🔗 请在浏览器中访问: http://localhost:3000")
        return True
    else:
        print("\n❌ 部分服务启动失败")
        if not backend_ok:
            print("   - 后端服务器启动失败")
        if not frontend_ok:
            print("   - 前端服务器启动失败")
        print("\n🔧 故障排除建议:")
        print("   1. 检查端口8000和3000是否被占用")
        print("   2. 确认虚拟环境已激活")
        print("   3. 手动启动服务器进行调试")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n⏳ 服务已在后台运行")
        print("💡 要停止服务，请使用以下命令:")
        print("   pkill -f uvicorn")
        print("   pkill -f 'npm start'")
    
    sys.exit(0 if success else 1)
