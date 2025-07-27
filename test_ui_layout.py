#!/usr/bin/env python3
"""
UI布局测试脚本
验证新的统一卡片式界面是否正常工作
"""

import subprocess
import time
import requests
import webbrowser
from pathlib import Path

class UILayoutTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 70)
        print("🎨 涂序彦教授数字人项目 - UI布局测试")
        print("=" * 70)
        print("📱 测试新的统一卡片式界面布局")
        print("🔧 验证输入框移动到聊天区域底部")
        print("=" * 70)
    
    def check_services(self):
        """检查服务状态"""
        print("\n🔍 检查服务状态...")
        
        # 检查后端
        try:
            response = requests.get(self.backend_url, timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务正常运行")
                backend_ok = True
            else:
                print(f"❌ 后端服务异常: {response.status_code}")
                backend_ok = False
        except:
            print("❌ 后端服务无法访问")
            backend_ok = False
        
        # 检查前端
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务正常运行")
                frontend_ok = True
            else:
                print(f"❌ 前端服务异常: {response.status_code}")
                frontend_ok = False
        except:
            print("❌ 前端服务无法访问")
            frontend_ok = False
        
        return backend_ok, frontend_ok
    
    def start_services_if_needed(self):
        """如果需要，启动服务"""
        print("\n🚀 检查并启动必要的服务...")
        
        backend_ok, frontend_ok = self.check_services()
        
        if not backend_ok or not frontend_ok:
            print("⚠️  部分服务未运行，尝试启动...")
            
            try:
                # 使用quick_start.py启动服务
                print("📡 启动项目服务...")
                subprocess.Popen([
                    "python3", "quick_start.py"
                ], cwd=self.project_root)
                
                print("⏳ 等待服务启动...")
                time.sleep(15)
                
                # 重新检查
                backend_ok, frontend_ok = self.check_services()
                
                if backend_ok and frontend_ok:
                    print("✅ 所有服务启动成功")
                    return True
                else:
                    print("❌ 部分服务启动失败")
                    return False
                    
            except Exception as e:
                print(f"❌ 启动服务失败: {e}")
                return False
        else:
            print("✅ 所有服务已运行")
            return True
    
    def test_api_functionality(self):
        """测试API功能"""
        print("\n🧪 测试API功能...")
        
        try:
            test_data = {"prompt": "UI布局测试消息"}
            
            response = requests.post(
                f"{self.backend_url}/ask_professor",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API功能正常")
                print(f"📝 回复长度: {len(result.get('answer', ''))}字符")
                return True
            else:
                print(f"❌ API调用失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API测试异常: {e}")
            return False
    
    def open_frontend_for_testing(self):
        """打开前端进行手动测试"""
        print("\n🌐 打开前端进行UI测试...")
        
        try:
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
            return True
        except Exception as e:
            print(f"❌ 无法打开浏览器: {e}")
            return False
    
    def provide_testing_instructions(self):
        """提供测试说明"""
        print("\n" + "=" * 70)
        print("📋 UI布局测试说明")
        print("=" * 70)
        
        print("\n🎯 请在浏览器中验证以下内容:")
        print("1. 界面布局:")
        print("   ✓ 左侧：数字人卡片")
        print("   ✓ 右侧：统一的聊天卡片")
        print("   ✓ 聊天卡片包含消息区域和输入框")
        
        print("\n2. 输入框位置:")
        print("   ✓ 输入框位于聊天卡片底部")
        print("   ✓ 输入框有清晰的边界分隔")
        print("   ✓ 发送按钮在输入框内右侧")
        
        print("\n3. 功能按钮:")
        print("   ✓ 录音按钮在输入框右侧")
        print("   ✓ 语音播放开关在录音按钮旁边")
        print("   ✓ 所有按钮都有合适的间距")
        
        print("\n4. 消息显示:")
        print("   ✓ 消息在聊天卡片上方区域显示")
        print("   ✓ 消息区域可以正常滚动")
        print("   ✓ 新消息会自动滚动到底部")
        
        print("\n5. 响应式设计:")
        print("   ✓ 在不同屏幕尺寸下布局正常")
        print("   ✓ 移动设备上界面适配良好")
        
        print("\n🧪 测试步骤:")
        print("1. 发送一条测试消息")
        print("2. 观察AI回复是否正常显示")
        print("3. 检查输入框是否保持在底部")
        print("4. 测试录音和语音播放功能")
        print("5. 调整浏览器窗口大小测试响应式")
        
        print("\n💡 如果发现问题:")
        print("- 按F12打开开发者工具")
        print("- 检查Console标签的错误信息")
        print("- 检查Network标签的API请求")
        print("- 截图并记录具体问题")
    
    def create_ui_test_checklist(self):
        """创建UI测试检查清单"""
        checklist = """
# UI布局测试检查清单

## ✅ 基础布局
- [ ] 左侧数字人卡片正常显示
- [ ] 右侧聊天卡片正常显示
- [ ] 两个卡片高度一致
- [ ] 卡片间距合适

## ✅ 聊天卡片结构
- [ ] 顶部校徽区域正常
- [ ] 中间消息区域可滚动
- [ ] 底部输入框固定位置
- [ ] 输入框与消息区域有清晰分隔

## ✅ 输入框功能
- [ ] 输入框可以正常输入文字
- [ ] 发送按钮位于输入框内右侧
- [ ] 录音按钮在输入框外右侧
- [ ] 语音播放开关正常工作
- [ ] 按Enter键可以发送消息

## ✅ 消息显示
- [ ] 用户消息显示在右侧
- [ ] AI消息显示在左侧
- [ ] 消息格式正确（Markdown渲染）
- [ ] 新消息自动滚动到底部
- [ ] 思考状态正常显示

## ✅ 交互功能
- [ ] 发送消息功能正常
- [ ] AI回复正常显示
- [ ] 语音录制功能正常
- [ ] 语音播放功能正常
- [ ] 重试功能正常

## ✅ 响应式设计
- [ ] 桌面端布局正常
- [ ] 平板端布局适配
- [ ] 手机端布局适配
- [ ] 窗口缩放时布局正常

## ✅ 视觉效果
- [ ] 卡片圆角和阴影正常
- [ ] 颜色搭配协调
- [ ] 字体大小合适
- [ ] 按钮状态变化正常
- [ ] 动画效果流畅

## 🐛 问题记录
记录发现的任何问题：
1. 
2. 
3. 

## 📝 改进建议
记录改进建议：
1. 
2. 
3. 
"""
        
        with open("UI_TEST_CHECKLIST.md", "w", encoding="utf-8") as f:
            f.write(checklist)
        
        print(f"📄 UI测试检查清单已创建: UI_TEST_CHECKLIST.md")
    
    def run_full_test(self):
        """运行完整的UI测试"""
        self.print_banner()
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败，无法进行UI测试")
            return False
        
        # 2. 测试API功能
        if not self.test_api_functionality():
            print("⚠️  API功能异常，但继续UI测试")
        
        # 3. 打开前端
        if not self.open_frontend_for_testing():
            print("❌ 无法打开前端，请手动访问: http://localhost:3000")
        
        # 4. 提供测试说明
        self.provide_testing_instructions()
        
        # 5. 创建测试检查清单
        self.create_ui_test_checklist()
        
        print("\n🎉 UI布局测试准备完成！")
        print("💡 请按照上述说明在浏览器中进行测试")
        
        return True

def main():
    """主函数"""
    tester = UILayoutTester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
