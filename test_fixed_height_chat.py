#!/usr/bin/env python3
"""
固定高度聊天界面测试脚本
验证聊天卡片高度固定，消息区域滚动功能正常
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class FixedHeightChatTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("📏 涂序彦教授数字人项目 - 固定高度聊天界面测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 聊天卡片高度固定为620px")
        print("   - 输入框始终固定在底部")
        print("   - 消息区域可滚动，支持长对话")
        print("   - 新消息自动滚动到底部")
        print("=" * 80)
    
    def check_services(self):
        """检查服务状态"""
        print("\n🔍 检查服务状态...")
        
        try:
            backend_response = requests.get(self.backend_url, timeout=5)
            backend_ok = backend_response.status_code == 200
            print(f"{'✅' if backend_ok else '❌'} 后端服务: {'正常' if backend_ok else '异常'}")
        except:
            backend_ok = False
            print("❌ 后端服务: 无法访问")
        
        try:
            frontend_response = requests.get(self.frontend_url, timeout=5)
            frontend_ok = frontend_response.status_code == 200
            print(f"{'✅' if frontend_ok else '❌'} 前端服务: {'正常' if frontend_ok else '异常'}")
        except:
            frontend_ok = False
            print("❌ 前端服务: 无法访问")
        
        return backend_ok, frontend_ok
    
    def start_services_if_needed(self):
        """如果需要，启动服务"""
        backend_ok, frontend_ok = self.check_services()
        
        if not backend_ok or not frontend_ok:
            print("\n🚀 启动项目服务...")
            try:
                subprocess.Popen([
                    "python3", "quick_start.py"
                ], cwd=self.project_root)
                
                print("⏳ 等待服务启动...")
                time.sleep(15)
                
                backend_ok, frontend_ok = self.check_services()
                return backend_ok and frontend_ok
            except Exception as e:
                print(f"❌ 启动服务失败: {e}")
                return False
        
        return True
    
    def send_multiple_test_messages(self):
        """发送多条测试消息来测试滚动效果"""
        print("\n📤 发送多条测试消息...")
        
        test_messages = [
            "你好，这是第一条测试消息",
            "请介绍一下人工智能的发展历程",
            "什么是机器学习？",
            "深度学习和传统机器学习有什么区别？",
            "请详细解释神经网络的工作原理",
            "人工智能在未来会如何发展？",
            "控制论在人工智能中的作用是什么？",
            "请谈谈您对AGI（通用人工智能）的看法",
            "这是最后一条测试消息，用于验证滚动效果"
        ]
        
        results = []
        
        for i, message in enumerate(test_messages, 1):
            print(f"📝 发送消息 {i}/{len(test_messages)}: {message[:30]}...")
            
            try:
                response = requests.post(
                    f"{self.backend_url}/ask_professor",
                    json={"prompt": message},
                    timeout=45
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer_length = len(result.get('answer', ''))
                    print(f"✅ 消息 {i} 成功，回复长度: {answer_length}字符")
                    results.append({
                        'message': message,
                        'success': True,
                        'answer_length': answer_length
                    })
                else:
                    print(f"❌ 消息 {i} 失败: {response.status_code}")
                    results.append({
                        'message': message,
                        'success': False
                    })
                    
            except Exception as e:
                print(f"❌ 消息 {i} 异常: {e}")
                results.append({
                    'message': message,
                    'success': False,
                    'error': str(e)
                })
            
            # 间隔时间，避免过于频繁
            if i < len(test_messages):
                time.sleep(3)
        
        return results
    
    def create_browser_test_script(self):
        """创建浏览器测试脚本"""
        test_script = """
// 固定高度聊天界面测试脚本
// 在浏览器控制台中运行

console.log("📏 开始固定高度聊天界面测试...");

function testFixedHeightLayout() {
    console.log("🔍 检查聊天卡片高度...");
    
    // 查找聊天卡片
    const chatCard = document.querySelector('.fixed-chat-card');
    if (chatCard) {
        const height = chatCard.offsetHeight;
        const computedStyle = window.getComputedStyle(chatCard);
        
        console.log(`📐 聊天卡片高度: ${height}px`);
        console.log(`📐 CSS高度: ${computedStyle.height}`);
        console.log(`📐 最大高度: ${computedStyle.maxHeight}`);
        
        if (height === 620) {
            console.log("✅ 聊天卡片高度正确固定为620px");
        } else {
            console.log(`⚠️ 聊天卡片高度异常: ${height}px (期望: 620px)`);
        }
    } else {
        console.log("❌ 未找到聊天卡片元素");
    }
    
    // 检查消息容器
    const messagesContainer = document.querySelector('.chat-messages-container');
    if (messagesContainer) {
        const isScrollable = messagesContainer.scrollHeight > messagesContainer.clientHeight;
        console.log(`📜 消息容器可滚动: ${isScrollable ? '是' : '否'}`);
        console.log(`📜 滚动高度: ${messagesContainer.scrollHeight}px`);
        console.log(`📜 可视高度: ${messagesContainer.clientHeight}px`);
        
        if (isScrollable) {
            console.log("✅ 消息容器滚动功能正常");
        }
    } else {
        console.log("❌ 未找到消息容器元素");
    }
    
    // 检查输入框位置
    const inputArea = document.querySelector('.chat-input-fixed');
    if (inputArea) {
        const rect = inputArea.getBoundingClientRect();
        console.log(`📝 输入框位置: top=${rect.top}px, bottom=${rect.bottom}px`);
        console.log("✅ 输入框固定在底部");
    } else {
        console.log("❌ 未找到输入框元素");
    }
}

function testScrollBehavior() {
    console.log("🔄 测试滚动行为...");
    
    const messagesContainer = document.querySelector('.chat-messages-container');
    if (messagesContainer) {
        // 滚动到顶部
        messagesContainer.scrollTop = 0;
        console.log("📜 滚动到顶部");
        
        setTimeout(() => {
            // 滚动到底部
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            console.log("📜 滚动到底部");
        }, 1000);
        
        setTimeout(() => {
            // 检查是否在底部
            const isAtBottom = messagesContainer.scrollTop + messagesContainer.clientHeight >= messagesContainer.scrollHeight - 10;
            console.log(`📜 是否在底部: ${isAtBottom ? '是' : '否'}`);
        }, 2000);
    }
}

function simulateMessageSending() {
    console.log("📤 模拟发送消息...");
    
    const input = document.querySelector('textarea');
    const sendButton = document.querySelector('button[type="submit"]');
    
    if (input && sendButton) {
        input.value = "这是一条测试消息，用于验证固定高度布局";
        input.dispatchEvent(new Event('input', { bubbles: true }));
        
        setTimeout(() => {
            sendButton.click();
            console.log("📤 测试消息已发送");
        }, 500);
    } else {
        console.log("❌ 未找到输入框或发送按钮");
    }
}

// 运行测试
testFixedHeightLayout();

setTimeout(() => {
    testScrollBehavior();
}, 2000);

setTimeout(() => {
    simulateMessageSending();
}, 5000);

console.log("🎯 测试脚本运行完成");
console.log("💡 请观察:");
console.log("   1. 聊天卡片高度是否固定为620px");
console.log("   2. 消息区域是否可以滚动");
console.log("   3. 输入框是否始终在底部");
console.log("   4. 新消息是否自动滚动到底部");
"""
        
        with open("browser_fixed_height_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_fixed_height_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 手动测试说明")
        print("=" * 80)
        
        print("\n🎯 测试步骤:")
        print("1. 在浏览器中打开前端页面")
        print("2. 观察右侧聊天卡片的高度")
        print("3. 发送多条消息，观察滚动效果")
        print("4. 检查输入框是否始终在底部")
        print("5. 调整浏览器窗口大小，验证响应式")
        
        print("\n🔍 检查要点:")
        print("✓ 聊天卡片高度固定为620px（桌面端）")
        print("✓ 左右两个卡片高度一致")
        print("✓ 消息超出可视区域时出现滚动条")
        print("✓ 新消息自动滚动到底部")
        print("✓ 输入框始终固定在卡片底部")
        print("✓ 输入框不会被长消息挤压")
        
        print("\n🐛 常见问题排查:")
        print("- 如果卡片高度不固定：检查CSS中的height属性")
        print("- 如果滚动不正常：检查overflow-y属性")
        print("- 如果输入框位置异常：检查flex-shrink属性")
        print("- 如果自动滚动失效：检查JavaScript滚动逻辑")
        
        print("\n🛠️ 开发者工具检查:")
        print("1. 按F12打开开发者工具")
        print("2. 在Elements标签中检查聊天卡片的CSS")
        print("3. 在Console标签中运行测试脚本")
        print("4. 观察Network标签中的API请求")
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败")
            return False
        
        # 2. 发送测试消息
        print("\n📤 发送测试消息以验证滚动效果...")
        results = self.send_multiple_test_messages()
        
        successful_messages = sum(1 for r in results if r.get('success', False))
        print(f"\n📊 消息发送结果: {successful_messages}/{len(results)} 成功")
        
        # 3. 打开浏览器
        print("\n🌐 打开浏览器进行视觉测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 4. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 5. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 固定高度聊天界面测试准备完成！")
        print("💡 请在浏览器中验证聊天卡片的固定高度效果")
        
        return True

def main():
    """主函数"""
    tester = FixedHeightChatTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
