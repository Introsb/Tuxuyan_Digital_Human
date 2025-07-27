#!/usr/bin/env python3
"""
测试前后端连接
"""

import requests
import time
import webbrowser

def print_banner():
    """显示横幅"""
    print("=" * 80)
    print("🔗 前后端连接测试")
    print("=" * 80)
    print("🎯 测试内容:")
    print("   - 后端服务状态")
    print("   - 前端服务状态")
    print("   - API端点连接")
    print("   - 聊天功能测试")
    print("   - 语音功能测试")
    print("=" * 80)

def test_backend_health():
    """测试后端健康状态"""
    print("\n🔧 测试后端健康状态...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 后端服务正常")
            print(f"   版本: {data.get('version', '未知')}")
            print(f"   功能: {data.get('features', [])}")
            print(f"   时间戳: {data.get('timestamp', '未知')}")
            return True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 后端服务无法访问: {e}")
        return False

def test_frontend_health():
    """测试前端健康状态"""
    print("\n🌐 测试前端健康状态...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        
        if response.status_code == 200:
            print("✅ 前端服务正常")
            print(f"   页面大小: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 前端服务无法访问: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🧪 测试API端点...")
    
    endpoints = [
        ("/", "健康检查"),
        ("/api_status", "API状态"),
        ("/speech_status", "语音状态")
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://127.0.0.1:8000{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description} ({endpoint}): 正常")
                results[endpoint] = True
            else:
                print(f"❌ {description} ({endpoint}): 状态码 {response.status_code}")
                results[endpoint] = False
                
        except Exception as e:
            print(f"❌ {description} ({endpoint}): 异常 {e}")
            results[endpoint] = False
    
    return all(results.values())

def test_chat_api():
    """测试聊天API"""
    print("\n💬 测试聊天API...")
    
    try:
        test_message = "你好，这是前后端连接测试"
        
        print(f"📤 发送消息: {test_message}")
        
        response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": test_message},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 聊天API正常")
            print(f"   AI回复: {result.get('answer', '无回复')[:80]}...")
            print(f"   回复来源: {result.get('source', '未知')}")
            print(f"   响应时间: {result.get('thinking_time', 0):.2f}秒")
            return True
        elif response.status_code == 422:
            print("❌ 聊天API 422错误（数据格式问题）")
            print(f"   错误详情: {response.text}")
            return False
        else:
            print(f"❌ 聊天API异常: {response.status_code}")
            print(f"   错误详情: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天API测试失败: {e}")
        return False

def test_tts_api():
    """测试TTS API"""
    print("\n🔊 测试TTS API...")
    
    try:
        test_text = "前后端连接测试成功"
        
        print(f"📤 发送TTS请求: {test_text}")
        
        response = requests.post(
            "http://127.0.0.1:8000/tts",
            json={
                "text": test_text,
                "voice": "zh-CN-male",
                "speed": 6,
                "pitch": 6,
                "volume": 5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"✅ TTS API正常，音频大小: {len(audio_data)} bytes")
            
            # 保存测试音频
            with open("test_connection_tts.wav", "wb") as f:
                f.write(audio_data)
            print("💾 测试音频已保存到: test_connection_tts.wav")
            
            return True
        else:
            print(f"❌ TTS API异常: {response.status_code}")
            print(f"   错误详情: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ TTS API测试失败: {e}")
        return False

def create_browser_test_script():
    """创建浏览器测试脚本"""
    print("\n📄 创建浏览器测试脚本...")
    
    script_content = """
// 前后端连接测试脚本
// 在浏览器控制台中运行

console.log("🔗 开始前后端连接测试...");

async function testBackendConnection() {
    console.log("🔧 测试后端连接...");
    
    try {
        // 测试健康检查
        const healthResponse = await fetch('http://127.0.0.1:8000/');
        if (healthResponse.ok) {
            const healthData = await healthResponse.json();
            console.log("✅ 后端健康检查正常");
            console.log("   版本:", healthData.version);
            console.log("   功能:", healthData.features);
        } else {
            console.error("❌ 后端健康检查失败:", healthResponse.status);
            return false;
        }
        
        // 测试聊天API
        console.log("💬 测试聊天API...");
        const chatResponse = await fetch('http://127.0.0.1:8000/ask_professor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: '浏览器前后端连接测试'
            })
        });
        
        if (chatResponse.ok) {
            const chatData = await chatResponse.json();
            console.log("✅ 聊天API正常");
            console.log("   回复:", chatData.answer.substring(0, 100) + "...");
            console.log("   来源:", chatData.source);
        } else {
            console.error("❌ 聊天API失败:", chatResponse.status);
            return false;
        }
        
        return true;
        
    } catch (error) {
        console.error("❌ 后端连接测试失败:", error);
        return false;
    }
}

async function testFrontendFeatures() {
    console.log("🌐 测试前端功能...");
    
    // 检查输入框
    const textarea = document.querySelector('textarea');
    if (textarea) {
        console.log("✅ 找到输入框");
        console.log("   占位符:", textarea.placeholder);
        console.log("   当前值:", textarea.value);
    } else {
        console.log("❌ 未找到输入框");
    }
    
    // 检查发送按钮
    const sendButton = document.querySelector('button[type="submit"], button[title*="发送"]');
    if (sendButton) {
        console.log("✅ 找到发送按钮");
    } else {
        console.log("❌ 未找到发送按钮");
    }
    
    // 检查音频控件
    const audioButtons = document.querySelectorAll('button[title*="播放"], button[title*="暂停"]');
    if (audioButtons.length > 0) {
        console.log(`✅ 找到 ${audioButtons.length} 个音频控件`);
    } else {
        console.log("❌ 未找到音频控件");
    }
    
    // 检查消息列表
    const messageList = document.querySelector('.message-list, .chat-area');
    if (messageList) {
        console.log("✅ 找到消息列表容器");
    } else {
        console.log("❌ 未找到消息列表容器");
    }
}

async function simulateUserInteraction() {
    console.log("🎭 模拟用户交互...");
    
    const textarea = document.querySelector('textarea');
    const sendButton = document.querySelector('button[type="submit"], button[title*="发送"]');
    
    if (textarea && sendButton) {
        console.log("📝 模拟输入消息...");
        
        // 模拟输入
        textarea.value = "前后端连接测试 - 浏览器模拟";
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        
        console.log("💡 提示: 可以点击发送按钮测试完整流程");
        console.log("💡 或者手动输入消息进行测试");
        
    } else {
        console.log("❌ 无法找到输入框或发送按钮");
    }
}

// 运行测试
setTimeout(() => testBackendConnection(), 500);
setTimeout(() => testFrontendFeatures(), 1500);
setTimeout(() => simulateUserInteraction(), 2500);

console.log("🎯 前后端连接测试脚本运行完成");
console.log("💡 请手动测试发送消息和语音功能");
"""
    
    with open("frontend_backend_test.js", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ 浏览器测试脚本已创建: frontend_backend_test.js")

def show_connection_results(backend_ok, frontend_ok, endpoints_ok, chat_ok, tts_ok):
    """显示连接测试结果"""
    print("\n" + "=" * 80)
    print("📊 前后端连接测试结果")
    print("=" * 80)
    
    tests = {
        "后端服务": backend_ok,
        "前端服务": frontend_ok,
        "API端点": endpoints_ok,
        "聊天功能": chat_ok,
        "TTS功能": tts_ok
    }
    
    for test_name, status in tests.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"   {test_name}: {status_text}")
    
    total_passed = sum(tests.values())
    total_tests = len(tests)
    
    print(f"\n📈 连接测试: {total_passed}/{total_tests} 项正常")
    
    if total_passed == total_tests:
        print("🎉 前后端连接完全正常！")
        print("🔗 所有API调用都可以正常工作")
        status_level = "完美"
    elif total_passed >= 4:
        print("✅ 前后端连接基本正常")
        print("🔗 主要功能可以正常使用")
        status_level = "良好"
    elif total_passed >= 2:
        print("⚠️  前后端连接部分正常")
        print("🔗 部分功能可能有问题")
        status_level = "一般"
    else:
        print("❌ 前后端连接存在严重问题")
        status_level = "异常"
    
    print(f"🏆 连接状态: {status_level}")
    
    print("\n🌐 服务地址:")
    print("   前端界面: http://localhost:3000")
    print("   后端API: http://127.0.0.1:8000")
    print("   API文档: http://127.0.0.1:8000/docs")
    
    print("\n💡 使用建议:")
    if chat_ok:
        print("   ✅ 可以正常进行聊天对话")
    if tts_ok:
        print("   ✅ 可以正常使用语音播放")
    
    print("\n🧪 进一步测试:")
    print("   - 在浏览器中运行 frontend_backend_test.js")
    print("   - 手动发送消息测试完整流程")
    print("   - 测试语音输入和播放功能")
    
    return total_passed >= 3

def main():
    """主函数"""
    print_banner()
    
    # 1. 测试后端健康状态
    backend_ok = test_backend_health()
    
    # 2. 测试前端健康状态
    frontend_ok = test_frontend_health()
    
    # 3. 测试API端点
    endpoints_ok = test_api_endpoints() if backend_ok else False
    
    # 4. 测试聊天API
    chat_ok = test_chat_api() if backend_ok else False
    
    # 5. 测试TTS API
    tts_ok = test_tts_api() if backend_ok else False
    
    # 6. 创建浏览器测试脚本
    create_browser_test_script()
    
    # 7. 显示结果
    success = show_connection_results(backend_ok, frontend_ok, endpoints_ok, chat_ok, tts_ok)
    
    # 8. 打开浏览器
    if success:
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
            print("💡 请测试发送消息功能验证前后端连接")
        except:
            print("\n⚠️  无法自动打开浏览器")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
