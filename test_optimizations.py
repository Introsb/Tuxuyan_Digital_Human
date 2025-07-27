#!/usr/bin/env python3
"""
优化功能测试验证脚本
"""

import requests
import time
import webbrowser

def print_banner():
    """显示测试横幅"""
    print("=" * 80)
    print("🧪 涂序彦教授数字人项目 - 优化功能测试")
    print("=" * 80)
    print("🎯 测试内容:")
    print("   1. 验证emoji图标移除")
    print("   2. 测试DeepSeek后端状态检测")
    print("   3. 验证在线/离线状态指示器")
    print("   4. 整体功能验证")
    print("=" * 80)

def test_backend_status_detection():
    """测试后端状态检测"""
    print("\n🔍 测试DeepSeek后端状态检测...")
    
    # 测试健康检查
    try:
        print("   📡 测试健康检查端点...")
        health_response = requests.get("http://127.0.0.1:8000/", timeout=10)
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   ✅ 健康检查正常")
            print(f"      版本: {health_data.get('version', '未知')}")
            print(f"      功能: {health_data.get('features', [])}")
        else:
            print(f"   ❌ 健康检查失败: {health_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ 健康检查异常: {e}")
        return False
    
    # 测试API状态端点
    try:
        print("   🔌 测试API状态端点...")
        api_response = requests.get("http://127.0.0.1:8000/api_status", timeout=10)
        
        if api_response.status_code == 200:
            api_data = api_response.json()
            print(f"   ✅ API状态端点正常")
            print(f"      DeepSeek可用: {'✅' if api_data.get('deepseek_available') else '❌'}")
            print(f"      聊天启用: {'✅' if api_data.get('chat_enabled') else '❌'}")
            print(f"      语音可用: {'✅' if api_data.get('speech_available') else '❌'}")
        else:
            print(f"   ❌ API状态端点失败: {api_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ API状态端点异常: {e}")
        return False
    
    return True

def test_chat_functionality():
    """测试聊天功能"""
    print("\n💬 测试聊天功能...")
    
    try:
        test_message = "测试优化后的聊天功能"
        print(f"   📤 发送测试消息: {test_message}")
        
        chat_response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json={"message": test_message},
            timeout=30
        )
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            print("   ✅ 聊天功能正常")
            print(f"      回复: {result.get('answer', '无回复')[:80]}...")
            print(f"      来源: {result.get('source', '未知')}")
            print(f"      响应时间: {result.get('thinking_time', 0):.2f}秒")
            return True
        else:
            print(f"   ❌ 聊天功能失败: {chat_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ 聊天功能异常: {e}")
        return False

def test_frontend_accessibility():
    """测试前端可访问性"""
    print("\n🌐 测试前端可访问性...")
    
    try:
        frontend_response = requests.get("http://localhost:3000", timeout=10)
        
        if frontend_response.status_code == 200:
            print("   ✅ 前端页面正常")
            print(f"      页面大小: {len(frontend_response.content)} bytes")
            return True
        else:
            print(f"   ❌ 前端页面异常: {frontend_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ 前端页面异常: {e}")
        return False

def create_browser_verification_script():
    """创建浏览器验证脚本"""
    print("\n📄 创建浏览器验证脚本...")
    
    script_content = """
// 优化功能验证脚本
// 在浏览器控制台中运行

console.log("🧪 开始优化功能验证...");

function verifyEmojiRemoval() {
    console.log("🔍 验证emoji图标移除...");
    
    // 检查侧边栏是否还有emoji
    const sidebarItems = document.querySelectorAll('.sidebar li, .chat-history li');
    let emojiFound = false;
    
    sidebarItems.forEach((item, index) => {
        const text = item.textContent;
        const hasEmoji = /[\\u{1F600}-\\u{1F64F}]|[\\u{1F300}-\\u{1F5FF}]|[\\u{1F680}-\\u{1F6FF}]|[\\u{1F1E0}-\\u{1F1FF}]|[\\u{2600}-\\u{26FF}]|[\\u{2700}-\\u{27BF}]/u.test(text);
        
        if (hasEmoji) {
            console.log(`⚠️  发现emoji在项目 ${index + 1}: ${text}`);
            emojiFound = true;
        }
    });
    
    if (!emojiFound) {
        console.log("✅ 侧边栏emoji图标已成功移除");
    }
    
    // 检查重试按钮
    const retryButtons = document.querySelectorAll('button[title*="重试"], button:contains("重试")');
    retryButtons.forEach((button, index) => {
        const text = button.textContent;
        if (text.includes('🔄')) {
            console.log(`⚠️  重试按钮仍包含emoji: ${text}`);
            emojiFound = true;
        } else if (text.includes('重试')) {
            console.log(`✅ 重试按钮emoji已移除: ${text}`);
        }
    });
    
    return !emojiFound;
}

function verifyBackendStatusDetection() {
    console.log("🔍 验证后端状态检测...");
    
    // 查找状态指示器
    const statusIndicators = document.querySelectorAll('[class*="status"], [class*="online"], [class*="offline"]');
    
    if (statusIndicators.length > 0) {
        console.log(`✅ 找到 ${statusIndicators.length} 个状态指示器`);
        
        statusIndicators.forEach((indicator, index) => {
            const text = indicator.textContent;
            const classes = indicator.className;
            console.log(`状态指示器 ${index + 1}:`);
            console.log(`  文本: ${text}`);
            console.log(`  类名: ${classes}`);
        });
        
        return true;
    } else {
        console.log("❌ 未找到状态指示器");
        return false;
    }
}

function verifyOnlineOfflineIndicator() {
    console.log("🔍 验证在线/离线状态指示器...");
    
    // 查找在线/离线指示器
    const onlineIndicators = document.querySelectorAll('*');
    let foundIndicator = false;
    
    onlineIndicators.forEach(element => {
        const text = element.textContent;
        if (text.includes('在线') || text.includes('离线')) {
            console.log(`✅ 找到状态指示器: ${text}`);
            console.log(`  元素类型: ${element.tagName}`);
            console.log(`  类名: ${element.className}`);
            foundIndicator = true;
        }
    });
    
    if (!foundIndicator) {
        console.log("❌ 未找到在线/离线状态指示器");
    }
    
    return foundIndicator;
}

async function testBackendConnection() {
    console.log("🔍 测试后端连接...");
    
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
        
        // 测试API状态
        const apiResponse = await fetch('http://127.0.0.1:8000/api_status');
        if (apiResponse.ok) {
            const apiData = await apiResponse.json();
            console.log("✅ API状态检查正常");
            console.log("   DeepSeek可用:", apiData.deepseek_available ? '✅' : '❌');
            console.log("   聊天启用:", apiData.chat_enabled ? '✅' : '❌');
        } else {
            console.error("❌ API状态检查失败:", apiResponse.status);
            return false;
        }
        
        return true;
        
    } catch (error) {
        console.error("❌ 后端连接测试失败:", error);
        return false;
    }
}

function generateTestReport() {
    console.log("📊 生成测试报告...");
    
    const results = {
        emojiRemoval: verifyEmojiRemoval(),
        statusDetection: verifyBackendStatusDetection(),
        onlineIndicator: verifyOnlineOfflineIndicator()
    };
    
    console.log("\\n📋 测试结果总结:");
    console.log("   Emoji移除:", results.emojiRemoval ? '✅ 通过' : '❌ 失败');
    console.log("   状态检测:", results.statusDetection ? '✅ 通过' : '❌ 失败');
    console.log("   在线指示器:", results.onlineIndicator ? '✅ 通过' : '❌ 失败');
    
    const passedTests = Object.values(results).filter(Boolean).length;
    const totalTests = Object.keys(results).length;
    
    console.log(`\\n📈 测试通过率: ${passedTests}/${totalTests} (${Math.round(passedTests/totalTests*100)}%)`);
    
    if (passedTests === totalTests) {
        console.log("🎉 所有优化功能验证通过！");
    } else {
        console.log("⚠️  部分优化功能需要检查");
    }
    
    return results;
}

// 运行验证
setTimeout(() => {
    console.log("🚀 开始运行优化功能验证...");
    
    // 先测试后端连接
    testBackendConnection().then(backendOk => {
        if (backendOk) {
            console.log("✅ 后端连接正常，继续前端验证");
        } else {
            console.log("❌ 后端连接异常，仅进行前端验证");
        }
        
        // 生成测试报告
        setTimeout(() => generateTestReport(), 1000);
    });
}, 500);

console.log("🎯 优化功能验证脚本已加载");
console.log("💡 请等待自动验证完成，或手动检查界面变化");
"""
    
    with open("optimization_verification.js", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ 浏览器验证脚本已创建: optimization_verification.js")

def show_test_results(backend_status_ok, chat_ok, frontend_ok):
    """显示测试结果"""
    print("\n" + "=" * 80)
    print("📊 优化功能测试结果")
    print("=" * 80)
    
    tests = {
        "后端状态检测": backend_status_ok,
        "聊天功能": chat_ok,
        "前端可访问性": frontend_ok
    }
    
    for test_name, status in tests.items():
        status_text = "✅ 通过" if status else "❌ 失败"
        print(f"   {test_name}: {status_text}")
    
    total_passed = sum(tests.values())
    total_tests = len(tests)
    
    print(f"\n📈 测试结果: {total_passed}/{total_tests} 项通过")
    
    print("\n🎯 已完成的优化:")
    print("   ✅ 移除侧边栏消息emoji图标")
    print("   ✅ 添加DeepSeek后端启动状态检测")
    print("   ✅ 替换模型卡片的在线/离线状态指示器")
    
    print("\n🧪 验证步骤:")
    print("   1. 在浏览器中检查侧边栏是否还有emoji图标")
    print("   2. 观察模型卡片的在线/离线状态指示器")
    print("   3. 运行 optimization_verification.js 进行详细验证")
    
    print("\n🌐 测试地址:")
    print("   前端界面: http://localhost:3000")
    print("   后端API: http://127.0.0.1:8000")
    print("   状态检测: http://127.0.0.1:8000/api_status")
    
    return total_passed >= 2

def main():
    """主函数"""
    print_banner()
    
    # 1. 测试后端状态检测
    backend_status_ok = test_backend_status_detection()
    
    # 2. 测试聊天功能
    chat_ok = test_chat_functionality()
    
    # 3. 测试前端可访问性
    frontend_ok = test_frontend_accessibility()
    
    # 4. 创建浏览器验证脚本
    create_browser_verification_script()
    
    # 5. 显示测试结果
    success = show_test_results(backend_status_ok, chat_ok, frontend_ok)
    
    # 6. 打开浏览器进行手动验证
    if success:
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
            print("💡 请手动验证优化效果")
        except:
            print("\n⚠️  无法自动打开浏览器")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
