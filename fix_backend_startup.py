#!/usr/bin/env python3
"""
修复后端启动问题
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

def print_banner():
    """显示横幅"""
    print("=" * 80)
    print("🔧 修复后端启动问题")
    print("=" * 80)
    print("🎯 诊断内容:")
    print("   - 检查Python环境和依赖")
    print("   - 验证API服务器文件")
    print("   - 测试不同启动方式")
    print("   - 修复常见问题")
    print("=" * 80)

def check_python_environment():
    """检查Python环境"""
    print("\n🐍 检查Python环境...")
    
    try:
        # 检查Python版本
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python版本: {result.stdout.strip()}")
        
        # 检查关键依赖
        dependencies = ["fastapi", "uvicorn", "requests", "pydantic"]
        
        for dep in dependencies:
            try:
                result = subprocess.run([sys.executable, "-c", f"import {dep}; print({dep}.__version__)"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {dep}: {result.stdout.strip()}")
                else:
                    print(f"❌ {dep}: 未安装")
                    return False
            except Exception as e:
                print(f"❌ {dep}: 检查失败 - {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Python环境检查失败: {e}")
        return False

def check_api_server_file():
    """检查API服务器文件"""
    print("\n📄 检查API服务器文件...")
    
    api_file = Path("complete_api_server.py")
    if not api_file.exists():
        print("❌ complete_api_server.py 文件不存在")
        return False
    
    print("✅ complete_api_server.py 文件存在")
    
    # 检查文件语法
    try:
        result = subprocess.run([sys.executable, "-m", "py_compile", "complete_api_server.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 文件语法正确")
            return True
        else:
            print(f"❌ 文件语法错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 语法检查失败: {e}")
        return False

def stop_existing_processes():
    """停止现有进程"""
    print("\n🛑 停止现有后端进程...")
    
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        subprocess.run(["pkill", "-f", "complete_api_server"], check=False)
        print("✅ 已停止现有进程")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"⚠️  停止进程时出现问题: {e}")
        return True  # 继续执行

def test_direct_import():
    """测试直接导入"""
    print("\n📦 测试直接导入...")
    
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "from complete_api_server import app; print('✅ 导入成功')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ 模块导入成功")
            return True
        else:
            print(f"❌ 模块导入失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ 模块导入超时")
        return False
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        return False

def start_backend_method1():
    """方法1: 使用uvicorn命令行启动"""
    print("\n🚀 方法1: 使用uvicorn命令行启动...")
    
    try:
        process = subprocess.Popen([
            "uvicorn", "complete_api_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待启动...")
        time.sleep(8)
        
        if process.poll() is None:
            print("✅ uvicorn命令行启动成功")
            return True, process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ uvicorn命令行启动失败")
            if stderr:
                print(f"错误信息: {stderr.decode()}")
            return False, None
            
    except Exception as e:
        print(f"❌ uvicorn命令行启动异常: {e}")
        return False, None

def start_backend_method2():
    """方法2: 使用Python直接运行"""
    print("\n🚀 方法2: 使用Python直接运行...")
    
    try:
        process = subprocess.Popen([
            sys.executable, "complete_api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待启动...")
        time.sleep(8)
        
        if process.poll() is None:
            print("✅ Python直接运行启动成功")
            return True, process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Python直接运行启动失败")
            if stderr:
                print(f"错误信息: {stderr.decode()}")
            return False, None
            
    except Exception as e:
        print(f"❌ Python直接运行异常: {e}")
        return False, None

def start_backend_method3():
    """方法3: 使用Python内联uvicorn"""
    print("\n🚀 方法3: 使用Python内联uvicorn...")
    
    inline_script = '''
import uvicorn
import sys
import os

try:
    from complete_api_server import app
    print("✅ 模块导入成功")
    print("🚀 启动uvicorn服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
except Exception as e:
    print(f"❌ 启动失败: {e}")
    sys.exit(1)
'''
    
    try:
        process = subprocess.Popen([
            sys.executable, "-c", inline_script
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待启动...")
        time.sleep(8)
        
        if process.poll() is None:
            print("✅ Python内联uvicorn启动成功")
            return True, process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Python内联uvicorn启动失败")
            if stdout:
                print(f"输出信息: {stdout.decode()}")
            if stderr:
                print(f"错误信息: {stderr.decode()}")
            return False, None
            
    except Exception as e:
        print(f"❌ Python内联uvicorn异常: {e}")
        return False, None

def test_backend_response():
    """测试后端响应"""
    print("\n🧪 测试后端响应...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 后端响应正常")
            print(f"   版本: {data.get('version', '未知')}")
            print(f"   功能: {data.get('features', [])}")
            return True
        else:
            print(f"❌ 后端响应异常: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务")
        return False
    except Exception as e:
        print(f"❌ 后端测试失败: {e}")
        return False

def test_chat_function():
    """测试聊天功能"""
    print("\n💬 测试聊天功能...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": "你好，后端测试"},
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天功能正常")
            print(f"   回复: {result.get('answer', '无回复')[:50]}...")
            return True
        else:
            print(f"❌ 聊天功能异常: {response.status_code}")
            print(f"   错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天功能测试失败: {e}")
        return False

def show_results(env_ok, file_ok, import_ok, backend_ok, response_ok, chat_ok):
    """显示结果"""
    print("\n" + "=" * 80)
    print("📊 后端启动诊断结果")
    print("=" * 80)
    
    checks = {
        "Python环境": env_ok,
        "API文件": file_ok,
        "模块导入": import_ok,
        "后端启动": backend_ok,
        "服务响应": response_ok,
        "聊天功能": chat_ok
    }
    
    for check_name, status in checks.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"   {check_name}: {status_text}")
    
    total_passed = sum(checks.values())
    total_checks = len(checks)
    
    print(f"\n📈 诊断结果: {total_passed}/{total_checks} 项正常")
    
    if total_passed == total_checks:
        print("🎉 后端完全正常！")
        print("\n🌐 服务地址:")
        print("   后端API: http://127.0.0.1:8000")
        print("   API文档: http://127.0.0.1:8000/docs")
        return True
    elif backend_ok and response_ok:
        print("✅ 后端基本正常，部分功能可能有问题")
        return True
    else:
        print("❌ 后端存在严重问题")
        print("\n💡 建议:")
        if not env_ok:
            print("   - 检查Python环境和依赖安装")
        if not file_ok:
            print("   - 检查API服务器文件完整性")
        if not import_ok:
            print("   - 检查模块导入问题")
        if not backend_ok:
            print("   - 尝试不同的启动方式")
        return False

def main():
    """主函数"""
    print_banner()
    
    # 1. 检查Python环境
    env_ok = check_python_environment()
    
    # 2. 检查API文件
    file_ok = check_api_server_file()
    
    # 3. 测试模块导入
    import_ok = test_direct_import()
    
    # 4. 停止现有进程
    stop_existing_processes()
    
    # 5. 尝试启动后端
    backend_ok = False
    successful_process = None
    
    if env_ok and file_ok and import_ok:
        # 尝试方法1
        success, process = start_backend_method1()
        if success:
            backend_ok = True
            successful_process = process
        else:
            # 尝试方法2
            success, process = start_backend_method2()
            if success:
                backend_ok = True
                successful_process = process
            else:
                # 尝试方法3
                success, process = start_backend_method3()
                if success:
                    backend_ok = True
                    successful_process = process
    
    # 6. 测试后端响应
    response_ok = False
    chat_ok = False
    
    if backend_ok:
        response_ok = test_backend_response()
        if response_ok:
            chat_ok = test_chat_function()
    
    # 7. 显示结果
    success = show_results(env_ok, file_ok, import_ok, backend_ok, response_ok, chat_ok)
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
