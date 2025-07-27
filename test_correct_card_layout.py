#!/usr/bin/env python3
"""
正确的卡片布局测试脚本
验证数字人卡片和聊天卡片高度一致，且数字人卡片保持9:16比例
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class CorrectCardLayoutTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("📐 涂序彦教授数字人项目 - 正确的卡片布局测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 验证数字人卡片和聊天卡片高度完全一致")
        print("   - 确认数字人卡片保持9:16的宽高比例")
        print("   - 检查数字人卡片宽度由9:16比例自动决定")
        print("   - 验证聊天卡片占据剩余空间")
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
    
    def create_browser_test_script(self):
        """创建浏览器测试脚本"""
        test_script = """
// 正确的卡片布局测试脚本
// 在浏览器控制台中运行

console.log("📐 开始正确的卡片布局测试...");

function testCorrectCardLayout() {
    console.log("🔍 检查卡片布局是否正确...");
    
    const digitalHumanCard = document.querySelector('.digital-human-card');
    const chatCard = document.querySelector('.fullscreen-chat-card');
    
    if (digitalHumanCard && chatCard) {
        const digitalWidth = digitalHumanCard.offsetWidth;
        const digitalHeight = digitalHumanCard.offsetHeight;
        const chatWidth = chatCard.offsetWidth;
        const chatHeight = chatCard.offsetHeight;
        
        console.log(`📏 数字人卡片尺寸: ${digitalWidth}x${digitalHeight}px`);
        console.log(`📏 聊天卡片尺寸: ${chatWidth}x${chatHeight}px`);
        
        // 1. 检查高度一致性
        const heightDiff = Math.abs(digitalHeight - chatHeight);
        console.log(`📏 高度差异: ${heightDiff}px`);
        
        if (heightDiff <= 5) {
            console.log("✅ 卡片高度一致性良好");
        } else {
            console.log(`❌ 卡片高度不一致，差异: ${heightDiff}px`);
        }
        
        // 2. 检查数字人卡片的9:16比例
        const digitalRatio = digitalWidth / digitalHeight;
        const targetRatio = 9 / 16; // 0.5625
        const ratioTolerance = 0.02;
        
        console.log(`📊 数字人卡片宽高比: ${digitalRatio.toFixed(4)}`);
        console.log(`📊 目标9:16比例: ${targetRatio.toFixed(4)}`);
        console.log(`📊 比例差异: ${Math.abs(digitalRatio - targetRatio).toFixed(4)}`);
        
        if (Math.abs(digitalRatio - targetRatio) <= ratioTolerance) {
            console.log("✅ 数字人卡片9:16比例正确");
        } else {
            console.log(`❌ 数字人卡片比例不正确，差异: ${((Math.abs(digitalRatio - targetRatio) / targetRatio) * 100).toFixed(1)}%`);
        }
        
        // 3. 检查宽度关系
        console.log(`📊 数字人卡片宽度: ${digitalWidth}px`);
        console.log(`📊 聊天卡片宽度: ${chatWidth}px`);
        console.log(`📊 宽度比例: ${(digitalWidth / chatWidth).toFixed(3)} (数字人:聊天)`);
        
        // 4. 验证数字人卡片宽度是否由9:16比例决定
        const expectedWidth = digitalHeight * (9 / 16);
        const widthDiff = Math.abs(digitalWidth - expectedWidth);
        
        console.log(`📊 基于高度计算的期望宽度: ${expectedWidth.toFixed(1)}px`);
        console.log(`📊 实际宽度与期望宽度差异: ${widthDiff.toFixed(1)}px`);
        
        if (widthDiff <= 2) {
            console.log("✅ 数字人卡片宽度正确由9:16比例决定");
        } else {
            console.log(`❌ 数字人卡片宽度不是由9:16比例决定，差异: ${widthDiff.toFixed(1)}px`);
        }
        
        return {
            digitalWidth,
            digitalHeight,
            chatWidth,
            chatHeight,
            heightDiff,
            digitalRatio,
            isHeightConsistent: heightDiff <= 5,
            isRatioCorrect: Math.abs(digitalRatio - targetRatio) <= ratioTolerance,
            isWidthCorrect: widthDiff <= 2
        };
    } else {
        console.log("❌ 未找到数字人卡片或聊天卡片");
        return null;
    }
}

function testDigitalHumanCardCSS() {
    console.log("🔍 检查数字人卡片CSS设置...");
    
    const digitalHumanCard = document.querySelector('.digital-human-card');
    
    if (digitalHumanCard) {
        const computedStyle = getComputedStyle(digitalHumanCard);
        
        const cssProperties = {
            'height': computedStyle.height,
            'width': computedStyle.width,
            'aspect-ratio': computedStyle.aspectRatio,
            'max-height': computedStyle.maxHeight,
            'min-height': computedStyle.minHeight
        };
        
        console.log("🎨 数字人卡片CSS属性:");
        Object.entries(cssProperties).forEach(([prop, value]) => {
            console.log(`   ${prop}: ${value}`);
        });
        
        // 检查关键设置
        if (computedStyle.aspectRatio === '9 / 16' || computedStyle.aspectRatio === '0.5625') {
            console.log("✅ aspect-ratio正确设置为9/16");
        } else {
            console.log(`⚠️ aspect-ratio设置可能不正确: ${computedStyle.aspectRatio}`);
        }
        
        if (computedStyle.height === '100%' || computedStyle.height.includes('vh')) {
            console.log("✅ 高度设置为100%，与聊天卡片一致");
        } else {
            console.log(`⚠️ 高度设置可能不正确: ${computedStyle.height}`);
        }
        
        if (computedStyle.width === 'auto') {
            console.log("✅ 宽度设置为auto，由aspect-ratio决定");
        } else {
            console.log(`ℹ️ 宽度设置: ${computedStyle.width}`);
        }
    } else {
        console.log("❌ 未找到数字人卡片");
    }
}

function testContainerLayout() {
    console.log("🔍 检查容器布局...");
    
    const digitalContainer = document.querySelector('.digital-human-container');
    const chatContainer = document.querySelector('.chat-container');
    const parentContainer = document.querySelector('.golden-ratio-layout');
    
    if (digitalContainer && chatContainer && parentContainer) {
        const digitalContainerWidth = digitalContainer.offsetWidth;
        const chatContainerWidth = chatContainer.offsetWidth;
        const parentWidth = parentContainer.offsetWidth;
        
        console.log(`📏 数字人容器宽度: ${digitalContainerWidth}px`);
        console.log(`📏 聊天容器宽度: ${chatContainerWidth}px`);
        console.log(`📏 父容器总宽度: ${parentWidth}px`);
        
        const digitalPercent = (digitalContainerWidth / parentWidth) * 100;
        const chatPercent = (chatContainerWidth / parentWidth) * 100;
        
        console.log(`📊 数字人容器占比: ${digitalPercent.toFixed(1)}%`);
        console.log(`📊 聊天容器占比: ${chatPercent.toFixed(1)}%`);
        
        // 检查数字人容器的CSS设置
        const digitalContainerStyle = getComputedStyle(digitalContainer);
        console.log(`🎨 数字人容器width: ${digitalContainerStyle.width}`);
        console.log(`🎨 数字人容器flex: ${digitalContainerStyle.flex}`);
        
        if (digitalContainerStyle.width === 'auto') {
            console.log("✅ 数字人容器宽度设置为auto，由子元素决定");
        } else {
            console.log(`ℹ️ 数字人容器宽度: ${digitalContainerStyle.width}`);
        }
        
        // 检查聊天容器的flex设置
        const chatContainerStyle = getComputedStyle(chatContainer);
        console.log(`🎨 聊天容器flex: ${chatContainerStyle.flex}`);
        
        if (chatContainerStyle.flex === '1 1 0%' || chatContainerStyle.flex.includes('1')) {
            console.log("✅ 聊天容器使用flex: 1，占据剩余空间");
        } else {
            console.log(`⚠️ 聊天容器flex设置可能不正确: ${chatContainerStyle.flex}`);
        }
    } else {
        console.log("❌ 未找到容器元素");
    }
}

function testVisualEffect() {
    console.log("🔍 检查视觉效果...");
    
    const digitalContainer = document.querySelector('.digital-human-container');
    const chatContainer = document.querySelector('.chat-container');
    
    if (digitalContainer && chatContainer) {
        const digitalRect = digitalContainer.getBoundingClientRect();
        const chatRect = chatContainer.getBoundingClientRect();
        
        // 检查顶部对齐
        const topDiff = Math.abs(digitalRect.top - chatRect.top);
        console.log(`📏 顶部对齐差异: ${topDiff.toFixed(1)}px`);
        
        // 检查底部对齐
        const bottomDiff = Math.abs(digitalRect.bottom - chatRect.bottom);
        console.log(`📏 底部对齐差异: ${bottomDiff.toFixed(1)}px`);
        
        if (topDiff <= 2 && bottomDiff <= 2) {
            console.log("✅ 两个卡片完美对齐");
        } else {
            console.log("⚠️ 卡片对齐可能需要调整");
        }
        
        // 检查数字人卡片是否明显比聊天卡片窄
        const widthRatio = digitalRect.width / chatRect.width;
        console.log(`📊 宽度比例 (数字人/聊天): ${widthRatio.toFixed(3)}`);
        
        if (widthRatio < 0.8) {
            console.log("✅ 数字人卡片明显比聊天卡片窄，符合9:16比例预期");
        } else {
            console.log("⚠️ 数字人卡片可能不够窄");
        }
    }
}

function testResponsiveLayout() {
    console.log("🔍 测试响应式布局...");
    
    const width = window.innerWidth;
    
    if (width >= 1024) {
        console.log("📱 当前断点: 桌面端 - 应保持高度一致和9:16比例");
        
        const result = testCorrectCardLayout();
        if (result) {
            if (result.isHeightConsistent && result.isRatioCorrect && result.isWidthCorrect) {
                console.log("✅ 桌面端布局完全正确");
            } else {
                console.log("❌ 桌面端布局需要调整");
            }
        }
    } else if (width >= 768) {
        console.log("📱 当前断点: 平板端 - 垂直布局，16:9比例");
    } else {
        console.log("📱 当前断点: 移动端 - 垂直布局，4:3比例");
    }
}

// 运行测试
console.log("🚀 开始正确的卡片布局测试...");

const layoutResult = testCorrectCardLayout();

setTimeout(() => {
    testDigitalHumanCardCSS();
}, 500);

setTimeout(() => {
    testContainerLayout();
}, 1000);

setTimeout(() => {
    testVisualEffect();
}, 1500);

setTimeout(() => {
    testResponsiveLayout();
}, 2000);

console.log("🎯 正确的卡片布局测试脚本运行完成");
console.log("💡 预期效果:");
console.log("   1. 数字人卡片和聊天卡片高度完全一致");
console.log("   2. 数字人卡片宽高比为9:16 (0.5625)");
console.log("   3. 数字人卡片明显比聊天卡片窄");
console.log("   4. 聊天卡片占据剩余的水平空间");

// 返回测试结果
if (layoutResult) {
    console.log("\\n📊 布局测试结果总结:");
    console.log(`   高度一致性: ${layoutResult.isHeightConsistent ? '✅ 正确' : '❌ 错误'}`);
    console.log(`   9:16比例: ${layoutResult.isRatioCorrect ? '✅ 正确' : '❌ 错误'}`);
    console.log(`   宽度计算: ${layoutResult.isWidthCorrect ? '✅ 正确' : '❌ 错误'}`);
    console.log(`   数字人卡片: ${layoutResult.digitalWidth}x${layoutResult.digitalHeight}px`);
    console.log(`   聊天卡片: ${layoutResult.chatWidth}x${layoutResult.chatHeight}px`);
}
"""
        
        with open("browser_correct_layout_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_correct_layout_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 正确的卡片布局测试说明")
        print("=" * 80)
        
        print("\n🎯 正确的布局要求:")
        print("1. 数字人卡片和聊天卡片高度完全一致")
        print("2. 数字人卡片保持9:16的宽高比例")
        print("3. 数字人卡片的宽度由9:16比例自动决定")
        print("4. 聊天卡片占据剩余的水平空间")
        
        print("\n🔍 检查要点:")
        print("✓ 两个卡片顶部和底部完美对齐")
        print("✓ 数字人卡片明显比聊天卡片窄")
        print("✓ 数字人卡片宽高比接近0.5625")
        print("✓ 如果高度是800px，宽度应该是450px (800 × 9/16)")
        
        print("\n📐 比例验证:")
        print("数字人卡片宽高比 = 宽度 ÷ 高度 = 9 ÷ 16 = 0.5625")
        print("如果高度是H，那么宽度应该是 H × (9/16)")
        
        print("\n🎨 预期视觉效果:")
        print("┌─────────┐ ┌─────────────────────────┐")
        print("│         │ │                        │")
        print("│数字人卡片│ │ 聊天卡片                │")
        print("│(9:16比例)│ │ (占据剩余空间)          │")
        print("│ 同等高度 │ │ 同等高度                │")
        print("└─────────┘ └─────────────────────────┘")
        
        print("\n🔧 如果布局不正确:")
        print("- 检查数字人卡片的aspect-ratio是否为9/16")
        print("- 检查数字人卡片的height是否为100%")
        print("- 检查数字人卡片的width是否为auto")
        print("- 检查数字人容器的width是否为auto")
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败")
            return False
        
        # 2. 打开浏览器
        print("\n🌐 打开浏览器进行正确的卡片布局测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 3. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 4. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 正确的卡片布局测试准备完成！")
        print("💡 请在浏览器中验证修复效果")
        print("📋 运行测试脚本以获得详细的布局分析")
        
        return True

def main():
    """主函数"""
    tester = CorrectCardLayoutTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
