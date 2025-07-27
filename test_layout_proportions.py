#!/usr/bin/env python3
"""
布局比例测试脚本
验证数字人卡片9:16比例和黄金比例宽度关系
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class LayoutProportionTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("📐 涂序彦教授数字人项目 - 布局比例测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 验证数字人卡片9:16竖屏比例")
        print("   - 确认黄金比例宽度关系 (0.382:1)")
        print("   - 检查响应式布局适配")
        print("   - 验证数字人内容正确显示")
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
                json={"prompt": "你好，这是布局比例测试消息"},
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
// 布局比例测试脚本
// 在浏览器控制台中运行

console.log("📐 开始布局比例测试...");

function testGoldenRatioLayout() {
    console.log("🔍 检查黄金比例布局...");
    
    const digitalHumanContainer = document.querySelector('.digital-human-container');
    const chatContainer = document.querySelector('.chat-container');
    
    if (digitalHumanContainer && chatContainer) {
        const digitalWidth = digitalHumanContainer.offsetWidth;
        const chatWidth = chatContainer.offsetWidth;
        const totalWidth = digitalWidth + chatWidth;
        
        console.log(`📏 数字人卡片宽度: ${digitalWidth}px`);
        console.log(`📏 聊天卡片宽度: ${chatWidth}px`);
        console.log(`📏 总宽度: ${totalWidth}px`);
        
        // 计算实际比例
        const actualRatio = digitalWidth / chatWidth;
        const goldenRatio = 0.382; // 黄金比例的较小部分
        const tolerance = 0.05; // 5% 容差
        
        console.log(`📊 实际宽度比例: ${actualRatio.toFixed(3)} (数字人:聊天)`);
        console.log(`📊 目标黄金比例: ${goldenRatio.toFixed(3)}`);
        console.log(`📊 比例差异: ${Math.abs(actualRatio - goldenRatio).toFixed(3)}`);
        
        if (Math.abs(actualRatio - goldenRatio) <= tolerance) {
            console.log("✅ 宽度比例符合黄金比例");
        } else {
            console.log(`⚠️ 宽度比例偏离黄金比例，差异: ${((Math.abs(actualRatio - goldenRatio) / goldenRatio) * 100).toFixed(1)}%`);
        }
        
        // 检查百分比
        const digitalPercent = (digitalWidth / totalWidth) * 100;
        const chatPercent = (chatWidth / totalWidth) * 100;
        
        console.log(`📊 数字人卡片占比: ${digitalPercent.toFixed(1)}%`);
        console.log(`📊 聊天卡片占比: ${chatPercent.toFixed(1)}%`);
        
        // 理论上数字人应该占约27.6% (0.382 / (0.382 + 1))
        const expectedDigitalPercent = 27.6;
        if (Math.abs(digitalPercent - expectedDigitalPercent) <= 3) {
            console.log("✅ 数字人卡片占比符合黄金比例");
        } else {
            console.log(`⚠️ 数字人卡片占比偏离预期: ${digitalPercent.toFixed(1)}% vs ${expectedDigitalPercent}%`);
        }
    } else {
        console.log("❌ 未找到布局容器");
    }
}

function testDigitalHumanAspectRatio() {
    console.log("🔍 检查数字人卡片9:16比例...");
    
    const digitalHumanCard = document.querySelector('.digital-human-card');
    
    if (digitalHumanCard) {
        const width = digitalHumanCard.offsetWidth;
        const height = digitalHumanCard.offsetHeight;
        
        console.log(`📏 数字人卡片尺寸: ${width}x${height}px`);
        
        // 计算实际宽高比
        const actualRatio = width / height;
        const targetRatio = 9 / 16; // 0.5625
        const tolerance = 0.05; // 5% 容差
        
        console.log(`📊 实际宽高比: ${actualRatio.toFixed(4)} (${width}:${height})`);
        console.log(`📊 目标9:16比例: ${targetRatio.toFixed(4)}`);
        console.log(`📊 比例差异: ${Math.abs(actualRatio - targetRatio).toFixed(4)}`);
        
        if (Math.abs(actualRatio - targetRatio) <= tolerance) {
            console.log("✅ 数字人卡片比例符合9:16");
        } else {
            console.log(`⚠️ 数字人卡片比例偏离9:16，差异: ${((Math.abs(actualRatio - targetRatio) / targetRatio) * 100).toFixed(1)}%`);
        }
        
        // 检查CSS aspect-ratio属性
        const computedStyle = getComputedStyle(digitalHumanCard);
        const aspectRatio = computedStyle.aspectRatio;
        console.log(`🎨 CSS aspect-ratio: ${aspectRatio}`);
        
        if (aspectRatio === '9 / 16' || aspectRatio === '0.5625') {
            console.log("✅ CSS aspect-ratio正确设置");
        } else {
            console.log(`⚠️ CSS aspect-ratio可能不正确: ${aspectRatio}`);
        }
    } else {
        console.log("❌ 未找到数字人卡片");
    }
}

function testDigitalHumanContent() {
    console.log("🔍 检查数字人内容显示...");
    
    const digitalHumanContent = document.querySelector('.digital-human-content');
    
    if (digitalHumanContent) {
        const contentHeight = digitalHumanContent.offsetHeight;
        const parentHeight = digitalHumanContent.parentElement.offsetHeight;
        
        console.log(`📏 数字人内容高度: ${contentHeight}px`);
        console.log(`📏 父容器高度: ${parentHeight}px`);
        
        // 检查内容是否适应容器
        if (contentHeight <= parentHeight) {
            console.log("✅ 数字人内容适应容器高度");
        } else {
            console.log(`⚠️ 数字人内容超出容器: ${contentHeight}px > ${parentHeight}px`);
        }
        
        // 检查关键元素是否存在
        const teamLogo = digitalHumanContent.querySelector('img[alt*="实践团徽"]');
        const professorEmoji = digitalHumanContent.querySelector('.text-6xl, .md\\\\:text-7xl, .lg\\\\:text-8xl');
        const professorName = digitalHumanContent.querySelector('h2');
        
        console.log(`🏷️ 团队徽标: ${teamLogo ? '✅ 存在' : '❌ 缺失'}`);
        console.log(`👨‍🏫 教授头像: ${professorEmoji ? '✅ 存在' : '❌ 缺失'}`);
        console.log(`📝 教授姓名: ${professorName ? '✅ 存在' : '❌ 缺失'}`);
        
        if (professorEmoji) {
            const emojiSize = getComputedStyle(professorEmoji).fontSize;
            console.log(`👨‍🏫 教授头像大小: ${emojiSize}`);
        }
    } else {
        console.log("❌ 未找到数字人内容");
    }
}

function testResponsiveLayout() {
    console.log("🔍 检查响应式布局...");
    
    const width = window.innerWidth;
    let breakpoint = "";
    
    if (width >= 1024) {
        breakpoint = "桌面端 (≥1024px)";
    } else if (width >= 768) {
        breakpoint = "平板端 (768-1023px)";
    } else {
        breakpoint = "移动端 (<768px)";
    }
    
    console.log(`📱 当前断点: ${breakpoint} (宽度: ${width}px)`);
    
    const goldenRatioLayout = document.querySelector('.golden-ratio-layout');
    if (goldenRatioLayout) {
        const computedStyle = getComputedStyle(goldenRatioLayout);
        const flexDirection = computedStyle.flexDirection;
        
        console.log(`📐 布局方向: ${flexDirection}`);
        
        if (width >= 1024) {
            if (flexDirection === 'row') {
                console.log("✅ 桌面端使用水平布局");
            } else {
                console.log("⚠️ 桌面端应该使用水平布局");
            }
        } else {
            if (flexDirection === 'column') {
                console.log("✅ 移动端使用垂直布局");
            } else {
                console.log("⚠️ 移动端应该使用垂直布局");
            }
        }
    }
    
    // 检查数字人卡片在不同断点的比例
    const digitalHumanCard = document.querySelector('.digital-human-card');
    if (digitalHumanCard) {
        const computedStyle = getComputedStyle(digitalHumanCard);
        const aspectRatio = computedStyle.aspectRatio;
        
        console.log(`📐 当前aspect-ratio: ${aspectRatio}`);
        
        if (width >= 1024) {
            if (aspectRatio === '9 / 16' || aspectRatio === '0.5625') {
                console.log("✅ 桌面端使用9:16比例");
            }
        } else if (width >= 768) {
            if (aspectRatio === '16 / 9' || aspectRatio === '1.7778') {
                console.log("✅ 平板端使用16:9比例");
            }
        } else {
            if (aspectRatio === '4 / 3' || aspectRatio === '1.3333') {
                console.log("✅ 移动端使用4:3比例");
            }
        }
    }
}

function testLayoutStability() {
    console.log("🔍 测试布局稳定性...");
    
    // 模拟窗口大小变化
    const originalWidth = window.innerWidth;
    console.log(`📏 原始窗口宽度: ${originalWidth}px`);
    
    // 监听resize事件
    let resizeCount = 0;
    const resizeHandler = () => {
        resizeCount++;
        console.log(`🔄 窗口大小变化 ${resizeCount}: ${window.innerWidth}x${window.innerHeight}`);
        
        // 重新检查比例
        setTimeout(() => {
            const digitalHumanContainer = document.querySelector('.digital-human-container');
            const chatContainer = document.querySelector('.chat-container');
            
            if (digitalHumanContainer && chatContainer) {
                const digitalWidth = digitalHumanContainer.offsetWidth;
                const chatWidth = chatContainer.offsetWidth;
                const ratio = digitalWidth / chatWidth;
                
                console.log(`📊 调整后宽度比例: ${ratio.toFixed(3)}`);
            }
        }, 100);
        
        if (resizeCount >= 3) {
            window.removeEventListener('resize', resizeHandler);
            console.log("✅ 布局稳定性测试完成");
        }
    };
    
    window.addEventListener('resize', resizeHandler);
    
    console.log("💡 请手动调整浏览器窗口大小来测试布局稳定性");
}

// 运行测试
console.log("🚀 开始布局比例测试...");

testGoldenRatioLayout();

setTimeout(() => {
    testDigitalHumanAspectRatio();
}, 500);

setTimeout(() => {
    testDigitalHumanContent();
}, 1000);

setTimeout(() => {
    testResponsiveLayout();
}, 1500);

setTimeout(() => {
    testLayoutStability();
}, 2000);

console.log("🎯 布局比例测试脚本运行完成");
console.log("💡 请观察:");
console.log("   1. 数字人卡片是否为9:16竖屏比例");
console.log("   2. 宽度比例是否符合黄金比例 (0.382:1)");
console.log("   3. 数字人内容是否正确显示");
console.log("   4. 响应式布局是否正常工作");
"""
        
        with open("browser_layout_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_layout_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 布局比例测试说明")
        print("=" * 80)
        
        print("\n🎯 测试步骤:")
        print("1. 在浏览器中打开前端页面")
        print("2. 观察数字人卡片的宽高比例")
        print("3. 检查两个卡片的宽度比例关系")
        print("4. 调整浏览器窗口大小测试响应式")
        print("5. 验证数字人内容显示正常")
        
        print("\n🔍 检查要点:")
        print("✓ 数字人卡片宽高比为9:16（竖屏比例）")
        print("✓ 数字人卡片宽度 : 聊天卡片宽度 ≈ 0.382:1（黄金比例）")
        print("✓ 数字人卡片占总宽度约27.6%")
        print("✓ 聊天卡片占总宽度约72.4%")
        print("✓ 数字人内容（头像、姓名等）正确显示")
        print("✓ 响应式布局在不同屏幕尺寸下正常")
        
        print("\n📐 比例计算:")
        print("黄金比例 φ = 1.618")
        print("较小部分 = 1 - 0.618 = 0.382")
        print("比例关系 = 0.382 : 1")
        print("数字人占比 = 0.382 / (0.382 + 1) = 27.6%")
        print("聊天占比 = 1 / (0.382 + 1) = 72.4%")
        
        print("\n🎨 视觉效果对比:")
        print("修改前:")
        print("  - 5列网格：数字人2列，聊天3列")
        print("  - 比例 2:3 = 0.667:1")
        print("  - 数字人占40%，聊天占60%")
        
        print("修改后:")
        print("  - 黄金比例：数字人0.382，聊天1")
        print("  - 比例 0.382:1")
        print("  - 数字人占27.6%，聊天占72.4%")
        print("  - 数字人卡片为9:16竖屏比例")
        
        print("\n🛠️ 开发者工具检查:")
        print("1. Elements标签: 检查.digital-human-container和.chat-container")
        print("2. 确认aspect-ratio: 9/16属性")
        print("3. 检查flex布局和宽度设置")
        print("4. 观察响应式媒体查询效果")
        
        print("\n🐛 常见问题排查:")
        print("- 如果比例不正确: 检查CSS flex和width设置")
        print("- 如果9:16比例异常: 检查aspect-ratio属性")
        print("- 如果内容显示异常: 检查数字人组件样式")
        print("- 如果响应式异常: 检查媒体查询断点")
    
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
        print("\n🌐 打开浏览器进行布局比例测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 4. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 5. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 布局比例测试准备完成！")
        print("💡 请在浏览器中验证新的布局比例效果")
        print(f"📊 基础功能测试: {'✅ 通过' if message_ok else '❌ 失败'}")
        
        return True

def main():
    """主函数"""
    tester = LayoutProportionTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
