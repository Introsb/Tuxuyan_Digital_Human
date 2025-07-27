#!/usr/bin/env python3
"""
强制刷新测试脚本
"""

import webbrowser
import time

def main():
    print("🔄 强制刷新浏览器...")
    
    # 打开项目页面
    webbrowser.open("http://localhost:3000")
    time.sleep(2)
    
    print("✅ 页面已刷新")
    print("💡 请检查以下内容:")
    print("   1. 数字人卡片是否比聊天卡片明显更窄")
    print("   2. 两个卡片的高度是否完全一致")
    print("   3. 数字人卡片是否呈现竖屏比例（高>宽）")
    
    print("\n🔧 如果仍然不正确，请按F12打开开发者工具，在Console中运行:")
    print("const digital = document.querySelector('.digital-human-card');")
    print("const chat = document.querySelector('.fullscreen-chat-card');")
    print("console.log('数字人:', digital.offsetWidth + 'x' + digital.offsetHeight);")
    print("console.log('聊天:', chat.offsetWidth + 'x' + chat.offsetHeight);")
    print("console.log('比例:', (digital.offsetWidth / digital.offsetHeight).toFixed(4));")

if __name__ == "__main__":
    main()
