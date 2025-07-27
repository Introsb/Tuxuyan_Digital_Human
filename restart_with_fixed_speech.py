#!/usr/bin/env python3
"""
重启服务器并应用语音修复
"""

import subprocess
import time
import requests
import webbrowser
from pathlib import Path

def print_banner():
    """显示横幅"""
    print("=" * 80)
    print("🔧 重启服务器并应用百度语音API修复")
    print("=" * 80)
    print("🎯 修复内容:")
    print("   - 使用标准百度语音HTTP API")
    print("   - 修复ASR（语音识别）功能")
    print("   - 修复TTS（语音合成）功能")
    print("   - 确保聊天功能正常")
    print("=" * 80)

def stop_current_services():
    """停止当前服务"""
    print("\n🛑 停止当前服务...")
    
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        print("✅ 已停止uvicorn进程")
    except:
        print("⚠️  停止uvicorn进程时出现问题")
    
    time.sleep(3)
    print("⏳ 等待进程完全停止...")

def start_fixed_backend():
    """启动修复后的后端"""
    print("\n🔧 启动修复后的API服务器...")
    
    try:
        backend_process = subprocess.Popen([
            "uvicorn", "complete_api_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
        
        print("⏳ 等待修复后的后端启动...")
        time.sleep(12)  # 等待12秒，给语音API初始化时间
        
        if backend_process.poll() is None:
            print("✅ 修复后的API服务器启动成功")
            return True
        else:
            print("❌ 修复后的API服务器启动失败")
            return False
            
    except Exception as e:
        print(f"❌ 启动修复后的API服务器时出错: {e}")
        return False

def test_speech_functionality():
    """测试语音功能"""
    print("\n🧪 测试修复后的语音功能...")
    
    try:
        # 测试语音状态
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

def test_chat_functionality():
    """测试聊天功能"""
    print("\n🧪 测试聊天功能...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": "你好，请简单介绍一下自己"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天功能正常")
            print(f"📝 回复内容: {result.get('answer', '无回复')[:100]}...")
            print(f"🤖 回复来源: {result.get('source', '未知')}")
            return True
        else:
            print(f"❌ 聊天功能失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试聊天功能异常: {e}")
        return False

def test_tts_endpoint():
    """测试TTS端点"""
    print("\n🧪 测试TTS端点...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/tts",
            json={
                "text": "您好，我是涂序彦教授，语音功能已修复。",
                "voice": "zh-CN-male",
                "speed": 5,
                "pitch": 6,
                "volume": 5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"✅ TTS端点正常，音频大小: {len(audio_data)} bytes")
            
            # 保存测试音频
            with open("test_fixed_tts.wav", "wb") as f:
                f.write(audio_data)
            print("💾 测试音频已保存到: test_fixed_tts.wav")
            
            return True
        else:
            print(f"❌ TTS端点失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试TTS端点异常: {e}")
        return False

def create_verification_script():
    """创建验证脚本"""
    print("\n📄 创建语音修复验证脚本...")
    
    script_content = """
// 语音修复验证脚本
// 在浏览器控制台中运行

console.log("🔧 开始语音修复验证...");

async function testFixedSpeechAPI() {
    console.log("🔍 测试修复后的语音API...");
    
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
            console.log("🎉 百度语音API修复成功！");
            
            // 测试TTS
            console.log("🔊 测试TTS功能...");
            const ttsResponse = await fetch('http://127.0.0.1:8000/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: '语音功能修复测试',
                    voice: 'zh-CN-male',
                    speed: 5,
                    pitch: 6,
                    volume: 5
                })
            });
            
            if (ttsResponse.ok) {
                const audioBlob = await ttsResponse.blob();
                console.log(`✅ TTS测试成功，音频大小: ${audioBlob.size} bytes`);
                
                // 可以播放测试音频
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                console.log("🎵 可以播放测试音频:", audio);
            } else {
                console.error("❌ TTS测试失败:", ttsResponse.status);
            }
        } else {
            console.log("⚠️  百度语音API仍有问题");
        }
        
    } catch (error) {
        console.error("❌ 语音API测试失败:", error);
    }
}

async function testChatAPI() {
    console.log("🔍 测试聊天API...");
    
    try {
        const response = await fetch('http://127.0.0.1:8000/ask_professor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: '你好，语音功能修复了吗？'
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log("✅ 聊天API正常");
            console.log("📝 回复:", data.answer.substring(0, 100) + "...");
        } else {
            console.error("❌ 聊天API失败:", response.status);
        }
        
    } catch (error) {
        console.error("❌ 聊天API测试失败:", error);
    }
}

function testVoiceComponents() {
    console.log("🔍 测试前端语音组件...");
    
    // 检查录音按钮
    const voiceButton = document.querySelector('.voice-recorder-btn');
    if (voiceButton) {
        console.log("✅ 语音录音按钮存在");
        console.log("🎨 按钮状态:", voiceButton.className);
    } else {
        console.log("❌ 未找到语音录音按钮");
    }
    
    // 检查播放按钮
    const audioButtons = document.querySelectorAll('[title*="播放"], [title*="朗读"]');
    if (audioButtons.length > 0) {
        console.log(`✅ 找到 ${audioButtons.length} 个音频播放按钮`);
    } else {
        console.log("❌ 未找到音频播放按钮");
    }
}

// 运行测试
setTimeout(() => testFixedSpeechAPI(), 500);
setTimeout(() => testChatAPI(), 1500);
setTimeout(() => testVoiceComponents(), 2500);

console.log("🎯 语音修复验证脚本运行完成");
console.log("💡 如果所有测试通过，语音功能应该已经完全修复");
"""
    
    with open("speech_fix_verification.js", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ 验证脚本已创建: speech_fix_verification.js")

def show_results(backend_ok, speech_ok, chat_ok, tts_ok):
    """显示结果"""
    print("\n" + "=" * 80)
    print("📊 语音修复结果总结")
    print("=" * 80)
    
    results = {
        "后端启动": backend_ok,
        "语音状态": speech_ok,
        "聊天功能": chat_ok,
        "TTS功能": tts_ok
    }
    
    for test_name, result in results.items():
        status = "✅ 正常" if result else "❌ 异常"
        print(f"   {test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\n📈 总体结果: {total_passed}/{total_tests} 项测试通过")
    
    if total_passed == total_tests:
        print("🎉 语音功能修复完全成功！")
        print("🎤 ASR和TTS功能现在使用标准百度API")
        print("🤖 聊天功能正常工作")
    elif backend_ok and speech_ok:
        print("⚠️  基本功能正常，部分功能可能需要调整")
    else:
        print("❌ 修复过程中出现问题，请检查日志")
    
    print("\n🌐 服务地址:")
    print("   前端界面: http://localhost:3000")
    print("   后端API: http://127.0.0.1:8000")
    print("   语音状态: http://127.0.0.1:8000/speech_status")
    print("   API文档: http://127.0.0.1:8000/docs")

def main():
    """主函数"""
    print_banner()
    
    # 1. 停止当前服务
    stop_current_services()
    
    # 2. 启动修复后的后端
    backend_ok = start_fixed_backend()
    
    if not backend_ok:
        print("❌ 修复后的后端启动失败")
        return False
    
    # 3. 测试各项功能
    speech_ok = test_speech_functionality()
    chat_ok = test_chat_functionality()
    tts_ok = test_tts_endpoint()
    
    # 4. 创建验证脚本
    create_verification_script()
    
    # 5. 显示结果
    show_results(backend_ok, speech_ok, chat_ok, tts_ok)
    
    # 6. 打开浏览器
    try:
        webbrowser.open("http://localhost:3000")
        print("\n🌐 已在浏览器中打开项目界面")
    except:
        print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
    
    success = backend_ok and speech_ok and chat_ok
    
    if success:
        print("\n✅ 语音修复完成！现在可以正常使用语音功能")
    else:
        print("\n❌ 修复过程中出现问题")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
