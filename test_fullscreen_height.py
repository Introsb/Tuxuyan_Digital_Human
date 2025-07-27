#!/usr/bin/env python3
"""
全屏高度聊天界面测试脚本
验证聊天卡片能够铺满整个可视屏幕区域
"""

import requests
import time
import subprocess
import webbrowser
from pathlib import Path

class FullscreenHeightTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("🖥️  涂序彦教授数字人项目 - 全屏高度聊天界面测试")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 聊天卡片铺满整个可视屏幕区域")
        print("   - 使用100vh视口单位实现真正全屏")
        print("   - 响应式适配不同屏幕尺寸")
        print("   - 移动端考虑浏览器地址栏动态高度")
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
    
    def send_test_messages(self):
        """发送测试消息"""
        print("\n📤 发送测试消息...")
        
        test_messages = [
            "你好，这是全屏高度测试",
            "请介绍一下人工智能的基本概念",
            "什么是深度学习？",
            "请详细解释神经网络的工作原理",
            "人工智能的未来发展趋势如何？"
        ]
        
        success_count = 0
        
        for i, message in enumerate(test_messages, 1):
            print(f"📝 发送消息 {i}/{len(test_messages)}: {message[:30]}...")
            
            try:
                response = requests.post(
                    f"{self.backend_url}/ask_professor",
                    json={"prompt": message},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer_length = len(result.get('answer', ''))
                    print(f"✅ 消息 {i} 成功，回复长度: {answer_length}字符")
                    success_count += 1
                else:
                    print(f"❌ 消息 {i} 失败: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ 消息 {i} 异常: {e}")
            
            if i < len(test_messages):
                time.sleep(2)
        
        print(f"\n📊 消息发送结果: {success_count}/{len(test_messages)} 成功")
        return success_count
    
    def create_browser_test_script(self):
        """创建浏览器测试脚本"""
        test_script = """
// 全屏高度聊天界面测试脚本
// 在浏览器控制台中运行

console.log("🖥️ 开始全屏高度聊天界面测试...");

function getViewportInfo() {
    return {
        windowHeight: window.innerHeight,
        windowWidth: window.innerWidth,
        documentHeight: document.documentElement.clientHeight,
        screenHeight: screen.height,
        screenWidth: screen.width,
        devicePixelRatio: window.devicePixelRatio
    };
}

function testFullscreenHeight() {
    console.log("📐 检查全屏高度适配...");
    
    const viewport = getViewportInfo();
    console.log("🖥️ 视口信息:", viewport);
    
    // 检查聊天容器
    const chatContainer = document.querySelector('.fullscreen-chat-container');
    if (chatContainer) {
        const containerHeight = chatContainer.offsetHeight;
        const containerRect = chatContainer.getBoundingClientRect();
        
        console.log(`📏 聊天容器高度: ${containerHeight}px`);
        console.log(`📏 视口高度: ${viewport.windowHeight}px`);
        console.log(`📏 高度比例: ${(containerHeight / viewport.windowHeight * 100).toFixed(1)}%`);
        
        if (Math.abs(containerHeight - viewport.windowHeight) <= 5) {
            console.log("✅ 聊天容器正确铺满屏幕高度");
        } else {
            console.log(`⚠️ 聊天容器高度异常，差值: ${Math.abs(containerHeight - viewport.windowHeight)}px`);
        }
    } else {
        console.log("❌ 未找到全屏聊天容器");
    }
    
    // 检查卡片高度
    const chatCard = document.querySelector('.fullscreen-chat-card');
    const digitalHumanCard = document.querySelector('.fullscreen-card-height');
    
    if (chatCard && digitalHumanCard) {
        const chatCardHeight = chatCard.offsetHeight;
        const digitalHumanHeight = digitalHumanCard.offsetHeight;
        
        console.log(`📏 聊天卡片高度: ${chatCardHeight}px`);
        console.log(`📏 数字人卡片高度: ${digitalHumanHeight}px`);
        
        if (Math.abs(chatCardHeight - digitalHumanHeight) <= 5) {
            console.log("✅ 左右卡片高度一致");
        } else {
            console.log(`⚠️ 左右卡片高度不一致，差值: ${Math.abs(chatCardHeight - digitalHumanHeight)}px`);
        }
    }
    
    // 检查CSS变量
    const rootStyle = getComputedStyle(document.documentElement);
    const vhValue = rootStyle.getPropertyValue('--vh');
    if (vhValue) {
        console.log(`📏 自定义--vh变量: ${vhValue}`);
        console.log("✅ 动态视口高度变量已设置");
    } else {
        console.log("⚠️ 未找到自定义--vh变量");
    }
}

function testResponsiveBreakpoints() {
    console.log("📱 测试响应式断点...");
    
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
    
    // 检查对应的CSS类是否生效
    const chatCard = document.querySelector('.fullscreen-chat-card');
    if (chatCard) {
        const computedStyle = getComputedStyle(chatCard);
        console.log(`📏 计算后的高度: ${computedStyle.height}`);
        console.log(`📏 最小高度: ${computedStyle.minHeight}`);
        console.log(`📏 最大高度: ${computedStyle.maxHeight}`);
    }
}

function testScrollBehavior() {
    console.log("🔄 测试滚动行为...");
    
    const messagesContainer = document.querySelector('.chat-messages-container');
    if (messagesContainer) {
        const isScrollable = messagesContainer.scrollHeight > messagesContainer.clientHeight;
        console.log(`📜 消息容器可滚动: ${isScrollable ? '是' : '否'}`);
        console.log(`📜 滚动高度: ${messagesContainer.scrollHeight}px`);
        console.log(`📜 可视高度: ${messagesContainer.clientHeight}px`);
        
        if (isScrollable) {
            console.log("✅ 消息容器滚动功能正常");
            
            // 测试滚动到底部
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            setTimeout(() => {
                const isAtBottom = messagesContainer.scrollTop + messagesContainer.clientHeight >= messagesContainer.scrollHeight - 10;
                console.log(`📜 滚动到底部: ${isAtBottom ? '成功' : '失败'}`);
            }, 500);
        }
    }
}

function simulateWindowResize() {
    console.log("🔄 模拟窗口大小变化...");
    
    const originalHeight = window.innerHeight;
    console.log(`📏 原始窗口高度: ${originalHeight}px`);
    
    // 监听resize事件
    let resizeCount = 0;
    const resizeHandler = () => {
        resizeCount++;
        console.log(`🔄 窗口大小变化 ${resizeCount}: ${window.innerWidth}x${window.innerHeight}`);
        
        // 检查--vh变量是否更新
        const rootStyle = getComputedStyle(document.documentElement);
        const vhValue = rootStyle.getPropertyValue('--vh');
        console.log(`📏 更新后的--vh: ${vhValue}`);
        
        if (resizeCount >= 3) {
            window.removeEventListener('resize', resizeHandler);
            console.log("✅ 窗口大小变化测试完成");
        }
    };
    
    window.addEventListener('resize', resizeHandler);
    
    console.log("💡 请手动调整浏览器窗口大小来测试响应式效果");
}

// 运行测试
console.log("🚀 开始全屏高度测试...");

testFullscreenHeight();

setTimeout(() => {
    testResponsiveBreakpoints();
}, 1000);

setTimeout(() => {
    testScrollBehavior();
}, 2000);

setTimeout(() => {
    simulateWindowResize();
}, 3000);

console.log("🎯 全屏高度测试脚本运行完成");
console.log("💡 请观察:");
console.log("   1. 聊天卡片是否铺满整个屏幕高度");
console.log("   2. 左右卡片高度是否一致");
console.log("   3. 调整窗口大小时是否正确响应");
console.log("   4. 移动端是否考虑了地址栏高度");
"""
        
        with open("browser_fullscreen_test.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("📄 浏览器测试脚本已创建: browser_fullscreen_test.js")
    
    def provide_manual_test_instructions(self):
        """提供手动测试说明"""
        print("\n" + "=" * 80)
        print("📋 全屏高度测试说明")
        print("=" * 80)
        
        print("\n🎯 测试步骤:")
        print("1. 在浏览器中打开前端页面")
        print("2. 观察聊天卡片是否铺满整个屏幕高度")
        print("3. 调整浏览器窗口大小，观察响应式效果")
        print("4. 在移动设备上测试地址栏隐藏/显示效果")
        print("5. 发送多条消息，验证滚动功能正常")
        
        print("\n🔍 检查要点:")
        print("✓ 聊天卡片高度 = 浏览器窗口高度")
        print("✓ 左右两个卡片高度完全一致")
        print("✓ 没有多余的空白区域")
        print("✓ 消息区域滚动正常")
        print("✓ 输入框始终在底部可见")
        print("✓ 窗口大小变化时动态调整")
        
        print("\n📱 响应式测试:")
        print("- 桌面端 (≥1024px): 使用100vh减去padding")
        print("- 平板端 (768-1023px): 调整padding适配")
        print("- 移动端 (<768px): 使用动态视口高度")
        
        print("\n🛠️ 开发者工具检查:")
        print("1. Elements标签: 检查.fullscreen-chat-card的CSS")
        print("2. Console标签: 运行测试脚本")
        print("3. 检查--vh CSS变量是否正确设置")
        print("4. 观察窗口resize时的高度变化")
        
        print("\n🐛 常见问题排查:")
        print("- 如果高度不是100%: 检查CSS中的vh单位")
        print("- 如果移动端有问题: 检查--vh变量和dvh支持")
        print("- 如果响应式异常: 检查媒体查询断点")
        print("- 如果滚动异常: 检查overflow属性设置")
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败")
            return False
        
        # 2. 发送测试消息
        success_count = self.send_test_messages()
        
        # 3. 打开浏览器
        print("\n🌐 打开浏览器进行全屏高度测试...")
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
        
        # 4. 创建浏览器测试脚本
        self.create_browser_test_script()
        
        # 5. 提供手动测试说明
        self.provide_manual_test_instructions()
        
        print("\n🎉 全屏高度聊天界面测试准备完成！")
        print("💡 请在浏览器中验证全屏高度效果")
        print(f"📊 测试消息发送成功率: {success_count}/5")
        
        return True

def main():
    """主函数"""
    tester = FullscreenHeightTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
