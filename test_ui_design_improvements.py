#!/usr/bin/env python3
"""
UI设计改进测试脚本
验证移除输入框分界线和圆形按钮设计的效果
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class UIDesignTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("🎨 涂序彦教授数字人项目 - UI设计改进测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 验证输入框分界线已移除")
        print("   - 确认所有按钮都是圆形设计")
        print("   - 检查视觉连贯性和统一性")
        print("   - 测试按钮交互效果")
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
    
    def send_test_message(self):
        """发送测试消息"""
        print("\n📤 发送测试消息...")
        
        try:
            response = requests.post(
                f"{self.backend_url}/ask_professor",
                json={"prompt": "你好，这是UI设计测试消息"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer_length = len(result.get('answer', ''))
                print(f"✅ 测试消息发送成功，回复长度: {answer_length}字符")
                return True
            else:
                print(f"❌ 测试消息发送失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 测试消息发送异常: {e}")
            return False
    
    def create_browser_test_script(self):
        """创建浏览器测试脚本"""
        test_script = """
// UI设计改进测试脚本
// 在浏览器控制台中运行

console.log("🎨 开始UI设计改进测试...");

function testInputAreaBorder() {
    console.log("🔍 检查输入框分界线...");
    
    // 查找输入框区域
    const inputArea = document.querySelector('.chat-input-fixed');
    if (inputArea) {
        const computedStyle = getComputedStyle(inputArea);
        const borderTop = computedStyle.borderTopWidth;
        
        console.log(`📏 输入框顶部边框宽度: ${borderTop}`);
        
        if (borderTop === '0px' || borderTop === 'none') {
            console.log("✅ 输入框分界线已成功移除");
        } else {
            console.log(`⚠️ 输入框仍有顶部边框: ${borderTop}`);
        }
        
        // 检查背景色
        const backgroundColor = computedStyle.backgroundColor;
        console.log(`🎨 输入框背景色: ${backgroundColor}`);
        
    } else {
        console.log("❌ 未找到输入框区域");
    }
}

function testCircularButtons() {
    console.log("🔍 检查圆形按钮设计...");
    
    // 查找所有按钮
    const buttons = document.querySelectorAll('button');
    console.log(`🔘 找到 ${buttons.length} 个按钮`);
    
    let circularCount = 0;
    let nonCircularCount = 0;
    
    buttons.forEach((button, index) => {
        const computedStyle = getComputedStyle(button);
        const borderRadius = computedStyle.borderRadius;
        const width = button.offsetWidth;
        const height = button.offsetHeight;
        
        // 检查是否为圆形（border-radius >= 50% 或等于宽度/高度的一半）
        const isCircular = borderRadius.includes('50%') || 
                          borderRadius.includes('9999px') ||
                          (parseFloat(borderRadius) >= Math.min(width, height) / 2);
        
        if (isCircular) {
            circularCount++;
            console.log(`✅ 按钮 ${index + 1}: 圆形 (${width}x${height}, border-radius: ${borderRadius})`);
        } else {
            nonCircularCount++;
            console.log(`⚠️ 按钮 ${index + 1}: 非圆形 (${width}x${height}, border-radius: ${borderRadius})`);
        }
    });
    
    console.log(`📊 圆形按钮: ${circularCount}, 非圆形按钮: ${nonCircularCount}`);
    
    if (nonCircularCount === 0) {
        console.log("✅ 所有按钮都是圆形设计");
    } else {
        console.log(`⚠️ 还有 ${nonCircularCount} 个按钮不是圆形`);
    }
}

function testButtonInteractions() {
    console.log("🔍 测试按钮交互效果...");
    
    // 查找发送按钮
    const sendButton = document.querySelector('button[type="submit"]');
    if (sendButton) {
        console.log("✅ 找到发送按钮");
        
        // 检查hover效果
        const originalTransform = getComputedStyle(sendButton).transform;
        console.log(`🎯 发送按钮原始transform: ${originalTransform}`);
        
        // 模拟hover
        sendButton.dispatchEvent(new MouseEvent('mouseenter'));
        setTimeout(() => {
            const hoverTransform = getComputedStyle(sendButton).transform;
            console.log(`🎯 发送按钮hover transform: ${hoverTransform}`);
            
            if (hoverTransform !== originalTransform) {
                console.log("✅ 发送按钮hover效果正常");
            } else {
                console.log("⚠️ 发送按钮hover效果可能异常");
            }
            
            sendButton.dispatchEvent(new MouseEvent('mouseleave'));
        }, 100);
    }
    
    // 查找语音播放按钮
    const ttsButtons = document.querySelectorAll('button[title*="语音播放"], button[title*="播放"]');
    if (ttsButtons.length > 0) {
        console.log(`✅ 找到 ${ttsButtons.length} 个语音播放按钮`);
        
        ttsButtons.forEach((button, index) => {
            const computedStyle = getComputedStyle(button);
            console.log(`🔊 语音按钮 ${index + 1}: ${computedStyle.borderRadius}`);
        });
    }
    
    // 查找录音按钮
    const recordButtons = document.querySelectorAll('button[title*="录音"], button[title*="开始录音"]');
    if (recordButtons.length > 0) {
        console.log(`✅ 找到 ${recordButtons.length} 个录音按钮`);
        
        recordButtons.forEach((button, index) => {
            const computedStyle = getComputedStyle(button);
            console.log(`🎤 录音按钮 ${index + 1}: ${computedStyle.borderRadius}`);
        });
    }
}

function testVisualCohesion() {
    console.log("🔍 检查视觉连贯性...");
    
    // 检查聊天卡片
    const chatCard = document.querySelector('.fullscreen-chat-card');
    if (chatCard) {
        const cardStyle = getComputedStyle(chatCard);
        console.log(`📱 聊天卡片背景: ${cardStyle.backgroundColor}`);
        console.log(`📱 聊天卡片边框: ${cardStyle.border}`);
    }
    
    // 检查消息区域
    const messagesContainer = document.querySelector('.chat-messages-container');
    if (messagesContainer) {
        const messagesStyle = getComputedStyle(messagesContainer);
        console.log(`💬 消息区域背景: ${messagesStyle.backgroundColor}`);
    }
    
    // 检查输入框区域
    const inputArea = document.querySelector('.chat-input-fixed');
    if (inputArea) {
        const inputStyle = getComputedStyle(inputArea);
        console.log(`📝 输入框区域背景: ${inputStyle.backgroundColor}`);
        console.log(`📝 输入框区域边框: ${inputStyle.border}`);
        
        // 检查是否有视觉分隔
        const borderTop = inputStyle.borderTopWidth;
        if (borderTop === '0px') {
            console.log("✅ 输入框与消息区域视觉连贯，无分隔线");
        } else {
            console.log(`⚠️ 输入框仍有分隔线: ${borderTop}`);
        }
    }
}

function simulateUserInteraction() {
    console.log("🔍 模拟用户交互...");
    
    // 查找输入框
    const textarea = document.querySelector('textarea');
    if (textarea) {
        console.log("✅ 找到输入框");
        
        // 模拟输入
        textarea.value = "这是UI测试消息";
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        
        console.log("📝 模拟输入文本");
        
        // 检查发送按钮状态
        setTimeout(() => {
            const sendButton = document.querySelector('button[type="submit"]');
            if (sendButton) {
                const isDisabled = sendButton.disabled;
                console.log(`🔘 发送按钮状态: ${isDisabled ? '禁用' : '启用'}`);
                
                if (!isDisabled) {
                    console.log("✅ 输入文本后发送按钮正确启用");
                }
            }
        }, 100);
    }
}

// 运行测试
console.log("🚀 开始UI设计改进测试...");

testInputAreaBorder();

setTimeout(() => {
    testCircularButtons();
}, 500);

setTimeout(() => {
    testButtonInteractions();
}, 1000);

setTimeout(() => {
    testVisualCohesion();
}, 1500);

setTimeout(() => {
    simulateUserInteraction();
}, 2000);

console.log("🎯 UI设计改进测试脚本运行完成");
console.log("💡 请观察:");
console.log("   1. 输入框区域是否没有顶部分界线");
console.log("   2. 所有按钮是否都是圆形设计");
console.log("   3. 按钮hover效果是否正常");
console.log("   4. 整体视觉是否更加统一和谐");
"""
        
        with open("browser_ui_design_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_ui_design_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 UI设计改进测试说明")
        print("=" * 80)
        
        print("\n🎯 测试步骤:")
        print("1. 在浏览器中打开前端页面")
        print("2. 观察输入框区域是否没有顶部分界线")
        print("3. 检查所有按钮是否都是圆形设计")
        print("4. 测试按钮的hover和点击效果")
        print("5. 发送消息验证功能正常")
        
        print("\n🔍 检查要点:")
        print("✓ 输入框区域与消息区域视觉连贯")
        print("✓ 发送按钮是圆形且在输入框内")
        print("✓ 录音按钮是圆形且有hover效果")
        print("✓ 语音播放按钮是圆形且状态清晰")
        print("✓ 所有按钮尺寸一致，视觉统一")
        print("✓ 按钮hover时有缩放效果")
        
        print("\n🎨 设计改进对比:")
        print("修改前:")
        print("  - 输入框有明显的顶部分界线")
        print("  - 按钮是方形或圆角矩形")
        print("  - 视觉上有分割感")
        
        print("修改后:")
        print("  - 输入框与消息区域视觉连贯")
        print("  - 所有按钮都是圆形设计")
        print("  - 整体更加和谐统一")
        
        print("\n🛠️ 开发者工具检查:")
        print("1. Elements标签: 检查.chat-input-fixed的CSS")
        print("2. 确认border-top属性已移除或为0")
        print("3. 检查按钮的border-radius属性")
        print("4. 观察hover时的transform效果")
        
        print("\n🐛 常见问题排查:")
        print("- 如果仍有分界线: 检查CSS中的border-top")
        print("- 如果按钮不是圆形: 检查border-radius设置")
        print("- 如果hover效果异常: 检查transition属性")
        print("- 如果功能异常: 检查JavaScript事件绑定")
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败")
            return False
        
        # 2. 发送测试消息
        message_ok = self.send_test_message()
        
        # 3. 打开浏览器
        print("\n🌐 打开浏览器进行UI设计测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 4. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 5. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 UI设计改进测试准备完成！")
        print("💡 请在浏览器中验证设计改进效果")
        print(f"📊 基础功能测试: {'✅ 通过' if message_ok else '❌ 失败'}")
        
        return True

def main():
    """主函数"""
    tester = UIDesignTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
