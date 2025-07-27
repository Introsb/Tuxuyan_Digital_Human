#!/usr/bin/env python3
"""
按钮布局测试脚本
验证输入框区域按钮的新布局和排列顺序
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class ButtonLayoutTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("🔘 涂序彦教授数字人项目 - 按钮布局测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 验证按钮排列顺序：录音 → 语音播放 → 发送")
        print("   - 确认所有按钮尺寸统一为 w-9 h-9")
        print("   - 检查发送按钮已移到输入框外部")
        print("   - 测试按钮间距和对齐效果")
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
                json={"prompt": "你好，这是按钮布局测试消息"},
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
// 按钮布局测试脚本
// 在浏览器控制台中运行

console.log("🔘 开始按钮布局测试...");

function testButtonOrder() {
    console.log("🔍 检查按钮排列顺序...");
    
    // 查找输入框区域的按钮容器
    const buttonContainer = document.querySelector('form .flex.items-center.gap-2');
    if (buttonContainer) {
        const buttons = buttonContainer.children;
        console.log(`📊 找到 ${buttons.length} 个按钮/组件`);
        
        // 预期顺序：录音按钮组件 → TTS按钮 → 发送按钮
        const expectedOrder = ['录音', '语音播放', '发送'];
        let actualOrder = [];
        
        Array.from(buttons).forEach((element, index) => {
            if (element.tagName === 'DIV') {
                // VoiceRecorderOptimized 组件
                const recordButton = element.querySelector('button[title*="录音"]');
                if (recordButton) {
                    actualOrder.push('录音');
                    console.log(`✅ 位置 ${index + 1}: 录音按钮组件`);
                }
            } else if (element.tagName === 'BUTTON') {
                const title = element.getAttribute('title') || '';
                if (title.includes('语音播放') || title.includes('播放')) {
                    actualOrder.push('语音播放');
                    console.log(`✅ 位置 ${index + 1}: 语音播放按钮`);
                } else if (title.includes('发送') || element.type === 'submit') {
                    actualOrder.push('发送');
                    console.log(`✅ 位置 ${index + 1}: 发送按钮`);
                }
            }
        });
        
        console.log(`📋 实际顺序: ${actualOrder.join(' → ')}`);
        console.log(`📋 预期顺序: ${expectedOrder.join(' → ')}`);
        
        if (JSON.stringify(actualOrder) === JSON.stringify(expectedOrder)) {
            console.log("✅ 按钮排列顺序正确");
        } else {
            console.log("⚠️ 按钮排列顺序不符合预期");
        }
    } else {
        console.log("❌ 未找到按钮容器");
    }
}

function testButtonSizes() {
    console.log("🔍 检查按钮尺寸统一性...");
    
    // 查找所有相关按钮
    const recordButton = document.querySelector('button[title*="录音"]');
    const ttsButton = document.querySelector('button[title*="语音播放"]');
    const sendButton = document.querySelector('button[type="submit"]');
    
    const buttons = [
        { name: '录音按钮', element: recordButton },
        { name: 'TTS按钮', element: ttsButton },
        { name: '发送按钮', element: sendButton }
    ];
    
    let allSameSize = true;
    let targetSize = null;
    
    buttons.forEach(({ name, element }) => {
        if (element) {
            const width = element.offsetWidth;
            const height = element.offsetHeight;
            const computedStyle = getComputedStyle(element);
            
            console.log(`📏 ${name}: ${width}x${height}px, classes: ${element.className}`);
            
            if (targetSize === null) {
                targetSize = { width, height };
            } else if (width !== targetSize.width || height !== targetSize.height) {
                allSameSize = false;
                console.log(`⚠️ ${name} 尺寸不一致`);
            }
            
            // 检查是否为圆形
            const borderRadius = computedStyle.borderRadius;
            const isCircular = borderRadius.includes('50%') || borderRadius.includes('9999px');
            console.log(`🔘 ${name} 圆形设计: ${isCircular ? '是' : '否'} (${borderRadius})`);
        } else {
            console.log(`❌ 未找到${name}`);
        }
    });
    
    if (allSameSize && targetSize) {
        console.log(`✅ 所有按钮尺寸统一: ${targetSize.width}x${targetSize.height}px`);
        
        // 检查是否为预期的36px (w-9 h-9)
        if (targetSize.width === 36 && targetSize.height === 36) {
            console.log("✅ 按钮尺寸符合预期 (36x36px, w-9 h-9)");
        } else {
            console.log(`⚠️ 按钮尺寸与预期不符，预期: 36x36px，实际: ${targetSize.width}x${targetSize.height}px`);
        }
    } else {
        console.log("❌ 按钮尺寸不统一");
    }
}

function testSendButtonPosition() {
    console.log("🔍 检查发送按钮位置...");
    
    const sendButton = document.querySelector('button[type="submit"]');
    const textarea = document.querySelector('textarea');
    
    if (sendButton && textarea) {
        const sendRect = sendButton.getBoundingClientRect();
        const textareaRect = textarea.getBoundingClientRect();
        
        console.log(`📝 输入框位置: left=${textareaRect.left}, right=${textareaRect.right}`);
        console.log(`🔘 发送按钮位置: left=${sendRect.left}, right=${sendRect.right}`);
        
        // 检查发送按钮是否在输入框外部（右侧）
        if (sendRect.left >= textareaRect.right) {
            console.log("✅ 发送按钮已移到输入框外部");
        } else if (sendRect.left >= textareaRect.left && sendRect.right <= textareaRect.right) {
            console.log("⚠️ 发送按钮仍在输入框内部");
        } else {
            console.log("❓ 发送按钮位置不确定");
        }
        
        // 检查发送按钮是否在按钮组的最右侧
        const buttonContainer = sendButton.parentElement;
        if (buttonContainer) {
            const buttons = Array.from(buttonContainer.children);
            const sendButtonIndex = buttons.indexOf(sendButton);
            
            if (sendButtonIndex === buttons.length - 1) {
                console.log("✅ 发送按钮位于按钮组最右侧");
            } else {
                console.log(`⚠️ 发送按钮不在最右侧，当前位置: ${sendButtonIndex + 1}/${buttons.length}`);
            }
        }
    } else {
        console.log("❌ 未找到发送按钮或输入框");
    }
}

function testButtonSpacing() {
    console.log("🔍 检查按钮间距...");
    
    const buttonContainer = document.querySelector('form .flex.items-center.gap-2');
    if (buttonContainer) {
        const computedStyle = getComputedStyle(buttonContainer);
        const gap = computedStyle.gap;
        
        console.log(`📏 按钮容器间距: ${gap}`);
        
        if (gap === '8px' || gap === '0.5rem') {
            console.log("✅ 按钮间距正确 (gap-2 = 8px)");
        } else {
            console.log(`⚠️ 按钮间距可能不正确: ${gap}`);
        }
        
        // 检查对齐方式
        const alignItems = computedStyle.alignItems;
        console.log(`📐 按钮对齐方式: ${alignItems}`);
        
        if (alignItems === 'center') {
            console.log("✅ 按钮垂直居中对齐");
        }
    }
}

function testButtonInteractions() {
    console.log("🔍 测试按钮交互效果...");
    
    // 测试输入框和发送按钮的联动
    const textarea = document.querySelector('textarea');
    const sendButton = document.querySelector('button[type="submit"]');
    
    if (textarea && sendButton) {
        console.log("📝 测试输入框和发送按钮联动...");
        
        // 清空输入框
        textarea.value = '';
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        
        setTimeout(() => {
            const isDisabledEmpty = sendButton.disabled;
            console.log(`🔘 空输入时发送按钮状态: ${isDisabledEmpty ? '禁用' : '启用'}`);
            
            // 输入文本
            textarea.value = '测试文本';
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            
            setTimeout(() => {
                const isDisabledWithText = sendButton.disabled;
                console.log(`🔘 有输入时发送按钮状态: ${isDisabledWithText ? '禁用' : '启用'}`);
                
                if (isDisabledEmpty && !isDisabledWithText) {
                    console.log("✅ 发送按钮状态联动正常");
                } else {
                    console.log("⚠️ 发送按钮状态联动可能异常");
                }
            }, 100);
        }, 100);
    }
}

// 运行测试
console.log("🚀 开始按钮布局测试...");

testButtonOrder();

setTimeout(() => {
    testButtonSizes();
}, 500);

setTimeout(() => {
    testSendButtonPosition();
}, 1000);

setTimeout(() => {
    testButtonSpacing();
}, 1500);

setTimeout(() => {
    testButtonInteractions();
}, 2000);

console.log("🎯 按钮布局测试脚本运行完成");
console.log("💡 请观察:");
console.log("   1. 按钮顺序是否为：录音 → 语音播放 → 发送");
console.log("   2. 所有按钮尺寸是否统一为36x36px");
console.log("   3. 发送按钮是否已移到输入框外部");
console.log("   4. 按钮间距和对齐是否合适");
"""
        
        with open("browser_button_layout_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_button_layout_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 按钮布局测试说明")
        print("=" * 80)
        
        print("\n🎯 测试步骤:")
        print("1. 在浏览器中打开前端页面")
        print("2. 观察输入框右侧的按钮排列")
        print("3. 检查按钮顺序和尺寸统一性")
        print("4. 测试各按钮的功能和交互")
        print("5. 验证发送按钮的状态联动")
        
        print("\n🔍 检查要点:")
        print("✓ 按钮顺序：录音 → 语音播放 → 发送")
        print("✓ 所有按钮尺寸统一为36x36px (w-9 h-9)")
        print("✓ 发送按钮已移到输入框外部")
        print("✓ 按钮间距适当 (gap-2 = 8px)")
        print("✓ 按钮垂直居中对齐")
        print("✓ 所有按钮都是圆形设计")
        
        print("\n🎨 布局改进对比:")
        print("修改前:")
        print("  [输入框 + 内置发送按钮] [录音] [TTS]")
        print("  - 发送按钮在输入框内部")
        print("  - 按钮分散布局")
        
        print("修改后:")
        print("  [输入框] [录音] [TTS] [发送]")
        print("  - 所有按钮统一排列")
        print("  - 发送按钮移到外部")
        print("  - 尺寸完全统一")
        
        print("\n🛠️ 开发者工具检查:")
        print("1. Elements标签: 检查按钮容器的HTML结构")
        print("2. 确认发送按钮不在textarea内部")
        print("3. 检查所有按钮的w-9 h-9类名")
        print("4. 观察gap-2间距效果")
        
        print("\n🐛 常见问题排查:")
        print("- 如果顺序错误: 检查HTML元素的排列")
        print("- 如果尺寸不一致: 检查w-9 h-9类名")
        print("- 如果发送按钮仍在内部: 检查textarea的relative定位")
        print("- 如果间距异常: 检查gap-2类名")
    
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
        print("\n🌐 打开浏览器进行按钮布局测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 4. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 5. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 按钮布局测试准备完成！")
        print("💡 请在浏览器中验证新的按钮布局效果")
        print(f"📊 基础功能测试: {'✅ 通过' if message_ok else '❌ 失败'}")
        
        return True

def main():
    """主函数"""
    tester = ButtonLayoutTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
