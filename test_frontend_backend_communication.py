#!/usr/bin/env python3
"""
前后端通信诊断脚本
测试前端和后端之间的数据传输和显示问题
"""

import requests
import time
import json
import subprocess
import webbrowser
from datetime import datetime

class FrontendBackendTester:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("🔍 涂序彦教授数字人项目 - 前后端通信诊断")
        print("=" * 80)
        print(f"📡 后端地址: {self.backend_url}")
        print(f"🌐 前端地址: {self.frontend_url}")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
    
    def test_backend_status(self):
        """测试后端状态"""
        print("\n🔧 测试后端服务状态...")
        
        try:
            # 测试健康检查端点
            response = requests.get(f"{self.backend_url}/", timeout=5)
            if response.status_code == 200:
                result = response.json()
                print("✅ 后端服务器正常运行")
                print(f"📋 服务器信息: {result.get('message', '')}")
                print(f"🎯 服务器类型: {result.get('server_type', '')}")
                return True
            else:
                print(f"❌ 后端服务器异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 后端服务器无法访问: {e}")
            return False
    
    def test_frontend_status(self):
        """测试前端状态"""
        print("\n🌐 测试前端服务状态...")
        
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("✅ 前端服务器正常运行")
                print(f"📄 页面大小: {len(response.text)} 字符")
                return True
            else:
                print(f"❌ 前端服务器异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 前端服务器无法访问: {e}")
            return False
    
    def test_cors_configuration(self):
        """测试CORS配置"""
        print("\n🔒 测试CORS跨域配置...")
        
        try:
            # 模拟前端的OPTIONS预检请求
            response = requests.options(
                f"{self.backend_url}/ask_professor",
                headers={
                    'Origin': self.frontend_url,
                    'Access-Control-Request-Method': 'POST',
                    'Access-Control-Request-Headers': 'Content-Type'
                },
                timeout=5
            )
            
            print(f"📊 OPTIONS请求状态: {response.status_code}")
            
            # 检查CORS头
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            print("🔍 CORS响应头:")
            for header, value in cors_headers.items():
                if value:
                    print(f"   ✅ {header}: {value}")
                else:
                    print(f"   ❌ {header}: 未设置")
            
            # 检查是否允许前端域名
            allow_origin = cors_headers.get('Access-Control-Allow-Origin')
            if allow_origin == '*' or self.frontend_url in str(allow_origin):
                print("✅ CORS配置允许前端访问")
                return True
            else:
                print("❌ CORS配置可能阻止前端访问")
                return False
                
        except Exception as e:
            print(f"❌ CORS测试失败: {e}")
            return False
    
    def test_api_endpoint_directly(self):
        """直接测试API端点"""
        print("\n🧪 直接测试API端点...")
        
        test_data = {
            "prompt": "你好，这是前后端通信测试"
        }
        
        try:
            print(f"📤 发送测试请求: {test_data['prompt']}")
            
            # 模拟前端的请求
            response = requests.post(
                f"{self.backend_url}/ask_professor",
                json=test_data,
                headers={
                    'Content-Type': 'application/json',
                    'Origin': self.frontend_url
                },
                timeout=60
            )
            
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📋 响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API调用成功")
                print(f"🔧 数据源: {result.get('source', 'unknown')}")
                print(f"🔢 使用tokens: {result.get('tokens_used', 0)}")
                print(f"📝 回复长度: {len(result.get('answer', ''))}")
                print(f"📄 回复预览: {result.get('answer', '')[:100]}...")
                
                # 验证响应格式
                required_fields = ['answer', 'source']
                missing_fields = [field for field in required_fields if field not in result]
                
                if not missing_fields:
                    print("✅ 响应格式正确")
                    return True, result
                else:
                    print(f"⚠️  响应缺少字段: {missing_fields}")
                    return False, result
            else:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"📄 错误内容: {response.text}")
                return False, None
                
        except Exception as e:
            print(f"❌ API测试失败: {e}")
            return False, None
    
    def test_json_response_format(self, api_result):
        """测试JSON响应格式"""
        print("\n📋 测试JSON响应格式...")
        
        if not api_result:
            print("❌ 没有API响应数据可测试")
            return False
        
        try:
            # 检查必需字段
            required_fields = {
                'answer': str,
                'source': str,
                'thinking_time': (int, float),
                'tokens_used': int
            }
            
            print("🔍 检查响应字段:")
            all_valid = True
            
            for field, expected_type in required_fields.items():
                if field in api_result:
                    value = api_result[field]
                    if isinstance(value, expected_type):
                        print(f"   ✅ {field}: {type(value).__name__} = {str(value)[:50]}")
                    else:
                        print(f"   ⚠️  {field}: 类型错误，期望 {expected_type.__name__}，实际 {type(value).__name__}")
                        all_valid = False
                else:
                    print(f"   ❌ {field}: 字段缺失")
                    all_valid = False
            
            # 检查answer字段是否为空
            answer = api_result.get('answer', '')
            if answer and len(answer.strip()) > 0:
                print("✅ answer字段包含有效内容")
            else:
                print("❌ answer字段为空或无效")
                all_valid = False
            
            return all_valid
            
        except Exception as e:
            print(f"❌ JSON格式检查失败: {e}")
            return False
    
    def generate_frontend_test_script(self):
        """生成前端测试脚本"""
        print("\n📝 生成前端测试脚本...")
        
        test_script = """
// 前端通信测试脚本 - 在浏览器控制台中运行
console.log("🧪 开始前端通信测试...");

// 测试函数
async function testFrontendBackendCommunication() {
    const backendUrl = 'http://127.0.0.1:8000';
    const testData = {
        prompt: "前端测试消息"
    };
    
    try {
        console.log("📤 发送请求到后端...");
        console.log("请求数据:", testData);
        
        const response = await fetch(`${backendUrl}/ask_professor`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        });
        
        console.log("📊 响应状态:", response.status);
        console.log("📋 响应头:", Object.fromEntries(response.headers.entries()));
        
        if (response.ok) {
            const result = await response.json();
            console.log("✅ 请求成功!");
            console.log("📄 响应数据:", result);
            
            // 检查响应格式
            const requiredFields = ['answer', 'source'];
            const missingFields = requiredFields.filter(field => !(field in result));
            
            if (missingFields.length === 0) {
                console.log("✅ 响应格式正确");
                console.log("📝 AI回复:", result.answer);
                return result;
            } else {
                console.error("❌ 响应格式错误，缺少字段:", missingFields);
                return null;
            }
        } else {
            const errorText = await response.text();
            console.error("❌ 请求失败:", response.status, errorText);
            return null;
        }
    } catch (error) {
        console.error("❌ 网络错误:", error);
        return null;
    }
}

// 运行测试
testFrontendBackendCommunication().then(result => {
    if (result) {
        console.log("🎉 前端通信测试成功!");
    } else {
        console.log("❌ 前端通信测试失败!");
    }
});
"""
        
        # 保存测试脚本
        with open("frontend_test_script.js", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print("✅ 前端测试脚本已生成: frontend_test_script.js")
        print("💡 使用方法:")
        print("   1. 在浏览器中打开前端页面")
        print("   2. 按F12打开开发者工具")
        print("   3. 切换到Console标签")
        print("   4. 复制并粘贴脚本内容")
        print("   5. 按Enter运行测试")
    
    def provide_debugging_instructions(self):
        """提供调试说明"""
        print("\n" + "=" * 80)
        print("🔧 前端调试说明")
        print("=" * 80)
        
        print("\n📱 浏览器调试步骤:")
        print("1. 打开前端页面: http://localhost:3000")
        print("2. 按F12打开开发者工具")
        print("3. 切换到Network标签")
        print("4. 在前端发送一条消息")
        print("5. 观察Network标签中的请求")
        
        print("\n🔍 需要检查的内容:")
        print("- 是否有发送到 /ask_professor 的POST请求")
        print("- 请求的状态码（应该是200）")
        print("- 请求的响应内容")
        print("- 是否有CORS错误")
        print("- Console标签中是否有JavaScript错误")
        
        print("\n📋 常见问题和解决方案:")
        print("1. CORS错误:")
        print("   - 检查后端CORS配置")
        print("   - 确保允许前端域名访问")
        
        print("2. 网络连接失败:")
        print("   - 检查后端服务器是否运行")
        print("   - 检查端口8000是否可访问")
        
        print("3. 前端显示问题:")
        print("   - 检查Console中的JavaScript错误")
        print("   - 检查消息更新逻辑")
        print("   - 检查React组件状态管理")
    
    def run_full_diagnosis(self):
        """运行完整诊断"""
        self.print_banner()
        
        # 1. 测试后端状态
        backend_ok = self.test_backend_status()
        
        # 2. 测试前端状态
        frontend_ok = self.test_frontend_status()
        
        # 3. 测试CORS配置
        cors_ok = self.test_cors_configuration()
        
        # 4. 直接测试API端点
        api_ok, api_result = self.test_api_endpoint_directly()
        
        # 5. 测试JSON响应格式
        json_ok = self.test_json_response_format(api_result) if api_result else False
        
        # 6. 生成前端测试脚本
        self.generate_frontend_test_script()
        
        # 7. 提供调试说明
        self.provide_debugging_instructions()
        
        # 生成诊断报告
        self.generate_diagnosis_report(backend_ok, frontend_ok, cors_ok, api_ok, json_ok)
        
        return all([backend_ok, frontend_ok, cors_ok, api_ok, json_ok])
    
    def generate_diagnosis_report(self, backend_ok, frontend_ok, cors_ok, api_ok, json_ok):
        """生成诊断报告"""
        print("\n" + "=" * 80)
        print("📊 前后端通信诊断报告")
        print("=" * 80)
        
        tests = {
            "后端服务状态": backend_ok,
            "前端服务状态": frontend_ok,
            "CORS跨域配置": cors_ok,
            "API端点测试": api_ok,
            "JSON响应格式": json_ok
        }
        
        print("🔍 测试结果:")
        for test_name, result in tests.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"   {test_name}: {status}")
        
        passed_tests = sum(tests.values())
        total_tests = len(tests)
        
        print(f"\n📈 总体结果: {passed_tests}/{total_tests} 项测试通过")
        
        if passed_tests == total_tests:
            print("🎉 所有测试通过！前后端通信应该正常工作")
            print("💡 如果前端仍然无法显示回复，请检查:")
            print("   - 浏览器控制台是否有JavaScript错误")
            print("   - React组件的状态更新逻辑")
            print("   - 消息列表的渲染逻辑")
        else:
            print("⚠️  存在问题，需要修复:")
            if not backend_ok:
                print("   - 后端服务器无法访问")
            if not frontend_ok:
                print("   - 前端服务器无法访问")
            if not cors_ok:
                print("   - CORS配置有问题")
            if not api_ok:
                print("   - API端点调用失败")
            if not json_ok:
                print("   - JSON响应格式有问题")

def main():
    """主函数"""
    tester = FrontendBackendTester()
    success = tester.run_full_diagnosis()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
