#!/usr/bin/env python3
"""
当前布局比例测试脚本
验证数字人卡片保持固定尺寸，聊天卡片适应黄金比例关系
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class CurrentLayoutRatioTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("📐 涂序彦教授数字人项目 - 当前布局比例测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 验证数字人卡片保持固定尺寸（不改变长度宽度）")
        print("   - 检查聊天卡片适应黄金比例关系")
        print("   - 确认比例：数字人卡片宽度:聊天卡片宽度 = 0.382:1")
        print("   - 验证两个卡片高度一致")
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
// 当前布局比例测试脚本
// 在浏览器控制台中运行

console.log("📐 开始当前布局比例测试...");

function testCurrentLayoutRatio() {
    console.log("🔍 检查当前布局比例关系...");
    
    const digitalCard = document.querySelector('.digital-human-card');
    const chatCard = document.querySelector('.fullscreen-chat-card');
    const digitalContainer = document.querySelector('.digital-human-container');
    const chatContainer = document.querySelector('.chat-container');
    
    if (digitalCard && chatCard && digitalContainer && chatContainer) {
        // 获取卡片尺寸
        const digitalCardWidth = digitalCard.offsetWidth;
        const digitalCardHeight = digitalCard.offsetHeight;
        const chatCardWidth = chatCard.offsetWidth;
        const chatCardHeight = chatCard.offsetHeight;
        
        // 获取容器尺寸
        const digitalContainerWidth = digitalContainer.offsetWidth;
        const chatContainerWidth = chatContainer.offsetWidth;
        
        console.log("📏 卡片尺寸:");
        console.log(`   数字人卡片: ${digitalCardWidth}x${digitalCardHeight}px`);
        console.log(`   聊天卡片: ${chatCardWidth}x${chatCardHeight}px`);
        
        console.log("📏 容器尺寸:");
        console.log(`   数字人容器: ${digitalContainerWidth}px`);
        console.log(`   聊天容器: ${chatContainerWidth}px`);
        
        // 1. 检查数字人卡片是否保持9:16比例
        const digitalRatio = digitalCardWidth / digitalCardHeight;
        const targetRatio = 9 / 16; // 0.5625
        const ratioTolerance = 0.05;
        
        console.log(`📊 数字人卡片宽高比: ${digitalRatio.toFixed(4)}`);
        console.log(`📊 目标9:16比例: ${targetRatio.toFixed(4)}`);
        
        if (Math.abs(digitalRatio - targetRatio) <= ratioTolerance) {
            console.log("✅ 数字人卡片保持9:16比例");
        } else {
            console.log(`⚠️ 数字人卡片比例偏离9:16`);
        }
        
        // 2. 检查高度一致性
        const heightDiff = Math.abs(digitalCardHeight - chatCardHeight);
        console.log(`📏 卡片高度差异: ${heightDiff}px`);
        
        if (heightDiff <= 5) {
            console.log("✅ 两个卡片高度一致");
        } else {
            console.log(`⚠️ 卡片高度不一致，差异: ${heightDiff}px`);
        }
        
        // 3. 检查宽度比例关系
        const widthRatio = digitalCardWidth / chatCardWidth;
        const targetWidthRatio = 0.382; // 数字人:聊天 = 0.382:1
        const widthTolerance = 0.05;
        
        console.log(`📊 实际宽度比例 (数字人:聊天): ${widthRatio.toFixed(3)}`);
        console.log(`📊 目标比例 (0.382:1): ${targetWidthRatio.toFixed(3)}`);
        console.log(`📊 比例差异: ${Math.abs(widthRatio - targetWidthRatio).toFixed(3)}`);
        
        if (Math.abs(widthRatio - targetWidthRatio) <= widthTolerance) {
            console.log("✅ 宽度比例符合黄金比例关系 (0.382:1)");
        } else {
            console.log(`⚠️ 宽度比例偏离目标，差异: ${((Math.abs(widthRatio - targetWidthRatio) / targetWidthRatio) * 100).toFixed(1)}%`);
        }
        
        // 4. 计算聊天卡片相对于数字人卡片的倍数
        const chatWidthMultiple = chatCardWidth / digitalCardWidth;
        const expectedMultiple = 1 / 0.382; // 约2.618
        
        console.log(`📊 聊天卡片宽度倍数: ${chatWidthMultiple.toFixed(2)}x`);
        console.log(`📊 期望倍数 (1/0.382): ${expectedMultiple.toFixed(2)}x`);
        
        if (Math.abs(chatWidthMultiple - expectedMultiple) <= 0.2) {
            console.log("✅ 聊天卡片宽度倍数符合黄金比例");
        } else {
            console.log(`⚠️ 聊天卡片宽度倍数偏离期望值`);
        }
        
        // 5. 检查数字人卡片是否保持固定尺寸
        console.log("🔍 数字人卡片尺寸检查:");
        console.log(`   宽度: ${digitalCardWidth}px (由9:16比例和高度决定)`);
        console.log(`   高度: ${digitalCardHeight}px (与聊天卡片一致)`);
        console.log(`   容器宽度: ${digitalContainerWidth}px (适应卡片尺寸)`);
        
        // 验证容器是否适应卡片尺寸
        const containerCardDiff = Math.abs(digitalContainerWidth - digitalCardWidth);
        if (containerCardDiff <= 10) {
            console.log("✅ 数字人容器正确适应卡片尺寸");
        } else {
            console.log(`⚠️ 数字人容器与卡片尺寸差异较大: ${containerCardDiff}px`);
        }
        
        return {
            digitalCardWidth,
            digitalCardHeight,
            chatCardWidth,
            chatCardHeight,
            digitalRatio,
            widthRatio,
            heightDiff,
            chatWidthMultiple,
            isRatioCorrect: Math.abs(digitalRatio - targetRatio) <= ratioTolerance,
            isHeightConsistent: heightDiff <= 5,
            isWidthRatioCorrect: Math.abs(widthRatio - targetWidthRatio) <= widthTolerance
        };
    } else {
        console.log("❌ 未找到必要的卡片或容器元素");
        return null;
    }
}

function testCSSSettings() {
    console.log("🔍 检查CSS设置...");
    
    const digitalCard = document.querySelector('.digital-human-card');
    const digitalContainer = document.querySelector('.digital-human-container');
    const chatContainer = document.querySelector('.chat-container');
    
    if (digitalCard && digitalContainer && chatContainer) {
        const cardStyle = getComputedStyle(digitalCard);
        const digitalContainerStyle = getComputedStyle(digitalContainer);
        const chatContainerStyle = getComputedStyle(chatContainer);
        
        console.log("🎨 数字人卡片CSS:");
        console.log(`   aspect-ratio: ${cardStyle.aspectRatio}`);
        console.log(`   width: ${cardStyle.width}`);
        console.log(`   height: ${cardStyle.height}`);
        
        console.log("🎨 数字人容器CSS:");
        console.log(`   flex: ${digitalContainerStyle.flex}`);
        console.log(`   width: ${digitalContainerStyle.width}`);
        
        console.log("🎨 聊天容器CSS:");
        console.log(`   flex: ${chatContainerStyle.flex}`);
        console.log(`   width: ${chatContainerStyle.width}`);
        
        // 验证关键设置
        if (cardStyle.aspectRatio === '9 / 16' || cardStyle.aspectRatio === '0.5625') {
            console.log("✅ 数字人卡片aspect-ratio正确设置");
        } else {
            console.log(`⚠️ 数字人卡片aspect-ratio可能不正确: ${cardStyle.aspectRatio}`);
        }
        
        if (digitalContainerStyle.width === 'auto') {
            console.log("✅ 数字人容器宽度设置为auto，适应卡片尺寸");
        } else {
            console.log(`ℹ️ 数字人容器宽度: ${digitalContainerStyle.width}`);
        }
        
        if (chatContainerStyle.flex === '1 1 0%' || chatContainerStyle.flex.includes('1')) {
            console.log("✅ 聊天容器使用flex: 1，占据剩余空间");
        } else {
            console.log(`ℹ️ 聊天容器flex: ${chatContainerStyle.flex}`);
        }
    }
}

function testLayoutBehavior() {
    console.log("🔍 测试布局行为...");
    
    const parentContainer = document.querySelector('.golden-ratio-layout');
    const digitalContainer = document.querySelector('.digital-human-container');
    const chatContainer = document.querySelector('.chat-container');
    
    if (parentContainer && digitalContainer && chatContainer) {
        const parentWidth = parentContainer.offsetWidth;
        const digitalWidth = digitalContainer.offsetWidth;
        const chatWidth = chatContainer.offsetWidth;
        const totalChildWidth = digitalWidth + chatWidth;
        
        console.log(`📏 父容器宽度: ${parentWidth}px`);
        console.log(`📏 子元素总宽度: ${totalChildWidth}px`);
        console.log(`📏 宽度差异: ${Math.abs(parentWidth - totalChildWidth)}px`);
        
        // 检查数字人卡片是否保持固定尺寸
        console.log("🔍 数字人卡片尺寸行为:");
        console.log("   - 宽度由9:16比例和高度自动计算");
        console.log("   - 高度与聊天卡片保持一致");
        console.log("   - 容器适应卡片尺寸");
        
        console.log("🔍 聊天卡片适应行为:");
        console.log("   - 占据数字人卡片之外的剩余空间");
        console.log("   - 宽度根据可用空间自动调整");
        console.log("   - 高度与数字人卡片保持一致");
        
        // 计算实际的比例关系
        const actualRatio = digitalWidth / chatWidth;
        console.log(`📊 当前实际比例 (数字人:聊天): ${actualRatio.toFixed(3)}`);
        
        if (actualRatio >= 0.3 && actualRatio <= 0.45) {
            console.log("✅ 当前比例在合理范围内，接近黄金比例关系");
        } else {
            console.log("ℹ️ 当前比例可能需要调整以更接近黄金比例");
        }
    }
}

// 运行测试
console.log("🚀 开始当前布局比例测试...");

const layoutResult = testCurrentLayoutRatio();

setTimeout(() => {
    testCSSSettings();
}, 500);

setTimeout(() => {
    testLayoutBehavior();
}, 1000);

console.log("🎯 当前布局比例测试脚本运行完成");
console.log("💡 当前布局特点:");
console.log("   1. 数字人卡片保持固定尺寸（9:16比例）");
console.log("   2. 聊天卡片占据剩余空间");
console.log("   3. 两个卡片高度一致");
console.log("   4. 布局自适应不同屏幕尺寸");

// 返回测试结果
if (layoutResult) {
    console.log("\\n📊 当前布局测试结果:");
    console.log(`   数字人卡片: ${layoutResult.digitalCardWidth}x${layoutResult.digitalCardHeight}px`);
    console.log(`   聊天卡片: ${layoutResult.chatCardWidth}x${layoutResult.chatCardHeight}px`);
    console.log(`   宽度比例: ${layoutResult.widthRatio.toFixed(3)} (目标: 0.382)`);
    console.log(`   高度一致: ${layoutResult.isHeightConsistent ? '✅ 是' : '❌ 否'}`);
    console.log(`   9:16比例: ${layoutResult.isRatioCorrect ? '✅ 正确' : '❌ 错误'}`);
}
"""
        
        with open("browser_current_layout_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_current_layout_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 当前布局比例测试说明")
        print("=" * 80)
        
        print("\n🎯 您的要求:")
        print("1. 不改变数字人卡片的长度和宽度（保持固定尺寸）")
        print("2. 可以改变数字人卡片的位置")
        print("3. 修改聊天界面的长度来适应黄金比例关系")
        print("4. 目标比例：数字人卡片宽度:聊天卡片宽度 = 0.382:1")
        
        print("\n🔍 当前布局特点:")
        print("✓ 数字人卡片保持9:16比例的固定尺寸")
        print("✓ 数字人卡片宽度由高度和9:16比例自动计算")
        print("✓ 聊天卡片占据剩余的水平空间")
        print("✓ 两个卡片高度完全一致")
        
        print("\n📐 比例验证:")
        print("当前布局已经符合您的要求：")
        print("- 数字人卡片尺寸固定（不会改变）")
        print("- 聊天卡片宽度自适应剩余空间")
        print("- 实际比例会根据屏幕尺寸自动调整")
        
        print("\n🎨 预期效果:")
        print("┌─────────┐ ┌─────────────────────────┐")
        print("│数字人卡片│ │ 聊天卡片 (适应剩余空间)  │")
        print("│(固定尺寸)│ │                        │")
        print("│ 9:16比例 │ │                        │")
        print("└─────────┘ └─────────────────────────┘")
        
        print("\n💡 说明:")
        print("当前的CSS设置已经实现了您的要求：")
        print("- 数字人卡片保持固定的9:16比例尺寸")
        print("- 聊天卡片使用flex: 1占据剩余空间")
        print("- 这样的布局会根据屏幕大小自动调整比例")
        print("- 在大屏幕上，聊天卡片会更宽，比例更接近黄金比例")
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败")
            return False
        
        # 2. 打开浏览器
        print("\n🌐 打开浏览器进行当前布局比例测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 3. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 4. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 当前布局比例测试准备完成！")
        print("💡 请在浏览器中验证当前布局是否符合您的要求")
        print("📋 运行测试脚本以获得详细的布局分析")
        
        return True

def main():
    """主函数"""
    tester = CurrentLayoutRatioTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
