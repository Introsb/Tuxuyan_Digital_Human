#!/usr/bin/env python3
"""
DeepSeek后端修复脚本
修复聊天功能不响应的问题
"""

import subprocess
import time
import sys
import requests
import webbrowser
from pathlib import Path

class DeepSeekBackendFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        
    def print_banner(self):
        """显示修复横幅"""
        print("=" * 80)
        print("🔧 DeepSeek后端修复 - 聊天功能恢复")
        print("=" * 80)
        print("🎯 修复目标:")
        print("   - 停止当前的不完整API服务器")
        print("   - 启动包含聊天+语音功能的完整API服务器")
        print("   - 验证DeepSeek聊天功能正常工作")
        print("   - 确保语音功能同时可用")
        print("=" * 80)
    
    def stop_current_services(self):
        """停止当前服务"""
        print("\n🛑 停止当前API服务...")
        
        try:
            # 停止uvicorn进程
            subprocess.run(["pkill", "-f", "uvicorn"], check=False)
            print("✅ 已停止uvicorn进程")
        except:
            print("⚠️  停止uvicorn进程时出现问题")
        
        # 等待进程完全停止
        time.sleep(3)
        print("⏳ 等待进程完全停止...")
    
    def start_complete_backend(self):
        """启动完整的后端服务器"""
        print("\n🔧 启动完整API服务器（聊天+语音）...")
        
        # 检查complete_api_server.py是否存在
        if not Path("complete_api_server.py").exists():
            print("❌ complete_api_server.py 不存在")
            return False
        
        try:
            # 使用subprocess启动后端，不等待
            backend_process = subprocess.Popen([
                "uvicorn", "complete_api_server:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload"
            ])
            
            print("⏳ 等待完整后端启动...")
            time.sleep(10)  # 等待10秒，给API初始化时间
            
            # 检查进程是否还在运行
            if backend_process.poll() is None:
                print("✅ 完整API服务器启动成功")
                return True
            else:
                print("❌ 完整API服务器启动失败")
                return False
                
        except Exception as e:
            print(f"❌ 启动完整API服务器时出错: {e}")
            return False
    
    def test_chat_functionality(self):
        """测试聊天功能"""
        print("\n🧪 测试聊天功能...")
        
        try:
            # 测试ask_professor端点
            print("🔍 测试 /ask_professor 端点...")
            response = requests.post(
                "http://127.0.0.1:8000/ask_professor",
                json={"message": "你好，请简单介绍一下自己"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ /ask_professor 端点正常")
                print(f"📝 回复内容: {result.get('answer', '无回复')[:100]}...")
                print(f"🤖 回复来源: {result.get('source', '未知')}")
                print(f"⏱️  思考时间: {result.get('thinking_time', 0):.2f}秒")
                ask_professor_ok = True
            else:
                print(f"❌ /ask_professor 端点失败，状态码: {response.status_code}")
                ask_professor_ok = False
            
            # 测试chat端点
            print("\n🔍 测试 /chat 端点...")
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"message": "你好"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ /chat 端点正常")
                print(f"📝 回复内容: {result.get('answer', '无回复')[:100]}...")
                chat_ok = True
            else:
                print(f"❌ /chat 端点失败，状态码: {response.status_code}")
                chat_ok = False
            
            return ask_professor_ok and chat_ok
                
        except Exception as e:
            print(f"❌ 测试聊天功能异常: {e}")
            return False
    
    def test_speech_functionality(self):
        """测试语音功能"""
        print("\n🧪 测试语音功能...")
        
        try:
            # 测试语音状态端点
            response = requests.get("http://127.0.0.1:8000/speech_status", timeout=10)
            
            if response.status_code == 200:
                status = response.json()
                print("✅ 语音状态端点正常")
                print(f"   百度语音可用: {'✅' if status.get('baidu_speech_available') else '❌'}")
                print(f"   ASR启用: {'✅' if status.get('asr_enabled') else '❌'}")
                print(f"   TTS启用: {'✅' if status.get('tts_enabled') else '❌'}")
                
                return status.get('baidu_speech_available', False)
            else:
                print(f"❌ 语音状态端点失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 测试语音功能异常: {e}")
            return False
    
    def test_api_status(self):
        """测试API状态"""
        print("\n🧪 测试API状态...")
        
        try:
            # 测试健康检查
            response = requests.get("http://127.0.0.1:8000/", timeout=10)
            
            if response.status_code == 200:
                status = response.json()
                print("✅ 健康检查正常")
                print(f"   服务器版本: {status.get('version', '未知')}")
                print(f"   服务器类型: {status.get('server_type', '未知')}")
                print(f"   可用功能: {status.get('features', [])}")
                
                # 测试API状态端点
                response = requests.get("http://127.0.0.1:8000/api_status", timeout=10)
                if response.status_code == 200:
                    api_status = response.json()
                    print("✅ API状态端点正常")
                    print(f"   DeepSeek可用: {'✅' if api_status.get('deepseek_available') else '❌'}")
                    print(f"   聊天启用: {'✅' if api_status.get('chat_enabled') else '❌'}")
                    print(f"   语音可用: {'✅' if api_status.get('speech_available') else '❌'}")
                    
                return True
            else:
                print(f"❌ 健康检查失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 测试API状态异常: {e}")
            return False
    
    def create_test_script(self):
        """创建测试脚本"""
        print("\n📄 创建DeepSeek后端测试脚本...")
        
        test_script = """
// DeepSeek后端功能测试脚本
// 在浏览器控制台中运行

console.log("🤖 开始DeepSeek后端功能测试...");

async function testChatEndpoints() {
    console.log("🔍 测试聊天端点...");
    
    try {
        // 测试ask_professor端点
        console.log("📤 测试 /ask_professor 端点...");
        const askResponse = await fetch('http://127.0.0.1:8000/ask_professor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: '你好，请简单介绍一下自己'
            })
        });
        
        if (askResponse.ok) {
            const askData = await askResponse.json();
            console.log("✅ /ask_professor 端点正常");
            console.log("📝 回复内容:", askData.answer.substring(0, 100) + "...");
            console.log("🤖 回复来源:", askData.source);
            console.log("⏱️  思考时间:", askData.thinking_time + "秒");
        } else {
            console.error("❌ /ask_professor 端点失败:", askResponse.status);
        }
        
        // 测试chat端点
        console.log("📤 测试 /chat 端点...");
        const chatResponse = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: '你好'
            })
        });
        
        if (chatResponse.ok) {
            const chatData = await chatResponse.json();
            console.log("✅ /chat 端点正常");
            console.log("📝 回复内容:", chatData.answer.substring(0, 100) + "...");
        } else {
            console.error("❌ /chat 端点失败:", chatResponse.status);
        }
        
    } catch (error) {
        console.error("❌ 聊天端点测试失败:", error);
    }
}

async function testAPIStatus() {
    console.log("🔍 测试API状态...");
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api_status');
        const data = await response.json();
        
        console.log("✅ API状态获取成功:");
        console.log("   DeepSeek可用:", data.deepseek_available ? '✅' : '❌');
        console.log("   聊天启用:", data.chat_enabled ? '✅' : '❌');
        console.log("   语音可用:", data.speech_available ? '✅' : '❌');
        console.log("   服务器版本:", data.server_version);
        console.log("   可用功能:", data.features);
        
    } catch (error) {
        console.error("❌ API状态测试失败:", error);
    }
}

async function testSpeechStatus() {
    console.log("🔍 测试语音状态...");
    
    try {
        const response = await fetch('http://127.0.0.1:8000/speech_status');
        const data = await response.json();
        
        console.log("✅ 语音状态获取成功:");
        console.log("   百度语音可用:", data.baidu_speech_available ? '✅' : '❌');
        console.log("   ASR启用:", data.asr_enabled ? '✅' : '❌');
        console.log("   TTS启用:", data.tts_enabled ? '✅' : '❌');
        console.log("   状态信息:", data.message);
        
    } catch (error) {
        console.error("❌ 语音状态测试失败:", error);
    }
}

// 运行测试
setTimeout(() => testAPIStatus(), 500);
setTimeout(() => testChatEndpoints(), 1000);
setTimeout(() => testSpeechStatus(), 2000);

console.log("🎯 DeepSeek后端功能测试脚本运行完成");
console.log("💡 如果所有测试通过，聊天和语音功能应该都正常");
"""
        
        with open("deepseek_backend_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("✅ 测试脚本已创建: deepseek_backend_test.js")
    
    def show_instructions(self):
        """显示使用说明"""
        print("\n" + "=" * 80)
        print("🎉 DeepSeek后端修复完成！")
        print("=" * 80)
        print("📱 前端界面: http://localhost:3000")
        print("🔧 后端API: http://127.0.0.1:8000")
        print("🤖 聊天端点: http://127.0.0.1:8000/ask_professor")
        print("🎤 语音状态: http://127.0.0.1:8000/speech_status")
        print("📚 API文档: http://127.0.0.1:8000/docs")
        print("=" * 80)
        print("💡 功能使用提示:")
        print("   1. 聊天功能：在前端输入框发送消息")
        print("   2. 语音输入：点击麦克风按钮录音")
        print("   3. 语音播放：点击消息旁的播放按钮")
        print("   4. 如有问题：运行deepseek_backend_test.js脚本")
        print("=" * 80)
    
    def run_fix(self):
        """运行修复流程"""
        self.print_banner()
        
        # 1. 停止当前服务
        self.stop_current_services()
        
        # 2. 启动完整后端
        backend_ok = self.start_complete_backend()
        
        if not backend_ok:
            print("❌ 完整API服务器启动失败")
            return False
        
        # 3. 测试API状态
        api_ok = self.test_api_status()
        
        # 4. 测试聊天功能
        chat_ok = self.test_chat_functionality()
        
        # 5. 测试语音功能
        speech_ok = self.test_speech_functionality()
        
        # 6. 创建测试脚本
        self.create_test_script()
        
        # 7. 显示说明
        self.show_instructions()
        
        # 8. 打开浏览器
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
        except:
            print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
        
        if backend_ok and api_ok and chat_ok:
            print("\n✅ DeepSeek后端修复成功！")
            print("🤖 聊天功能完全正常，可以与AI对话")
            if speech_ok:
                print("🎤 语音功能同时可用")
            else:
                print("⚠️  语音功能可能需要额外配置")
            return True
        else:
            print("\n❌ 修复过程中出现问题")
            if not chat_ok:
                print("   - 聊天功能仍有问题")
            if not speech_ok:
                print("   - 语音功能可能有问题")
            return False

def main():
    """主函数"""
    fixer = DeepSeekBackendFixer()
    success = fixer.run_fix()
    
    if success:
        print("\n⏳ 服务已在后台运行")
        print("💡 要停止服务，请使用以下命令:")
        print("   pkill -f uvicorn")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
