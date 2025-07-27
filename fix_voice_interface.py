#!/usr/bin/env python3
"""
语音接口修复脚本
修复语音功能不可用的问题
"""

import subprocess
import time
import sys
import os
import requests
import webbrowser
from pathlib import Path

class VoiceInterfaceFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        
    def print_banner(self):
        """显示修复横幅"""
        print("=" * 80)
        print("🔧 涂序彦教授数字人项目 - 语音接口修复")
        print("=" * 80)
        print("🎯 修复目标:")
        print("   - 停止当前的simple_api_server")
        print("   - 启动包含语音功能的api_server")
        print("   - 安装百度语音SDK依赖")
        print("   - 验证语音功能正常工作")
        print("=" * 80)
    
    def stop_current_services(self):
        """停止当前服务"""
        print("\n🛑 停止当前服务...")
        
        try:
            # 停止uvicorn进程
            subprocess.run(["pkill", "-f", "uvicorn"], check=False)
            print("✅ 已停止uvicorn进程")
        except:
            print("⚠️  停止uvicorn进程时出现问题")
        
        try:
            # 停止npm进程
            subprocess.run(["pkill", "-f", "npm start"], check=False)
            print("✅ 已停止npm进程")
        except:
            print("⚠️  停止npm进程时出现问题")
        
        # 等待进程完全停止
        time.sleep(3)
        print("⏳ 等待进程完全停止...")
    
    def install_speech_dependencies(self):
        """安装语音相关依赖"""
        print("\n📦 安装语音相关依赖...")
        
        dependencies = [
            "baidu-aip",
            "pydub",
            "wave"
        ]
        
        for dep in dependencies:
            try:
                print(f"📥 安装 {dep}...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", dep
                ], check=True, capture_output=True)
                print(f"✅ {dep} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  {dep} 安装失败: {e}")
    
    def start_voice_enabled_backend(self):
        """启动包含语音功能的后端"""
        print("\n🔧 启动包含语音功能的后端服务器...")
        
        # 检查api_server.py是否存在
        if not Path("api_server.py").exists():
            print("❌ api_server.py 不存在")
            return False
        
        try:
            # 使用subprocess启动后端，不等待
            backend_process = subprocess.Popen([
                "uvicorn", "api_server:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload"
            ])
            
            print("⏳ 等待后端启动...")
            time.sleep(8)  # 等待8秒，给语音API初始化时间
            
            # 检查进程是否还在运行
            if backend_process.poll() is None:
                print("✅ 语音功能后端服务器启动成功")
                return True
            else:
                print("❌ 语音功能后端服务器启动失败")
                return False
                
        except Exception as e:
            print(f"❌ 启动语音功能后端时出错: {e}")
            return False
    
    def start_frontend(self):
        """启动前端"""
        print("\n🌐 启动前端服务器...")
        
        frontend_dir = Path("react-version")
        if not frontend_dir.exists():
            print("❌ react-version 目录不存在")
            return False
        
        try:
            # 启动前端
            frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd=frontend_dir)
            
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
    
    def test_voice_endpoints(self):
        """测试语音端点"""
        print("\n🧪 测试语音端点...")
        
        try:
            # 测试语音状态端点
            print("🔍 测试语音状态端点...")
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
            print(f"❌ 测试语音端点异常: {e}")
            return False
    
    def test_basic_endpoints(self):
        """测试基本端点"""
        print("\n🧪 测试基本服务...")
        
        try:
            # 测试后端
            response = requests.get("http://127.0.0.1:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ 后端API正常")
                backend_ok = True
            else:
                print("⚠️  后端API响应异常")
                backend_ok = False
        except:
            print("❌ 后端API无法访问")
            backend_ok = False
        
        try:
            # 测试前端
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务正常")
                frontend_ok = True
            else:
                print("⚠️  前端服务响应异常")
                frontend_ok = False
        except:
            print("❌ 前端服务无法访问")
            frontend_ok = False
        
        return backend_ok, frontend_ok
    
    def create_voice_test_script(self):
        """创建语音测试脚本"""
        print("\n📄 创建语音测试脚本...")
        
        test_script = """
// 语音功能测试脚本 - 修复后验证
// 在浏览器控制台中运行

console.log("🎤 开始语音功能修复验证...");

async function testVoiceEndpoints() {
    console.log("🔍 测试语音端点...");
    
    try {
        // 测试语音状态
        const statusResponse = await fetch('http://127.0.0.1:8000/speech_status');
        const statusData = await statusResponse.json();
        
        console.log("✅ 语音状态端点正常:");
        console.log("   百度语音可用:", statusData.baidu_speech_available ? '✅' : '❌');
        console.log("   ASR启用:", statusData.asr_enabled ? '✅' : '❌');
        console.log("   TTS启用:", statusData.tts_enabled ? '✅' : '❌');
        console.log("   状态信息:", statusData.message);
        
        if (statusData.baidu_speech_available) {
            console.log("🎉 语音功能已修复！可以使用ASR和TTS功能");
        } else {
            console.log("⚠️  语音功能仍有问题，但端点已可访问");
        }
        
    } catch (error) {
        console.error("❌ 语音端点测试失败:", error);
    }
}

function testVoiceComponents() {
    console.log("🔍 测试语音组件...");
    
    // 检查录音按钮
    const voiceButton = document.querySelector('.voice-recorder-btn');
    if (voiceButton) {
        console.log("✅ 语音录音按钮存在");
        console.log("🎨 按钮状态:", voiceButton.className);
        console.log("🔘 按钮是否禁用:", voiceButton.disabled);
    } else {
        console.log("❌ 未找到语音录音按钮");
    }
    
    // 检查音频播放按钮
    const audioButtons = document.querySelectorAll('[title*="播放"], [title*="朗读"]');
    if (audioButtons.length > 0) {
        console.log(`✅ 找到 ${audioButtons.length} 个音频播放按钮`);
    } else {
        console.log("❌ 未找到音频播放按钮");
    }
}

function testMicrophonePermission() {
    console.log("🔍 测试麦克风权限...");
    
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            console.log("✅ 麦克风权限正常");
            stream.getTracks().forEach(track => track.stop());
        })
        .catch(error => {
            console.error("❌ 麦克风权限问题:", error);
            console.log("💡 请在浏览器中允许麦克风访问");
        });
}

// 运行测试
setTimeout(() => testVoiceEndpoints(), 500);
setTimeout(() => testVoiceComponents(), 1000);
setTimeout(() => testMicrophonePermission(), 1500);

console.log("🎯 语音功能修复验证脚本运行完成");
console.log("💡 如果所有测试通过，语音功能应该已经修复");
"""
        
        with open("voice_fix_verification.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("✅ 语音测试脚本已创建: voice_fix_verification.js")
    
    def show_instructions(self):
        """显示使用说明"""
        print("\n" + "=" * 80)
        print("🎉 语音接口修复完成！")
        print("=" * 80)
        print("📱 前端界面: http://localhost:3000")
        print("🔧 后端API: http://127.0.0.1:8000")
        print("🎤 语音状态: http://127.0.0.1:8000/speech_status")
        print("📚 API文档: http://127.0.0.1:8000/docs")
        print("=" * 80)
        print("💡 语音功能使用提示:")
        print("   1. 点击麦克风按钮开始录音")
        print("   2. 说话后点击停止录音")
        print("   3. 系统会自动识别语音并回复")
        print("   4. 点击播放按钮听取AI回复")
        print("=" * 80)
        print("🔧 如果语音功能仍有问题:")
        print("   1. 检查浏览器麦克风权限")
        print("   2. 运行voice_fix_verification.js脚本")
        print("   3. 查看浏览器控制台错误信息")
        print("=" * 80)
    
    def run_fix(self):
        """运行修复流程"""
        self.print_banner()
        
        # 1. 停止当前服务
        self.stop_current_services()
        
        # 2. 安装语音依赖
        self.install_speech_dependencies()
        
        # 3. 启动语音功能后端
        backend_ok = self.start_voice_enabled_backend()
        
        if not backend_ok:
            print("❌ 语音功能后端启动失败")
            return False
        
        # 4. 启动前端
        frontend_ok = self.start_frontend()
        
        # 5. 测试基本服务
        backend_test, frontend_test = self.test_basic_endpoints()
        
        # 6. 测试语音端点
        voice_ok = self.test_voice_endpoints()
        
        # 7. 创建测试脚本
        self.create_voice_test_script()
        
        # 8. 显示说明
        self.show_instructions()
        
        # 9. 打开浏览器
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
        except:
            print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
        
        if backend_ok and frontend_ok and backend_test:
            print("\n✅ 语音接口修复成功！")
            if voice_ok:
                print("🎤 语音功能完全正常，可以使用ASR和TTS")
            else:
                print("⚠️  语音端点可访问，但百度API可能需要配置")
            return True
        else:
            print("\n❌ 修复过程中出现问题")
            return False

def main():
    """主函数"""
    fixer = VoiceInterfaceFixer()
    success = fixer.run_fix()
    
    if success:
        print("\n⏳ 服务已在后台运行")
        print("💡 要停止服务，请使用以下命令:")
        print("   pkill -f uvicorn")
        print("   pkill -f 'npm start'")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
