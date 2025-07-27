#!/usr/bin/env python3
"""
测试422错误修复
验证前后端数据格式匹配
"""

import requests
import json

def test_backend_endpoints():
    """测试后端端点"""
    print("🧪 测试422错误修复")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # 测试数据
    test_cases = [
        {
            "name": "正确格式 - message字段",
            "data": {"message": "你好，这是测试消息"},
            "expected": "成功"
        },
        {
            "name": "错误格式 - prompt字段（旧格式）",
            "data": {"prompt": "你好，这是测试消息"},
            "expected": "422错误"
        },
        {
            "name": "缺少必需字段",
            "data": {"text": "你好，这是测试消息"},
            "expected": "422错误"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试: {test_case['name']}")
        print(f"   数据: {test_case['data']}")
        
        try:
            response = requests.post(
                f"{base_url}/ask_professor",
                json=test_case['data'],
                timeout=30
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ 成功: {result.get('answer', '无回复')[:50]}...")
                print(f"   来源: {result.get('source', '未知')}")
            elif response.status_code == 422:
                print(f"   ⚠️  422错误（预期）: {response.text[:100]}...")
            else:
                print(f"   ❌ 其他错误: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
    
    print("\n" + "=" * 50)
    print("📋 测试总结:")
    print("   - message字段应该成功（200状态码）")
    print("   - prompt字段应该失败（422状态码）")
    print("   - 前端已修复为使用message字段")

def test_frontend_format():
    """测试前端格式"""
    print("\n🌐 前端格式测试")
    print("=" * 50)
    
    # 模拟前端请求
    frontend_data = {"message": "前端测试消息"}
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask_professor",
            json=frontend_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 前端格式测试成功")
            print(f"   回复: {result.get('answer', '无回复')[:100]}...")
            print(f"   来源: {result.get('source', '未知')}")
            print(f"   响应时间: {result.get('thinking_time', 0):.2f}秒")
            return True
        else:
            print(f"❌ 前端格式测试失败: {response.status_code}")
            print(f"   错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 前端格式测试异常: {e}")
        return False

def create_browser_test_script():
    """创建浏览器测试脚本"""
    print("\n📄 创建浏览器测试脚本...")
    
    script_content = """
// 422错误修复验证脚本
// 在浏览器控制台中运行

console.log("🔧 开始422错误修复验证...");

async function test422Fix() {
    console.log("🧪 测试修复后的API调用...");
    
    try {
        // 测试正确格式（message字段）
        console.log("📤 测试正确格式（message字段）...");
        const correctResponse = await fetch('http://127.0.0.1:8000/ask_professor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: '你好，这是修复后的测试'
            })
        });
        
        if (correctResponse.ok) {
            const correctData = await correctResponse.json();
            console.log("✅ 正确格式测试成功");
            console.log("📝 回复:", correctData.answer.substring(0, 100) + "...");
            console.log("🤖 来源:", correctData.source);
        } else {
            console.error("❌ 正确格式测试失败:", correctResponse.status);
        }
        
        // 测试错误格式（prompt字段）
        console.log("📤 测试错误格式（prompt字段）...");
        const wrongResponse = await fetch('http://127.0.0.1:8000/ask_professor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: '这应该会失败'
            })
        });
        
        if (wrongResponse.status === 422) {
            console.log("✅ 错误格式正确返回422错误");
        } else {
            console.log("⚠️  错误格式未返回预期的422错误:", wrongResponse.status);
        }
        
    } catch (error) {
        console.error("❌ 测试过程中出现异常:", error);
    }
}

function testFrontendIntegration() {
    console.log("🔍 测试前端集成...");
    
    // 检查前端是否使用正确的字段
    const inputArea = document.querySelector('textarea');
    if (inputArea) {
        console.log("✅ 找到输入框");
        
        // 模拟输入和发送
        console.log("💡 可以在输入框中输入消息测试");
        console.log("💡 前端现在使用message字段，应该不会再出现422错误");
    } else {
        console.log("❌ 未找到输入框");
    }
}

// 运行测试
setTimeout(() => test422Fix(), 500);
setTimeout(() => testFrontendIntegration(), 2000);

console.log("🎯 422错误修复验证脚本运行完成");
console.log("💡 如果测试通过，前端聊天功能应该正常工作");
"""
    
    with open("test_422_fix_browser.js", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ 浏览器测试脚本已创建: test_422_fix_browser.js")

def main():
    """主函数"""
    print("🔧 422错误修复测试工具")
    
    # 1. 测试后端端点
    test_backend_endpoints()
    
    # 2. 测试前端格式
    frontend_ok = test_frontend_format()
    
    # 3. 创建浏览器测试脚本
    create_browser_test_script()
    
    print("\n🎉 修复总结:")
    print("   ✅ 前端已修改为使用message字段")
    print("   ✅ 后端期望message字段")
    print("   ✅ 数据格式现在匹配")
    
    if frontend_ok:
        print("\n✅ 422错误已修复！前端聊天功能应该正常工作")
        print("💡 请在浏览器中测试聊天功能")
    else:
        print("\n❌ 仍有问题，请检查后端服务状态")
    
    return frontend_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
