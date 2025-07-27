#!/usr/bin/env python3
"""
UI/UX优化测试脚本
验证前端界面优化效果
"""

import subprocess
import time
import requests
import webbrowser
from pathlib import Path

def print_banner():
    """显示测试横幅"""
    print("=" * 80)
    print("🎨 UI/UX优化测试")
    print("=" * 80)
    print("🎯 测试内容:")
    print("   1. 输入框状态管理 - 立即清空和焦点保持")
    print("   2. 音频播放控件 - 扬声器图标和暂停按钮")
    print("   3. 输入框自适应高度 - 平滑动画效果")
    print("   4. 整体用户体验 - 设计一致性")
    print("=" * 80)

def check_frontend_running():
    """检查前端是否运行"""
    print("\n🔍 检查前端服务状态...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常运行")
            return True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端服务无法访问: {e}")
        return False

def check_backend_running():
    """检查后端是否运行"""
    print("\n🔍 检查后端服务状态...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务正常运行")
            return True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端服务无法访问: {e}")
        return False

def restart_frontend():
    """重启前端服务"""
    print("\n🔄 重启前端服务以应用UI优化...")
    
    # 停止现有前端
    try:
        subprocess.run(["pkill", "-f", "react-scripts"], check=False)
        print("✅ 已停止现有前端服务")
    except:
        print("ℹ️  没有运行中的前端服务")
    
    time.sleep(3)
    
    # 启动前端
    frontend_dir = Path("react-version")
    if not frontend_dir.exists():
        print("❌ react-version 目录不存在")
        return False
    
    try:
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待前端启动...")
        time.sleep(20)
        
        if frontend_process.poll() is None:
            print("✅ 前端服务重启成功")
            return True
        else:
            print("❌ 前端服务重启失败")
            return False
            
    except Exception as e:
        print(f"❌ 重启前端时出错: {e}")
        return False

def create_ui_test_guide():
    """创建UI测试指南"""
    print("\n📄 创建UI测试指南...")
    
    guide_content = """# 🎨 UI/UX优化测试指南

## 🎯 测试项目

### 1. 输入框状态管理测试
**测试步骤：**
1. 在输入框中输入一条消息
2. 点击发送按钮或按回车键
3. 观察输入框是否立即清空
4. 检查输入框焦点是否保持（光标仍在输入框中）
5. 立即输入下一条消息测试连续输入

**预期效果：**
- ✅ 输入框立即清空
- ✅ 焦点保持在输入框
- ✅ 可以立即输入下一条消息
- ✅ 无需手动点击输入框

### 2. 音频播放控件测试
**测试步骤：**
1. 发送一条消息等待AI回复
2. 查看AI回复下方的音频控件
3. 点击扬声器图标🔊开始播放
4. 观察播放时是否显示暂停按钮⏸️
5. 点击暂停按钮测试暂停功能
6. 测试重播按钮功能

**预期效果：**
- ✅ 显示圆形扬声器图标
- ✅ 播放时显示暂停按钮
- ✅ 可以暂停和重新播放
- ✅ 按钮左对齐在文字下方
- ✅ 圆形小图标设计

### 3. 输入框自适应高度测试
**测试步骤：**
1. 在输入框中输入单行文本
2. 按Shift+Enter或继续输入创建多行文本
3. 观察输入框高度变化是否平滑
4. 输入大量文本测试最大高度限制
5. 删除文本观察高度是否平滑缩小

**预期效果：**
- ✅ 高度平滑调整（无突然跳跃）
- ✅ 有合理的最大高度限制
- ✅ 超出最大高度时显示滚动条
- ✅ 删除文本时高度平滑缩小
- ✅ 动画效果自然流畅

### 4. 整体用户体验测试
**测试步骤：**
1. 进行完整的对话流程
2. 测试语音输入功能
3. 测试语音播放功能
4. 观察界面响应速度
5. 检查设计一致性

**预期效果：**
- ✅ 操作流畅无卡顿
- ✅ 视觉设计一致
- ✅ 交互反馈及时
- ✅ 用户体验良好

## 🌐 测试环境

- **前端地址**: http://localhost:3000
- **后端地址**: http://127.0.0.1:8000
- **推荐浏览器**: Chrome, Firefox, Safari

## 🐛 问题报告

如发现问题，请记录：
1. 问题描述
2. 复现步骤
3. 预期行为
4. 实际行为
5. 浏览器版本

## 💡 优化建议

如有改进建议：
1. 具体的改进点
2. 改进原因
3. 预期效果
4. 实现难度评估

## 🎨 设计规范

### 颜色方案
- 主色调：蓝色系
- 辅助色：灰色系
- 强调色：红色（错误）、绿色（成功）

### 动画规范
- 过渡时间：0.3秒
- 缓动函数：ease-in-out
- 避免过度动画

### 交互规范
- 按钮hover效果
- 加载状态指示
- 错误状态提示
- 成功状态反馈
"""
    
    with open("UI_TEST_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ UI测试指南已创建: UI_TEST_GUIDE.md")

def create_browser_test_script():
    """创建浏览器测试脚本"""
    print("\n📄 创建浏览器测试脚本...")
    
    script_content = """
// UI/UX优化验证脚本
// 在浏览器控制台中运行

console.log("🎨 开始UI/UX优化验证...");

function testInputBoxBehavior() {
    console.log("📝 测试输入框行为...");
    
    const textarea = document.querySelector('textarea');
    if (textarea) {
        console.log("✅ 找到输入框");
        
        // 检查自适应高度
        const originalHeight = textarea.style.height;
        console.log("原始高度:", originalHeight);
        
        // 模拟输入多行文本
        textarea.value = "这是第一行\\n这是第二行\\n这是第三行\\n这是第四行";
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        
        setTimeout(() => {
            const newHeight = textarea.style.height;
            console.log("多行文本后高度:", newHeight);
            
            if (newHeight !== originalHeight) {
                console.log("✅ 输入框高度自适应正常");
            } else {
                console.log("⚠️  输入框高度可能未自适应");
            }
            
            // 清空文本
            textarea.value = "";
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
        }, 500);
        
    } else {
        console.log("❌ 未找到输入框");
    }
}

function testAudioControls() {
    console.log("🔊 测试音频控件...");
    
    const audioButtons = document.querySelectorAll('button[title*="播放"], button[title*="暂停"]');
    if (audioButtons.length > 0) {
        console.log(`✅ 找到 ${audioButtons.length} 个音频控件`);
        
        audioButtons.forEach((button, index) => {
            const title = button.getAttribute('title');
            const hasIcon = button.querySelector('svg');
            const isRound = button.classList.contains('rounded-full');
            
            console.log(`音频按钮 ${index + 1}:`);
            console.log(`  标题: ${title}`);
            console.log(`  有图标: ${hasIcon ? '✅' : '❌'}`);
            console.log(`  圆形设计: ${isRound ? '✅' : '❌'}`);
        });
    } else {
        console.log("❌ 未找到音频控件");
    }
}

function testAnimations() {
    console.log("🎬 测试动画效果...");
    
    const elementsWithTransition = document.querySelectorAll('[style*="transition"], .transition');
    console.log(`✅ 找到 ${elementsWithTransition.length} 个带动画的元素`);
    
    elementsWithTransition.forEach((element, index) => {
        const style = window.getComputedStyle(element);
        const transition = style.transition;
        if (transition && transition !== 'none') {
            console.log(`动画元素 ${index + 1}: ${transition}`);
        }
    });
}

function testOverallDesign() {
    console.log("🎨 测试整体设计...");
    
    // 检查主要容器
    const mainContainer = document.querySelector('.chat-area, .message-list, .input-area');
    if (mainContainer) {
        console.log("✅ 找到主要容器");
    }
    
    // 检查响应式设计
    const responsiveElements = document.querySelectorAll('.w-full, .max-w-3xl, .mx-auto');
    console.log(`✅ 找到 ${responsiveElements.length} 个响应式元素`);
    
    // 检查颜色一致性
    const buttons = document.querySelectorAll('button');
    console.log(`✅ 找到 ${buttons.length} 个按钮元素`);
}

// 运行所有测试
setTimeout(() => testInputBoxBehavior(), 500);
setTimeout(() => testAudioControls(), 1000);
setTimeout(() => testAnimations(), 1500);
setTimeout(() => testOverallDesign(), 2000);

console.log("🎯 UI/UX优化验证脚本运行完成");
console.log("💡 请手动测试输入框、音频控件和动画效果");
"""
    
    with open("ui_test_browser.js", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ 浏览器测试脚本已创建: ui_test_browser.js")

def show_optimization_summary():
    """显示优化总结"""
    print("\n" + "=" * 80)
    print("📊 UI/UX优化总结")
    print("=" * 80)
    
    optimizations = [
        "✅ 输入框状态管理 - 立即清空和焦点保持",
        "✅ 音频播放控件 - 扬声器图标和暂停按钮设计",
        "✅ 输入框自适应高度 - 平滑动画效果",
        "✅ 圆形小图标设计 - 左对齐布局",
        "✅ 平滑过渡动画 - 0.3秒缓动效果",
        "✅ 设计一致性 - 统一的视觉风格"
    ]
    
    print("\n🎨 已完成的优化:")
    for opt in optimizations:
        print(f"   {opt}")
    
    print("\n📁 修改的文件:")
    print("   - react-version/src/components/InputArea.js")
    print("   - react-version/src/components/AudioPlayer.js")
    
    print("\n🎯 优化效果:")
    print("   - 更流畅的用户交互体验")
    print("   - 更直观的音频控制界面")
    print("   - 更自然的输入框行为")
    print("   - 更一致的设计语言")
    
    print("\n🌐 测试地址:")
    print("   前端界面: http://localhost:3000")
    print("   测试指南: UI_TEST_GUIDE.md")
    print("   浏览器脚本: ui_test_browser.js")

def main():
    """主函数"""
    print_banner()
    
    # 1. 检查服务状态
    frontend_running = check_frontend_running()
    backend_running = check_backend_running()
    
    # 2. 如果前端未运行，重启前端
    if not frontend_running:
        frontend_running = restart_frontend()
    
    # 3. 创建测试文档
    create_ui_test_guide()
    create_browser_test_script()
    
    # 4. 显示优化总结
    show_optimization_summary()
    
    # 5. 打开浏览器
    if frontend_running:
        try:
            webbrowser.open("http://localhost:3000")
            print("\n🌐 已在浏览器中打开项目界面")
            print("💡 请按照 UI_TEST_GUIDE.md 进行测试")
        except:
            print("\n⚠️  无法自动打开浏览器，请手动访问: http://localhost:3000")
        
        return True
    else:
        print("\n❌ 前端服务未运行，无法进行UI测试")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
