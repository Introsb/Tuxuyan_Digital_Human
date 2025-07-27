#!/usr/bin/env python3
"""
完整系统启动脚本
启动前端和后端服务
"""

import subprocess
import time
import sys
import requests
import webbrowser
from pathlib import Path
import os

class FullSystemStarter:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.frontend_process = None
        
    def print_banner(self):
        """显示启动横幅"""
        print("=" * 80)
        print("🚀 涂序彦教授数字人项目 - 完整系统启动")
        print("=" * 80)
        print("🎯 启动内容:")
        print("   - 后端API服务器（聊天+语音功能）")
        print("   - 前端React应用")
        print("   - 验证所有功能正常")
        print("=" * 80)
    
    def stop_existing_services(self):
        """停止现有服务"""
        print("\n🛑 停止现有服务...")
        
        try:
            # 停止uvicorn进程
            subprocess.run(["pkill", "-f", "uvicorn"], check=False)
            print("✅ 已停止现有uvicorn进程")
        except:
            print("⚠️  停止uvicorn进程时出现问题")
        
        try:
            # 停止npm进程
            subprocess.run(["pkill", "-f", "npm start"], check=False)
            print("✅ 已停止现有npm进程")
        except:
            print("⚠️  停止npm进程时出现问题")
        
        # 等待进程完全停止
        time.sleep(3)
        print("⏳ 等待进程完全停止...")
    
    def start_backend(self):
        """启动后端服务"""
        print("\n🔧 启动后端API服务器...")
        
        # 检查complete_api_server.py是否存在
        if not Path("complete_api_server.py").exists():
            print("❌ complete_api_server.py 不存在")
            return False
        
        try:
            # 启动后端
            self.backend_process = subprocess.Popen([
                "uvicorn", "complete_api_server:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print("⏳ 等待后端启动...")
            time.sleep(10)  # 等待10秒
            
            # 检查进程是否还在运行
            if self.backend_process.poll() is None:
                print("✅ 后端API服务器启动成功")
                return True
            else:
                print("❌ 后端API服务器启动失败")
                # 打印错误信息
                stdout, stderr = self.backend_process.communicate()
                if stderr:
                    print(f"错误信息: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ 启动后端时出错: {e}")
            return False
    
    def start_frontend(self):
        """启动前端服务"""
        print("\n🌐 启动前端React应用...")
        
        frontend_dir = Path("react-version")
        if not frontend_dir.exists():
            print("❌ react-version 目录不存在")
            return False
        
        # 检查package.json是否存在
        if not (frontend_dir / "package.json").exists():
            print("❌ package.json 不存在")
            return False
        
        try:
            # 启动前端
            self.frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print("⏳ 等待前端启动...")
            time.sleep(15)  # 等待15秒，前端启动较慢
            
            # 检查进程是否还在运行
            if self.frontend_process.poll() is None:
                print("✅ 前端React应用启动成功")
                return True
            else:
                print("❌ 前端React应用启动失败")
                # 打印错误信息
                stdout, stderr = self.frontend_process.communicate()
                if stderr:
                    print(f"错误信息: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ 启动前端时出错: {e}")
            return False
    
    def test_backend_health(self):
        """测试后端健康状态"""
        print("\n🧪 测试后端健康状态...")
        
        try:
            # 测试健康检查端点
            response = requests.get("http://127.0.0.1:8000/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 后端健康检查正常")
                print(f"   服务器版本: {data.get('version', '未知')}")
                print(f"   服务器类型: {data.get('server_type', '未知')}")
                print(f"   可用功能: {data.get('features', [])}")
                return True
            else:
                print(f"❌ 后端健康检查失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 后端健康检查异常: {e}")
            return False
    
    def test_frontend_health(self):
        """测试前端健康状态"""
        print("\n🧪 测试前端健康状态...")
        
        try:
            # 测试前端页面
            response = requests.get("http://localhost:3000", timeout=10)
            
            if response.status_code == 200:
                print("✅ 前端页面正常")
                print(f"   页面大小: {len(response.content)} bytes")
                return True
            else:
                print(f"❌ 前端页面失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 前端页面异常: {e}")
            return False
    
    def test_chat_functionality(self):
        """测试聊天功能"""
        print("\n🧪 测试聊天功能...")
        
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask_professor",
                json={"message": "你好，系统启动测试"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 聊天功能正常")
                print(f"📝 回复内容: {result.get('answer', '无回复')[:100]}...")
                print(f"🤖 回复来源: {result.get('source', '未知')}")
                print(f"⏱️  响应时间: {result.get('thinking_time', 0):.2f}秒")
                return True
            else:
                print(f"❌ 聊天功能失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 聊天功能异常: {e}")
            return False
    
    def test_speech_functionality(self):
        """测试语音功能"""
        print("\n🧪 测试语音功能...")
        
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
                print(f"❌ 语音状态端点失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 语音功能异常: {e}")
            return False
    
    def create_usage_guide(self):
        """创建使用指南"""
        print("\n📄 创建使用指南...")
        
        guide_content = """# 🎯 涂序彦教授数字人使用指南

## 🌐 访问地址
- **前端界面**: http://localhost:3000
- **后端API**: http://127.0.0.1:8000
- **API文档**: http://127.0.0.1:8000/docs
- **语音状态**: http://127.0.0.1:8000/speech_status

## 💬 聊天功能
1. 在前端界面的输入框中输入问题
2. 点击发送按钮或按回车键
3. AI会以涂序彦教授的身份回答您的问题

## 🎤 语音功能
### 语音输入（ASR）
1. 点击麦克风按钮 🎤 开始录音
2. 说话（系统会显示录音状态）
3. 再次点击麦克风按钮停止录音
4. 系统自动识别语音并转换为文字
5. 自动发送消息给AI

### 语音播放（TTS）
1. AI回复消息后，每条消息旁会显示播放按钮 🔊
2. 点击播放按钮听取AI的语音回复
3. 支持暂停/继续播放

## 🔧 故障排除
### 如果聊天功能不工作
1. 检查后端是否正常运行：访问 http://127.0.0.1:8000
2. 查看浏览器控制台是否有错误信息
3. 确认网络连接正常

### 如果语音功能不工作
1. 检查浏览器麦克风权限
2. 确认使用的是支持的浏览器（Chrome、Firefox、Safari）
3. 访问 http://127.0.0.1:8000/speech_status 查看语音服务状态

### 如果前端页面无法访问
1. 确认前端服务正在运行
2. 检查端口3000是否被占用
3. 尝试刷新浏览器页面

## 📱 浏览器兼容性
- ✅ Chrome（推荐）
- ✅ Firefox
- ✅ Safari
- ⚠️ Edge（部分功能可能有限制）

## 🎯 使用技巧
1. **提问方式**: 可以询问AI、机器学习、深度学习等相关问题
2. **语音质量**: 录音时保持安静环境，清晰发音
3. **响应时间**: AI回复可能需要5-20秒，请耐心等待

## 🛑 停止服务
如需停止服务，请使用以下命令：
```bash
pkill -f uvicorn    # 停止后端
pkill -f "npm start"  # 停止前端
```

## 📞 技术支持
如遇到问题，请检查：
1. 终端输出的错误信息
2. 浏览器控制台的错误信息
3. 网络连接状态
4. API密钥配置
"""
        
        with open("USAGE_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(guide_content)
        
        print("✅ 使用指南已创建: USAGE_GUIDE.md")
    
    def show_startup_summary(self, backend_ok, frontend_ok, chat_ok, speech_ok):
        """显示启动总结"""
        print("\n" + "=" * 80)
        print("📊 系统启动结果总结")
        print("=" * 80)
        
        results = {
            "后端服务": backend_ok,
            "前端服务": frontend_ok,
            "聊天功能": chat_ok,
            "语音功能": speech_ok
        }
        
        for service_name, result in results.items():
            status = "✅ 正常" if result else "❌ 异常"
            print(f"   {service_name}: {status}")
        
        total_passed = sum(results.values())
        total_tests = len(results)
        
        print(f"\n📈 总体结果: {total_passed}/{total_tests} 项服务正常")
        
        if total_passed == total_tests:
            print("🎉 系统启动完全成功！所有功能正常")
        elif backend_ok and frontend_ok:
            print("⚠️  基本服务正常，部分功能可能需要调整")
        else:
            print("❌ 启动过程中出现问题")
        
        print("\n🌐 服务地址:")
        print("   前端界面: http://localhost:3000")
        print("   后端API: http://127.0.0.1:8000")
        print("   API文档: http://127.0.0.1:8000/docs")
        
        print("\n💡 使用提示:")
        print("   1. 在前端界面输入问题与AI对话")
        print("   2. 点击麦克风按钮进行语音输入")
        print("   3. 点击播放按钮听取AI语音回复")
        
        if total_passed >= 2:  # 至少前后端正常
            print("\n✅ 系统已准备就绪，可以开始使用！")
        else:
            print("\n❌ 系统启动失败，请检查错误信息")
    
    def start_full_system(self):
        """启动完整系统"""
        self.print_banner()
        
        # 1. 停止现有服务
        self.stop_existing_services()
        
        # 2. 启动后端
        backend_ok = self.start_backend()
        
        # 3. 启动前端
        frontend_ok = self.start_frontend()
        
        # 4. 测试后端健康状态
        if backend_ok:
            backend_health = self.test_backend_health()
        else:
            backend_health = False
        
        # 5. 测试前端健康状态
        if frontend_ok:
            frontend_health = self.test_frontend_health()
        else:
            frontend_health = False
        
        # 6. 测试聊天功能
        if backend_health:
            chat_ok = self.test_chat_functionality()
        else:
            chat_ok = False
        
        # 7. 测试语音功能
        if backend_health:
            speech_ok = self.test_speech_functionality()
        else:
            speech_ok = False
        
        # 8. 创建使用指南
        self.create_usage_guide()
        
        # 9. 显示启动总结
        self.show_startup_summary(backend_ok and backend_health, 
                                 frontend_ok and frontend_health, 
                                 chat_ok, speech_ok)
        
        # 10. 打开浏览器
        if frontend_ok and frontend_health:
            try:
                webbrowser.open("http://localhost:3000")
                print("\n🌐 已在浏览器中打开项目界面")
            except:
                print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
        
        success = backend_ok and frontend_ok and backend_health and frontend_health
        
        if success:
            print("\n⏳ 服务已在后台运行")
            print("💡 要停止服务，请使用以下命令:")
            print("   pkill -f uvicorn")
            print("   pkill -f 'npm start'")
        
        return success

def main():
    """主函数"""
    starter = FullSystemStarter()
    success = starter.start_full_system()
    
    if success:
        print("\n🎯 系统启动成功！")
        print("📖 详细使用说明请查看: USAGE_GUIDE.md")
    else:
        print("\n❌ 系统启动失败")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
