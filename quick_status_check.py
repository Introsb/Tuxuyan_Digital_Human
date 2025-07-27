#!/usr/bin/env python3
"""
快速状态检查
"""

import requests
import webbrowser

def check_services():
    """检查服务状态"""
    print("🔍 检查服务状态...")
    
    # 检查后端
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ 后端服务正常")
            print(f"   版本: {data.get('version', '未知')}")
            print(f"   功能: {data.get('features', [])}")
            backend_ok = True
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            backend_ok = False
    except Exception as e:
        print(f"❌ 后端服务无法访问: {e}")
        backend_ok = False
    
    # 检查前端
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常")
            print(f"   页面大小: {len(response.content)} bytes")
            frontend_ok = True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            frontend_ok = False
    except Exception as e:
        print(f"❌ 前端服务无法访问: {e}")
        frontend_ok = False
    
    # 测试聊天功能
    if backend_ok:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask_professor",
                json={"message": "你好"},
                timeout=20
            )
            if response.status_code == 200:
                result = response.json()
                print("✅ 聊天功能正常")
                print(f"   回复: {result.get('answer', '无回复')[:50]}...")
                chat_ok = True
            else:
                print(f"❌ 聊天功能异常: {response.status_code}")
                chat_ok = False
        except Exception as e:
            print(f"❌ 聊天功能测试失败: {e}")
            chat_ok = False
    else:
        chat_ok = False
    
    print("\n📊 服务状态总结:")
    print(f"   后端服务: {'✅' if backend_ok else '❌'}")
    print(f"   前端服务: {'✅' if frontend_ok else '❌'}")
    print(f"   聊天功能: {'✅' if chat_ok else '❌'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 服务启动成功！")
        print("🌐 访问地址:")
        print("   前端界面: http://localhost:3000")
        print("   后端API: http://127.0.0.1:8000")
        
        # 打开浏览器
        try:
            webbrowser.open("http://localhost:3000")
            print("🌐 已在浏览器中打开项目界面")
        except:
            print("⚠️  无法自动打开浏览器")
        
        return True
    else:
        print("\n❌ 部分服务未正常启动")
        return False

if __name__ == "__main__":
    check_services()
