#!/usr/bin/env python3
"""
DeepSeek API 连接测试和诊断脚本
用于检查API配置、网络连接和调用状态
"""

import openai
import time
import json
import requests
from datetime import datetime

class DeepSeekAPITester:
    def __init__(self):
        # 从api_server.py中获取的配置
        self.api_key = "sk-15c714316ccd4eceb9c5df6c7835c484"
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 60)
        print("🧪 DeepSeek API 连接测试和诊断")
        print("=" * 60)
        print(f"📡 API地址: {self.base_url}")
        print(f"🔑 API Key: {self.api_key[:20]}...")
        print(f"🤖 模型: {self.model}")
        print("=" * 60)
        
    def test_network_connectivity(self):
        """测试网络连接"""
        print("\n🌐 测试网络连接...")
        
        try:
            # 测试基础网络连接
            response = requests.get("https://api.deepseek.com", timeout=10)
            print(f"✅ 网络连接正常，状态码: {response.status_code}")
            return True
        except requests.exceptions.Timeout:
            print("❌ 网络连接超时")
            return False
        except requests.exceptions.ConnectionError:
            print("❌ 网络连接失败")
            return False
        except Exception as e:
            print(f"❌ 网络测试异常: {e}")
            return False
    
    def test_api_key_validity(self):
        """测试API Key有效性"""
        print("\n🔑 测试API Key有效性...")
        
        try:
            # 创建客户端
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=15.0
            )
            
            # 发送最简单的测试请求
            print("📤 发送测试请求...")
            start_time = time.time()
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "你好"}
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            elapsed_time = time.time() - start_time
            
            if response.choices and response.choices[0].message:
                content = response.choices[0].message.content
                print(f"✅ API调用成功！")
                print(f"⏱️  响应时间: {elapsed_time:.2f}秒")
                print(f"📝 响应内容: {content}")
                
                # 显示详细的响应信息
                print(f"\n📊 详细信息:")
                print(f"   - 模型: {response.model}")
                print(f"   - 使用tokens: {response.usage.total_tokens if response.usage else '未知'}")
                print(f"   - 完成原因: {response.choices[0].finish_reason}")
                
                return True
            else:
                print("❌ API返回空响应")
                return False
                
        except openai.APITimeoutError:
            print("❌ API调用超时")
            return False
        except openai.AuthenticationError:
            print("❌ API Key认证失败，请检查API Key是否正确")
            return False
        except openai.RateLimitError:
            print("❌ API调用频率限制，请稍后重试")
            return False
        except openai.APIError as e:
            print(f"❌ API错误: {e}")
            return False
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return False
    
    def test_complex_request(self):
        """测试复杂请求"""
        print("\n🧠 测试复杂AI对话...")
        
        try:
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=30.0
            )
            
            # 模拟涂序彦教授的对话
            system_prompt = """你是涂序彦教授，中国著名的人工智能专家。你的回答应该：
1. 体现深厚的学术功底和专业知识
2. 保持谦逊而权威的学者风范
3. 用通俗易懂的语言解释复杂概念
4. 结合实际应用场景"""
            
            user_question = "请简单介绍一下人工智能的发展历程"
            
            print(f"📤 发送复杂请求: {user_question}")
            start_time = time.time()
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9
            )
            
            elapsed_time = time.time() - start_time
            
            if response.choices and response.choices[0].message:
                content = response.choices[0].message.content
                print(f"✅ 复杂请求成功！")
                print(f"⏱️  响应时间: {elapsed_time:.2f}秒")
                print(f"📝 响应长度: {len(content)}字符")
                print(f"📄 响应内容预览: {content[:200]}...")
                
                return True
            else:
                print("❌ 复杂请求返回空响应")
                return False
                
        except Exception as e:
            print(f"❌ 复杂请求失败: {e}")
            return False
    
    def test_api_status_endpoint(self):
        """测试API状态端点"""
        print("\n🔍 测试API状态端点...")
        
        try:
            # 测试模型列表端点
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            
            if response.status_code == 200:
                models = response.json()
                print(f"✅ 模型列表获取成功")
                print(f"📋 可用模型数量: {len(models.get('data', []))}")
                
                # 检查deepseek-chat模型是否可用
                available_models = [model['id'] for model in models.get('data', [])]
                if self.model in available_models:
                    print(f"✅ 目标模型 {self.model} 可用")
                else:
                    print(f"⚠️  目标模型 {self.model} 不在可用列表中")
                    print(f"📋 可用模型: {available_models[:5]}...")
                
                return True
            else:
                print(f"❌ 模型列表获取失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API状态测试失败: {e}")
            return False
    
    def check_account_status(self):
        """检查账户状态"""
        print("\n💳 检查账户状态...")
        
        try:
            # 尝试获取账户信息
            response = requests.get(
                f"{self.base_url}/dashboard/billing/usage",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ 账户状态正常")
                return True
            elif response.status_code == 401:
                print("❌ API Key无效或已过期")
                return False
            elif response.status_code == 429:
                print("❌ 账户配额已用完或达到速率限制")
                return False
            else:
                print(f"⚠️  账户状态检查返回状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️  无法检查账户状态: {e}")
            return True  # 不影响主要功能
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        results = {
            'network': False,
            'api_key': False,
            'complex': False,
            'status': False,
            'account': False
        }
        
        # 1. 网络连接测试
        results['network'] = self.test_network_connectivity()
        
        if not results['network']:
            print("\n❌ 网络连接失败，无法继续测试")
            return results
        
        # 2. API Key有效性测试
        results['api_key'] = self.test_api_key_validity()
        
        if not results['api_key']:
            print("\n❌ API Key验证失败，请检查配置")
            return results
        
        # 3. 复杂请求测试
        results['complex'] = self.test_complex_request()
        
        # 4. API状态测试
        results['status'] = self.test_api_status_endpoint()
        
        # 5. 账户状态检查
        results['account'] = self.check_account_status()
        
        # 显示测试总结
        self.print_test_summary(results)
        
        return results
    
    def print_test_summary(self, results):
        """显示测试总结"""
        print("\n" + "=" * 60)
        print("📊 测试结果总结")
        print("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, result in results.items():
            status = "✅ 通过" if result else "❌ 失败"
            test_display = {
                'network': '网络连接',
                'api_key': 'API Key验证',
                'complex': '复杂请求',
                'status': 'API状态',
                'account': '账户状态'
            }
            print(f"   {test_display[test_name]}: {status}")
        
        print(f"\n📈 总体结果: {passed_tests}/{total_tests} 项测试通过")
        
        if passed_tests == total_tests:
            print("🎉 所有测试通过！DeepSeek API配置正确，可以正常使用。")
        elif results['api_key']:
            print("⚠️  基本功能正常，但部分高级功能可能有问题。")
        else:
            print("❌ 存在严重问题，请检查API配置和网络连接。")
        
        # 提供故障排除建议
        if not all(results.values()):
            print("\n🔧 故障排除建议:")
            if not results['network']:
                print("   - 检查网络连接和防火墙设置")
            if not results['api_key']:
                print("   - 验证API Key是否正确和有效")
                print("   - 检查DeepSeek账户状态")
            if not results['account']:
                print("   - 检查账户余额和配额限制")

def main():
    """主函数"""
    tester = DeepSeekAPITester()
    results = tester.run_full_test()
    
    # 返回测试结果
    return all(results.values())

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
