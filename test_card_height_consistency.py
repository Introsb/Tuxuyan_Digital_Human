#!/usr/bin/env python3
"""
卡片高度一致性测试脚本
验证数字人卡片和聊天卡片的高度是否完全一致
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class CardHeightConsistencyTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("📏 涂序彦教授数字人项目 - 卡片高度一致性测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 验证数字人卡片和聊天卡片高度完全一致")
        print("   - 确认两个卡片在桌面端呈现相同的视觉高度")
        print("   - 检查高度差异是否在可接受范围内（<5px）")
        print("   - 验证数字人内容在新高度下正确显示")
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
// 卡片高度一致性测试脚本
// 在浏览器控制台中运行

console.log("📏 开始卡片高度一致性测试...");

function testCardHeightConsistency() {
    console.log("🔍 检查数字人卡片和聊天卡片高度一致性...");
    
    const digitalHumanCard = document.querySelector('.digital-human-card');
    const chatCard = document.querySelector('.fullscreen-chat-card');
    
    if (digitalHumanCard && chatCard) {
        const digitalHeight = digitalHumanCard.offsetHeight;
        const chatHeight = chatCard.offsetHeight;
        const heightDiff = Math.abs(digitalHeight - chatHeight);
        
        console.log(`📏 数字人卡片高度: ${digitalHeight}px`);
        console.log(`📏 聊天卡片高度: ${chatHeight}px`);
        console.log(`📏 高度差异: ${heightDiff}px`);
        
        // 检查高度一致性（允许5px以内的差异）
        const tolerance = 5;
        if (heightDiff <= tolerance) {
            console.log("✅ 卡片高度一致性良好");
        } else {
            console.log(`⚠️ 卡片高度差异较大: ${heightDiff}px (超过${tolerance}px容差)`);
        }
        
        // 计算高度差异百分比
        const heightDiffPercent = (heightDiff / Math.max(digitalHeight, chatHeight)) * 100;
        console.log(`📊 高度差异百分比: ${heightDiffPercent.toFixed(2)}%`);
        
        if (heightDiffPercent <= 1) {
            console.log("✅ 高度差异在1%以内，视觉效果良好");
        } else {
            console.log(`⚠️ 高度差异超过1%，可能影响视觉效果`);
        }
        
        return {
            digitalHeight,
            chatHeight,
            heightDiff,
            heightDiffPercent,
            isConsistent: heightDiff <= tolerance
        };
    } else {
        console.log("❌ 未找到数字人卡片或聊天卡片");
        return null;
    }
}

function testCardContainerHeights() {
    console.log("🔍 检查卡片容器高度...");
    
    const digitalContainer = document.querySelector('.digital-human-container');
    const chatContainer = document.querySelector('.chat-container');
    
    if (digitalContainer && chatContainer) {
        const digitalContainerHeight = digitalContainer.offsetHeight;
        const chatContainerHeight = chatContainer.offsetHeight;
        const containerHeightDiff = Math.abs(digitalContainerHeight - chatContainerHeight);
        
        console.log(`📏 数字人容器高度: ${digitalContainerHeight}px`);
        console.log(`📏 聊天容器高度: ${chatContainerHeight}px`);
        console.log(`📏 容器高度差异: ${containerHeightDiff}px`);
        
        if (containerHeightDiff <= 5) {
            console.log("✅ 容器高度一致性良好");
        } else {
            console.log(`⚠️ 容器高度差异较大: ${containerHeightDiff}px`);
        }
        
        // 检查容器是否使用了相同的高度类
        const digitalHasFullscreen = digitalContainer.classList.contains('fullscreen-card-height');
        const chatHasFullscreen = chatContainer.classList.contains('fullscreen-card-height');
        
        console.log(`🎨 数字人容器使用fullscreen-card-height: ${digitalHasFullscreen ? '是' : '否'}`);
        console.log(`🎨 聊天容器使用fullscreen-card-height: ${chatHasFullscreen ? '是' : '否'}`);
        
        if (digitalHasFullscreen && chatHasFullscreen) {
            console.log("✅ 两个容器都使用了相同的高度类");
        } else {
            console.log("⚠️ 容器使用的高度类不一致");
        }
    } else {
        console.log("❌ 未找到卡片容器");
    }
}

function testDigitalHumanCardCSS() {
    console.log("🔍 检查数字人卡片CSS样式...");
    
    const digitalHumanCard = document.querySelector('.digital-human-card');
    
    if (digitalHumanCard) {
        const computedStyle = getComputedStyle(digitalHumanCard);
        
        const cssProperties = {
            'height': computedStyle.height,
            'width': computedStyle.width,
            'aspect-ratio': computedStyle.aspectRatio,
            'max-height': computedStyle.maxHeight,
            'min-height': computedStyle.minHeight,
            'display': computedStyle.display,
            'flex-direction': computedStyle.flexDirection
        };
        
        console.log("🎨 数字人卡片CSS属性:");
        Object.entries(cssProperties).forEach(([prop, value]) => {
            console.log(`   ${prop}: ${value}`);
        });
        
        // 检查关键样式
        if (computedStyle.height === '100%' || computedStyle.height.includes('vh')) {
            console.log("✅ 数字人卡片使用了全高度样式");
        } else {
            console.log(`⚠️ 数字人卡片可能未使用全高度样式: ${computedStyle.height}`);
        }
        
        // 检查是否移除了aspect-ratio限制
        if (computedStyle.aspectRatio === 'auto' || computedStyle.aspectRatio === 'none') {
            console.log("✅ aspect-ratio限制已移除，优先保证高度一致");
        } else {
            console.log(`ℹ️ 仍有aspect-ratio设置: ${computedStyle.aspectRatio}`);
        }
        
        // 检查CSS类
        const classList = Array.from(digitalHumanCard.classList);
        console.log(`🎨 应用的CSS类: ${classList.join(', ')}`);
        
        if (classList.includes('h-full')) {
            console.log("✅ 数字人卡片使用了h-full类");
        } else {
            console.log("⚠️ 数字人卡片可能缺少h-full类");
        }
    } else {
        console.log("❌ 未找到数字人卡片");
    }
}

function testDigitalHumanContentFit() {
    console.log("🔍 检查数字人内容适配...");
    
    const digitalHumanContent = document.querySelector('.digital-human-content');
    const digitalHumanCard = document.querySelector('.digital-human-card');
    
    if (digitalHumanContent && digitalHumanCard) {
        const contentHeight = digitalHumanContent.offsetHeight;
        const cardHeight = digitalHumanCard.offsetHeight;
        const contentFitRatio = contentHeight / cardHeight;
        
        console.log(`📏 数字人内容高度: ${contentHeight}px`);
        console.log(`📏 数字人卡片高度: ${cardHeight}px`);
        console.log(`📊 内容适配比例: ${(contentFitRatio * 100).toFixed(1)}%`);
        
        if (contentFitRatio <= 1.0) {
            console.log("✅ 数字人内容适应卡片高度");
        } else {
            console.log(`⚠️ 数字人内容超出卡片高度: ${(contentFitRatio * 100).toFixed(1)}%`);
        }
        
        // 检查关键元素是否可见
        const teamLogo = digitalHumanContent.querySelector('img[alt*="实践团徽"]');
        const professorEmoji = digitalHumanContent.querySelector('.text-6xl, .md\\\\:text-7xl, .lg\\\\:text-8xl');
        const professorName = digitalHumanContent.querySelector('h2');
        
        console.log(`🏷️ 团队徽标: ${teamLogo ? '✅ 存在' : '❌ 缺失'}`);
        console.log(`👨‍🏫 教授头像: ${professorEmoji ? '✅ 存在' : '❌ 缺失'}`);
        console.log(`📝 教授姓名: ${professorName ? '✅ 存在' : '❌ 缺失'}`);
        
        // 检查元素是否在可视区域内
        if (teamLogo && professorEmoji && professorName) {
            const cardRect = digitalHumanCard.getBoundingClientRect();
            
            const logoRect = teamLogo.getBoundingClientRect();
            const emojiRect = professorEmoji.getBoundingClientRect();
            const nameRect = professorName.getBoundingClientRect();
            
            const logoVisible = logoRect.bottom <= cardRect.bottom && logoRect.top >= cardRect.top;
            const emojiVisible = emojiRect.bottom <= cardRect.bottom && emojiRect.top >= cardRect.top;
            const nameVisible = nameRect.bottom <= cardRect.bottom && nameRect.top >= cardRect.top;
            
            console.log(`🏷️ 团队徽标可见: ${logoVisible ? '✅ 是' : '⚠️ 否'}`);
            console.log(`👨‍🏫 教授头像可见: ${emojiVisible ? '✅ 是' : '⚠️ 否'}`);
            console.log(`📝 教授姓名可见: ${nameVisible ? '✅ 是' : '⚠️ 否'}`);
            
            if (logoVisible && emojiVisible && nameVisible) {
                console.log("✅ 所有关键元素都在可视区域内");
            } else {
                console.log("⚠️ 部分关键元素可能被裁剪");
            }
        }
    } else {
        console.log("❌ 未找到数字人内容或卡片");
    }
}

function testResponsiveHeightConsistency() {
    console.log("🔍 测试响应式高度一致性...");
    
    const width = window.innerWidth;
    let breakpoint = "";
    
    if (width >= 1024) {
        breakpoint = "桌面端 (≥1024px)";
        console.log("📱 当前断点: 桌面端 - 应保持高度一致");
        
        // 桌面端应该保持高度一致
        const result = testCardHeightConsistency();
        if (result && result.isConsistent) {
            console.log("✅ 桌面端高度一致性良好");
        } else {
            console.log("⚠️ 桌面端高度一致性需要改进");
        }
    } else if (width >= 768) {
        breakpoint = "平板端 (768-1023px)";
        console.log("📱 当前断点: 平板端 - 垂直布局");
    } else {
        breakpoint = "移动端 (<768px)";
        console.log("📱 当前断点: 移动端 - 垂直布局");
    }
    
    console.log(`📱 当前屏幕宽度: ${width}px (${breakpoint})`);
}

function testVisualAlignment() {
    console.log("🔍 检查视觉对齐效果...");
    
    const digitalContainer = document.querySelector('.digital-human-container');
    const chatContainer = document.querySelector('.chat-container');
    
    if (digitalContainer && chatContainer) {
        const digitalRect = digitalContainer.getBoundingClientRect();
        const chatRect = chatContainer.getBoundingClientRect();
        
        const topDiff = Math.abs(digitalRect.top - chatRect.top);
        const bottomDiff = Math.abs(digitalRect.bottom - chatRect.bottom);
        
        console.log(`📏 顶部对齐差异: ${topDiff.toFixed(1)}px`);
        console.log(`📏 底部对齐差异: ${bottomDiff.toFixed(1)}px`);
        
        if (topDiff <= 2 && bottomDiff <= 2) {
            console.log("✅ 视觉对齐效果良好");
        } else {
            console.log("⚠️ 视觉对齐可能需要调整");
        }
        
        // 检查是否在同一水平线上
        if (Math.abs(digitalRect.top - chatRect.top) <= 1) {
            console.log("✅ 两个卡片在同一水平线上");
        } else {
            console.log(`⚠️ 两个卡片不在同一水平线上，差异: ${Math.abs(digitalRect.top - chatRect.top).toFixed(1)}px`);
        }
    }
}

// 运行测试
console.log("🚀 开始卡片高度一致性测试...");

const heightResult = testCardHeightConsistency();

setTimeout(() => {
    testCardContainerHeights();
}, 500);

setTimeout(() => {
    testDigitalHumanCardCSS();
}, 1000);

setTimeout(() => {
    testDigitalHumanContentFit();
}, 1500);

setTimeout(() => {
    testResponsiveHeightConsistency();
}, 2000);

setTimeout(() => {
    testVisualAlignment();
}, 2500);

console.log("🎯 卡片高度一致性测试脚本运行完成");
console.log("💡 请观察:");
console.log("   1. 数字人卡片和聊天卡片高度是否一致");
console.log("   2. 两个卡片是否在同一水平线上");
console.log("   3. 数字人内容是否完整显示");
console.log("   4. 视觉效果是否协调统一");

// 返回测试结果
if (heightResult) {
    console.log("\\n📊 高度一致性测试结果:");
    console.log(`   数字人卡片: ${heightResult.digitalHeight}px`);
    console.log(`   聊天卡片: ${heightResult.chatHeight}px`);
    console.log(`   高度差异: ${heightResult.heightDiff}px`);
    console.log(`   一致性: ${heightResult.isConsistent ? '✅ 良好' : '❌ 需改进'}`);
}
"""
        
        with open("browser_height_consistency_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_height_consistency_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 卡片高度一致性测试说明")
        print("=" * 80)
        
        print("\n🎯 测试步骤:")
        print("1. 在浏览器中打开前端页面")
        print("2. 观察左侧数字人卡片和右侧聊天卡片的高度")
        print("3. 按F12打开开发者工具")
        print("4. 在Console标签中运行测试脚本")
        print("5. 检查两个卡片是否在同一水平线上")
        
        print("\n🔍 检查要点:")
        print("✓ 数字人卡片和聊天卡片高度完全一致")
        print("✓ 两个卡片的顶部和底部对齐")
        print("✓ 高度差异在5px以内（理想情况下为0px）")
        print("✓ 数字人内容在新高度下完整显示")
        print("✓ 视觉效果协调统一")
        
        print("\n📐 高度验证方法:")
        print("1. 在Elements标签中分别选择两个卡片元素")
        print("2. 查看Computed标签中的height值")
        print("3. 对比两个高度值是否相同")
        print("4. 使用测试脚本获得精确的差异数据")
        
        print("\n🔧 问题排查:")
        print("如果高度不一致，检查以下项目:")
        print("- 两个容器是否都使用了fullscreen-card-height类")
        print("- 数字人卡片是否使用了h-full类")
        print("- 是否有aspect-ratio限制影响高度")
        print("- CSS中是否有冲突的高度设置")
        
        print("\n🎨 预期效果:")
        print("修复后应该看到:")
        print("- 左右两个卡片高度完全相同")
        print("- 两个卡片顶部和底部完美对齐")
        print("- 数字人内容适应新的高度并正确显示")
        print("- 整体界面更加协调统一")
        
        print("\n📱 响应式测试:")
        print("- 桌面端 (≥1024px): 应保持高度一致")
        print("- 平板端 (768-1023px): 垂直布局，高度可以不同")
        print("- 移动端 (<768px): 垂直布局，高度可以不同")
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败")
            return False
        
        # 2. 打开浏览器
        print("\n🌐 打开浏览器进行卡片高度一致性测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 3. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 4. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 卡片高度一致性测试准备完成！")
        print("💡 请在浏览器中验证修复效果")
        print("📋 运行测试脚本以获得详细的高度分析")
        
        return True

def main():
    """主函数"""
    tester = CardHeightConsistencyTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
