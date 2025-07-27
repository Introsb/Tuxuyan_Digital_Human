#!/usr/bin/env python3
"""
数字人卡片9:16比例修复测试脚本
验证数字人卡片是否正确显示为9:16竖屏比例
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class DigitalHumanAspectRatioTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("📐 涂序彦教授数字人项目 - 数字人卡片9:16比例修复测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 验证数字人卡片严格按照9:16比例显示")
        print("   - 确认宽高比接近0.5625（9÷16）")
        print("   - 检查CSS aspect-ratio属性是否正确应用")
        print("   - 验证数字人内容在9:16比例下正确显示")
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
// 数字人卡片9:16比例修复测试脚本
// 在浏览器控制台中运行

console.log("📐 开始数字人卡片9:16比例测试...");

function testDigitalHumanAspectRatio() {
    console.log("🔍 检查数字人卡片9:16比例...");
    
    const digitalHumanCard = document.querySelector('.digital-human-card');
    
    if (digitalHumanCard) {
        const width = digitalHumanCard.offsetWidth;
        const height = digitalHumanCard.offsetHeight;
        
        console.log(`📏 数字人卡片实际尺寸: ${width}x${height}px`);
        
        // 计算实际宽高比
        const actualRatio = width / height;
        const targetRatio = 9 / 16; // 0.5625
        const tolerance = 0.02; // 2% 容差
        
        console.log(`📊 实际宽高比: ${actualRatio.toFixed(4)}`);
        console.log(`📊 目标9:16比例: ${targetRatio.toFixed(4)}`);
        console.log(`📊 比例差异: ${Math.abs(actualRatio - targetRatio).toFixed(4)}`);
        console.log(`📊 差异百分比: ${((Math.abs(actualRatio - targetRatio) / targetRatio) * 100).toFixed(1)}%`);
        
        if (Math.abs(actualRatio - targetRatio) <= tolerance) {
            console.log("✅ 数字人卡片比例符合9:16标准");
        } else {
            console.log(`❌ 数字人卡片比例偏离9:16标准，差异: ${((Math.abs(actualRatio - targetRatio) / targetRatio) * 100).toFixed(1)}%`);
        }
        
        // 检查CSS aspect-ratio属性
        const computedStyle = getComputedStyle(digitalHumanCard);
        const aspectRatio = computedStyle.aspectRatio;
        console.log(`🎨 CSS aspect-ratio属性: ${aspectRatio}`);
        
        if (aspectRatio === '9 / 16' || aspectRatio === '0.5625') {
            console.log("✅ CSS aspect-ratio属性正确设置");
        } else {
            console.log(`⚠️ CSS aspect-ratio属性可能不正确: ${aspectRatio}`);
        }
        
        // 检查其他可能影响比例的CSS属性
        const cssHeight = computedStyle.height;
        const cssWidth = computedStyle.width;
        const cssMaxHeight = computedStyle.maxHeight;
        const cssMinHeight = computedStyle.minHeight;
        
        console.log(`🎨 CSS属性检查:`);
        console.log(`   width: ${cssWidth}`);
        console.log(`   height: ${cssHeight}`);
        console.log(`   max-height: ${cssMaxHeight}`);
        console.log(`   min-height: ${cssMinHeight}`);
        
        // 检查是否有冲突的样式
        if (cssHeight !== 'auto' && cssHeight !== '0px') {
            console.log(`⚠️ 发现可能冲突的height样式: ${cssHeight}`);
        }
        
        if (cssMaxHeight !== 'none' && cssMaxHeight !== 'auto') {
            console.log(`⚠️ 发现可能冲突的max-height样式: ${cssMaxHeight}`);
        }
        
        return {
            width,
            height,
            actualRatio,
            targetRatio,
            isCorrect: Math.abs(actualRatio - targetRatio) <= tolerance
        };
    } else {
        console.log("❌ 未找到数字人卡片元素");
        return null;
    }
}

function testDigitalHumanContainer() {
    console.log("🔍 检查数字人容器...");
    
    const container = document.querySelector('.digital-human-container');
    
    if (container) {
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
        
        console.log(`📏 数字人容器尺寸: ${containerWidth}x${containerHeight}px`);
        
        // 检查容器是否影响子元素的aspect-ratio
        const computedStyle = getComputedStyle(container);
        const containerHeight_css = computedStyle.height;
        
        console.log(`🎨 容器CSS height: ${containerHeight_css}`);
        
        if (containerHeight_css === 'auto') {
            console.log("✅ 容器高度为auto，不会干扰aspect-ratio");
        } else {
            console.log(`⚠️ 容器高度可能干扰aspect-ratio: ${containerHeight_css}`);
        }
    } else {
        console.log("❌ 未找到数字人容器");
    }
}

function testDigitalHumanContent() {
    console.log("🔍 检查数字人内容适配...");
    
    const content = document.querySelector('.digital-human-content');
    
    if (content) {
        const contentHeight = content.offsetHeight;
        const parentHeight = content.parentElement.offsetHeight;
        
        console.log(`📏 数字人内容高度: ${contentHeight}px`);
        console.log(`📏 父容器高度: ${parentHeight}px`);
        
        // 检查内容是否适应容器
        const heightRatio = contentHeight / parentHeight;
        console.log(`📊 内容高度占比: ${(heightRatio * 100).toFixed(1)}%`);
        
        if (heightRatio <= 1.0) {
            console.log("✅ 数字人内容适应9:16容器");
        } else {
            console.log(`⚠️ 数字人内容超出容器: ${(heightRatio * 100).toFixed(1)}%`);
        }
        
        // 检查关键元素是否存在且可见
        const teamLogo = content.querySelector('img[alt*="实践团徽"]');
        const professorEmoji = content.querySelector('.text-6xl, .md\\\\:text-7xl, .lg\\\\:text-8xl');
        const professorName = content.querySelector('h2');
        
        console.log(`🏷️ 团队徽标: ${teamLogo ? '✅ 存在' : '❌ 缺失'}`);
        console.log(`👨‍🏫 教授头像: ${professorEmoji ? '✅ 存在' : '❌ 缺失'}`);
        console.log(`📝 教授姓名: ${professorName ? '✅ 存在' : '❌ 缺失'}`);
        
        // 检查元素是否在可视区域内
        if (teamLogo) {
            const logoRect = teamLogo.getBoundingClientRect();
            const containerRect = content.getBoundingClientRect();
            const logoVisible = logoRect.top >= containerRect.top && logoRect.bottom <= containerRect.bottom;
            console.log(`🏷️ 团队徽标可见性: ${logoVisible ? '✅ 可见' : '⚠️ 可能被裁剪'}`);
        }
        
        if (professorEmoji) {
            const emojiRect = professorEmoji.getBoundingClientRect();
            const containerRect = content.getBoundingClientRect();
            const emojiVisible = emojiRect.top >= containerRect.top && emojiRect.bottom <= containerRect.bottom;
            console.log(`👨‍🏫 教授头像可见性: ${emojiVisible ? '✅ 可见' : '⚠️ 可能被裁剪'}`);
        }
    } else {
        console.log("❌ 未找到数字人内容");
    }
}

function testCSSConflicts() {
    console.log("🔍 检查CSS样式冲突...");
    
    const digitalHumanCard = document.querySelector('.digital-human-card');
    
    if (digitalHumanCard) {
        // 获取所有应用的CSS类
        const classList = Array.from(digitalHumanCard.classList);
        console.log(`🎨 应用的CSS类: ${classList.join(', ')}`);
        
        // 检查可能冲突的类
        const conflictClasses = ['h-full', 'h-screen', 'min-h-full', 'max-h-full'];
        const foundConflicts = classList.filter(cls => conflictClasses.includes(cls));
        
        if (foundConflicts.length > 0) {
            console.log(`⚠️ 发现可能冲突的CSS类: ${foundConflicts.join(', ')}`);
        } else {
            console.log("✅ 未发现明显的CSS类冲突");
        }
        
        // 检查计算后的样式
        const computedStyle = getComputedStyle(digitalHumanCard);
        const importantStyles = {
            'aspect-ratio': computedStyle.aspectRatio,
            'width': computedStyle.width,
            'height': computedStyle.height,
            'max-height': computedStyle.maxHeight,
            'min-height': computedStyle.minHeight,
            'display': computedStyle.display,
            'flex-direction': computedStyle.flexDirection
        };
        
        console.log("🎨 关键CSS属性:");
        Object.entries(importantStyles).forEach(([prop, value]) => {
            console.log(`   ${prop}: ${value}`);
        });
    }
}

function testResponsiveAspectRatio() {
    console.log("🔍 测试响应式aspect-ratio...");
    
    const width = window.innerWidth;
    let expectedRatio = null;
    
    if (width >= 1024) {
        expectedRatio = 9 / 16; // 桌面端 9:16
        console.log("📱 当前断点: 桌面端 (≥1024px) - 期望9:16比例");
    } else if (width >= 768) {
        expectedRatio = 16 / 9; // 平板端 16:9
        console.log("📱 当前断点: 平板端 (768-1023px) - 期望16:9比例");
    } else {
        expectedRatio = 4 / 3; // 移动端 4:3
        console.log("📱 当前断点: 移动端 (<768px) - 期望4:3比例");
    }
    
    const digitalHumanCard = document.querySelector('.digital-human-card');
    if (digitalHumanCard && expectedRatio) {
        const actualRatio = digitalHumanCard.offsetWidth / digitalHumanCard.offsetHeight;
        const tolerance = 0.05;
        
        console.log(`📊 当前实际比例: ${actualRatio.toFixed(4)}`);
        console.log(`📊 期望比例: ${expectedRatio.toFixed(4)}`);
        
        if (Math.abs(actualRatio - expectedRatio) <= tolerance) {
            console.log("✅ 响应式aspect-ratio正确");
        } else {
            console.log(`⚠️ 响应式aspect-ratio偏离期望值`);
        }
    }
}

// 运行测试
console.log("🚀 开始数字人卡片9:16比例修复测试...");

const result = testDigitalHumanAspectRatio();

setTimeout(() => {
    testDigitalHumanContainer();
}, 500);

setTimeout(() => {
    testDigitalHumanContent();
}, 1000);

setTimeout(() => {
    testCSSConflicts();
}, 1500);

setTimeout(() => {
    testResponsiveAspectRatio();
}, 2000);

console.log("🎯 数字人卡片9:16比例测试脚本运行完成");
console.log("💡 请观察:");
console.log("   1. 数字人卡片宽高比是否接近0.5625");
console.log("   2. CSS aspect-ratio属性是否正确应用");
console.log("   3. 数字人内容是否在9:16比例下正确显示");
console.log("   4. 是否存在CSS样式冲突");

// 返回测试结果供进一步分析
if (result) {
    console.log("\\n📊 测试结果总结:");
    console.log(`   实际比例: ${result.actualRatio.toFixed(4)}`);
    console.log(`   目标比例: ${result.targetRatio.toFixed(4)}`);
    console.log(`   测试结果: ${result.isCorrect ? '✅ 通过' : '❌ 失败'}`);
}
"""
        
        with open("browser_aspect_ratio_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_aspect_ratio_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 数字人卡片9:16比例修复测试说明")
        print("=" * 80)
        
        print("\n🎯 测试步骤:")
        print("1. 在浏览器中打开前端页面")
        print("2. 按F12打开开发者工具")
        print("3. 在Console标签中运行测试脚本")
        print("4. 观察数字人卡片的实际显示效果")
        print("5. 使用Elements标签检查CSS样式")
        
        print("\n🔍 检查要点:")
        print("✓ 数字人卡片宽高比应接近0.5625（9÷16）")
        print("✓ CSS aspect-ratio属性应为'9 / 16'")
        print("✓ 数字人内容（头像、姓名等）应完整显示")
        print("✓ 不应存在height: 100%等冲突样式")
        print("✓ 卡片应呈现明显的竖屏比例")
        
        print("\n📐 比例验证方法:")
        print("1. 在Elements标签中选择.digital-human-card元素")
        print("2. 查看Computed标签中的width和height值")
        print("3. 计算width ÷ height，应约等于0.5625")
        print("4. 检查aspect-ratio属性是否为'9 / 16'")
        
        print("\n🔧 问题排查:")
        print("如果比例不正确，检查以下项目:")
        print("- 是否有h-full、h-screen等冲突的CSS类")
        print("- 是否有height: 100%等固定高度样式")
        print("- 是否有max-height限制影响aspect-ratio")
        print("- 父容器是否设置了固定高度")
        
        print("\n🎨 预期效果:")
        print("修复后的数字人卡片应该:")
        print("- 呈现明显的竖屏比例（高度大于宽度）")
        print("- 宽高比约为0.5625（9:16）")
        print("- 数字人内容完整显示且居中")
        print("- 在不同屏幕尺寸下保持正确比例")
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败")
            return False
        
        # 2. 打开浏览器
        print("\n🌐 打开浏览器进行数字人卡片比例测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 3. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 4. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 数字人卡片9:16比例修复测试准备完成！")
        print("💡 请在浏览器中验证修复效果")
        print("📋 运行测试脚本以获得详细的比例分析")
        
        return True

def main():
    """主函数"""
    tester = DigitalHumanAspectRatioTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
