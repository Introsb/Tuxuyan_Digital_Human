#!/usr/bin/env python3
"""
输入框区域改进测试脚本
验证输入框高度调整和按钮内部布局的效果
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class InputAreaTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("📝 涂序彦教授数字人项目 - 输入框区域改进测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 验证输入框最小高度增加到60px")
        print("   - 确认所有按钮都在输入框内部")
        print("   - 检查按钮排列顺序：录音 → 语音播放 → 发送")
        print("   - 验证输入框边距调整效果")
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
                json={"prompt": "你好，这是输入框改进测试消息"},
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
// 输入框区域改进测试脚本
// 在浏览器控制台中运行

console.log("📝 开始输入框区域改进测试...");

function testInputAreaHeight() {
    console.log("🔍 检查输入框高度...");
    
    const textarea = document.querySelector('textarea');
    if (textarea) {
        const height = textarea.offsetHeight;
        const computedStyle = getComputedStyle(textarea);
        const minHeight = computedStyle.minHeight;
        
        console.log(`📏 输入框实际高度: ${height}px`);
        console.log(`📏 输入框最小高度: ${minHeight}`);
        
        // 检查最小高度是否为60px
        if (minHeight === '60px') {
            console.log("✅ 输入框最小高度正确设置为60px");
        } else {
            console.log(`⚠️ 输入框最小高度不正确，期望: 60px，实际: ${minHeight}`);
        }
        
        // 检查最大高度
        const maxHeight = computedStyle.maxHeight;
        console.log(`📏 输入框最大高度: ${maxHeight}`);
        
        if (maxHeight === '120px') {
            console.log("✅ 输入框最大高度正确保持为120px");
        } else {
            console.log(`⚠️ 输入框最大高度异常: ${maxHeight}`);
        }
        
        // 检查内边距
        const padding = computedStyle.padding;
        const paddingRight = computedStyle.paddingRight;
        console.log(`📏 输入框内边距: ${padding}`);
        console.log(`📏 输入框右内边距: ${paddingRight}`);
        
        if (paddingRight === '128px' || paddingRight === '8rem') {
            console.log("✅ 输入框右内边距正确设置为按钮预留空间");
        } else {
            console.log(`⚠️ 输入框右内边距可能不正确: ${paddingRight}`);
        }
    } else {
        console.log("❌ 未找到输入框");
    }
}

function testButtonsInsideInput() {
    console.log("🔍 检查按钮是否在输入框内部...");
    
    const textarea = document.querySelector('textarea');
    const buttonContainer = document.querySelector('.absolute.right-2');
    
    if (textarea && buttonContainer) {
        const textareaRect = textarea.getBoundingClientRect();
        const buttonRect = buttonContainer.getBoundingClientRect();
        
        console.log(`📝 输入框位置: left=${textareaRect.left}, right=${textareaRect.right}, top=${textareaRect.top}, bottom=${textareaRect.bottom}`);
        console.log(`🔘 按钮组位置: left=${buttonRect.left}, right=${buttonRect.right}, top=${buttonRect.top}, bottom=${buttonRect.bottom}`);
        
        // 检查按钮是否在输入框内部
        const isInside = buttonRect.left >= textareaRect.left && 
                        buttonRect.right <= textareaRect.right &&
                        buttonRect.top >= textareaRect.top && 
                        buttonRect.bottom <= textareaRect.bottom;
        
        if (isInside) {
            console.log("✅ 按钮组正确位于输入框内部");
        } else {
            console.log("⚠️ 按钮组可能不在输入框内部");
        }
        
        // 检查按钮是否垂直居中
        const textareaCenterY = textareaRect.top + textareaRect.height / 2;
        const buttonCenterY = buttonRect.top + buttonRect.height / 2;
        const centerDiff = Math.abs(textareaCenterY - buttonCenterY);
        
        if (centerDiff <= 5) {
            console.log("✅ 按钮组垂直居中对齐");
        } else {
            console.log(`⚠️ 按钮组可能未垂直居中，偏差: ${centerDiff}px`);
        }
    } else {
        console.log("❌ 未找到输入框或按钮组");
    }
}

function testButtonOrder() {
    console.log("🔍 检查按钮排列顺序...");
    
    const buttonContainer = document.querySelector('.absolute.right-2');
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
    console.log("🔍 检查内部按钮尺寸...");
    
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
            
            console.log(`📏 ${name}: ${width}x${height}px`);
            
            if (targetSize === null) {
                targetSize = { width, height };
            } else if (width !== targetSize.width || height !== targetSize.height) {
                allSameSize = false;
                console.log(`⚠️ ${name} 尺寸不一致`);
            }
        } else {
            console.log(`❌ 未找到${name}`);
        }
    });
    
    if (allSameSize && targetSize) {
        console.log(`✅ 所有按钮尺寸统一: ${targetSize.width}x${targetSize.height}px`);
        
        // 检查是否为预期的32px (w-8 h-8)
        if (targetSize.width === 32 && targetSize.height === 32) {
            console.log("✅ 按钮尺寸符合内部布局预期 (32x32px, w-8 h-8)");
        } else {
            console.log(`⚠️ 按钮尺寸与预期不符，预期: 32x32px，实际: ${targetSize.width}x${targetSize.height}px`);
        }
    } else {
        console.log("❌ 按钮尺寸不统一");
    }
}

function testInputAreaPadding() {
    console.log("🔍 检查输入框区域边距...");
    
    const inputArea = document.querySelector('.chat-input-fixed');
    if (inputArea) {
        const computedStyle = getComputedStyle(inputArea);
        const paddingLeft = computedStyle.paddingLeft;
        const paddingRight = computedStyle.paddingRight;
        const paddingTop = computedStyle.paddingTop;
        const paddingBottom = computedStyle.paddingBottom;
        
        console.log(`📏 输入框区域边距:`);
        console.log(`   左边距: ${paddingLeft}`);
        console.log(`   右边距: ${paddingRight}`);
        console.log(`   上边距: ${paddingTop}`);
        console.log(`   下边距: ${paddingBottom}`);
        
        // 检查左右边距是否为24px (px-6)
        if (paddingLeft === '24px' && paddingRight === '24px') {
            console.log("✅ 输入框区域左右边距正确设置为24px (px-6)");
        } else {
            console.log(`⚠️ 输入框区域左右边距可能不正确，期望: 24px，实际: ${paddingLeft}/${paddingRight}`);
        }
        
        // 检查上下边距是否为16px (py-4)
        if (paddingTop === '16px' && paddingBottom === '16px') {
            console.log("✅ 输入框区域上下边距正确保持为16px (py-4)");
        } else {
            console.log(`⚠️ 输入框区域上下边距可能不正确，期望: 16px，实际: ${paddingTop}/${paddingBottom}`);
        }
    } else {
        console.log("❌ 未找到输入框区域");
    }
}

function testTextInputExperience() {
    console.log("🔍 测试文本输入体验...");
    
    const textarea = document.querySelector('textarea');
    if (textarea) {
        // 测试多行文本
        const testText = "这是第一行\\n这是第二行\\n这是第三行\\n这是第四行\\n这是第五行";
        
        textarea.value = testText;
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        
        setTimeout(() => {
            const height = textarea.offsetHeight;
            const scrollHeight = textarea.scrollHeight;
            
            console.log(`📝 多行文本测试:`);
            console.log(`   输入框高度: ${height}px`);
            console.log(`   滚动高度: ${scrollHeight}px`);
            
            if (height <= 120) {
                console.log("✅ 输入框高度限制正常工作");
            } else {
                console.log(`⚠️ 输入框高度超出限制: ${height}px > 120px`);
            }
            
            if (scrollHeight > height) {
                console.log("✅ 多行文本滚动功能正常");
            } else {
                console.log("ℹ️ 文本未超出可视区域，无需滚动");
            }
            
            // 清空输入框
            textarea.value = '';
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
        }, 500);
    }
}

// 运行测试
console.log("🚀 开始输入框区域改进测试...");

testInputAreaHeight();

setTimeout(() => {
    testButtonsInsideInput();
}, 500);

setTimeout(() => {
    testButtonOrder();
}, 1000);

setTimeout(() => {
    testButtonSizes();
}, 1500);

setTimeout(() => {
    testInputAreaPadding();
}, 2000);

setTimeout(() => {
    testTextInputExperience();
}, 2500);

console.log("🎯 输入框区域改进测试脚本运行完成");
console.log("💡 请观察:");
console.log("   1. 输入框最小高度是否为60px");
console.log("   2. 所有按钮是否都在输入框内部");
console.log("   3. 按钮排列顺序是否正确");
console.log("   4. 输入框区域边距是否增加");
"""
        
        with open("browser_input_area_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_input_area_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 输入框区域改进测试说明")
        print("=" * 80)
        
        print("\n🎯 测试步骤:")
        print("1. 在浏览器中打开前端页面")
        print("2. 观察输入框的高度和外观")
        print("3. 检查按钮是否都在输入框内部")
        print("4. 测试多行文本输入效果")
        print("5. 验证各按钮功能正常")
        
        print("\n🔍 检查要点:")
        print("✓ 输入框最小高度为60px（比之前的40px高50%）")
        print("✓ 输入框最大高度保持120px")
        print("✓ 所有按钮（录音、TTS、发送）都在输入框内部")
        print("✓ 按钮顺序：录音 → 语音播放 → 发送")
        print("✓ 按钮尺寸统一为32x32px (w-8 h-8)")
        print("✓ 输入框区域左右边距增加到24px")
        print("✓ 输入框右内边距为按钮预留足够空间")
        
        print("\n🎨 改进效果对比:")
        print("修改前:")
        print("  - 输入框最小高度40px")
        print("  - 按钮在输入框外部排列")
        print("  - 输入框区域边距16px")
        
        print("修改后:")
        print("  - 输入框最小高度60px，更宽敞")
        print("  - 所有按钮内置在输入框右侧")
        print("  - 输入框区域左右边距24px")
        print("  - 整体布局更紧凑统一")
        
        print("\n🛠️ 开发者工具检查:")
        print("1. Elements标签: 检查textarea的CSS样式")
        print("2. 确认min-height为60px")
        print("3. 检查按钮的absolute定位")
        print("4. 观察px-6边距效果")
        
        print("\n🐛 常见问题排查:")
        print("- 如果高度不正确: 检查min-h-[60px]类名")
        print("- 如果按钮不在内部: 检查absolute定位和right-2")
        print("- 如果按钮重叠: 检查pr-32右内边距")
        print("- 如果边距异常: 检查px-6和py-4类名")
    
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
        print("\n🌐 打开浏览器进行输入框改进测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 4. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 5. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 输入框区域改进测试准备完成！")
        print("💡 请在浏览器中验证输入框改进效果")
        print(f"📊 基础功能测试: {'✅ 通过' if message_ok else '❌ 失败'}")
        
        return True

def main():
    """主函数"""
    tester = InputAreaTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
