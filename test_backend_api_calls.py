#!/usr/bin/env python3
"""
后端API调用测试脚本
测试涂序彦教授数字人项目的后端API调用情况
"""

import requests
import time
import json
from datetime import datetime

class BackendAPITester:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 70)
        print("🧪 涂序彦教授数字人项目 - 后端API调用测试")
        print("=" * 70)
        print(f"📡 后端地址: {self.backend_url}")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
    
    def test_backend_health(self):
        """测试后端健康状态"""
        print("\n🔧 测试后端健康状态...")
        
        try:
            response = requests.get(f"{self.backend_url}/", timeout=5)
            if response.status_code == 200:
                result = response.json()
                print("✅ 后端服务器响应正常")
                print(f"📋 服务器信息: {result.get('message', '')}")
                print(f"🔢 版本: {result.get('version', '')}")
                print(f"🎯 服务器类型: {result.get('server_type', '')}")
                
                # 显示统计信息
                stats = result.get('stats', {})
                if stats:
                    print(f"📊 API统计:")
                    print(f"   - 总调用次数: {stats.get('total_calls', 0)}")
                    print(f"   - 成功次数: {stats.get('successful_calls', 0)}")
                    print(f"   - 失败次数: {stats.get('failed_calls', 0)}")
                    print(f"   - 总tokens: {stats.get('total_tokens', 0)}")
                
                return True
            else:
                print(f"❌ 后端服务器异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 后端健康检查失败: {e}")
            return False
    
    def test_api_status(self):
        """测试API状态端点"""
        print("\n🔍 测试API状态端点...")
        
        try:
            response = requests.get(f"{self.backend_url}/api_status", timeout=15)
            if response.status_code == 200:
                result = response.json()
                api_status = result.get('api_status', 'unknown')
                message = result.get('message', '')
                
                print(f"📊 API状态: {api_status}")
                print(f"📝 状态信息: {message}")
                
                if api_status == 'connected':
                    print("✅ DeepSeek API连接正常")
                    return True
                else:
                    print("❌ DeepSeek API连接异常")
                    return False
            else:
                print(f"❌ API状态检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API状态检查异常: {e}")
            return False
    
    def test_simple_conversation(self):
        """测试简单对话"""
        print("\n💬 测试简单对话...")
        
        test_data = {"prompt": "你好，请简单介绍一下自己"}
        
        try:
            print(f"📤 发送请求: {test_data['prompt']}")
            start_time = time.time()
            
            response = requests.post(
                f"{self.backend_url}/ask_professor",
                json=test_data,
                timeout=60
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '')
                source = result.get('source', 'unknown')
                thinking_time = result.get('thinking_time', 0)
                tokens_used = result.get('tokens_used', 0)
                
                print(f"✅ 请求成功")
                print(f"⏱️  总耗时: {elapsed_time:.2f}秒")
                print(f"🧠 AI思考时间: {thinking_time:.2f}秒")
                print(f"🔧 数据源: {source}")
                print(f"🔢 使用tokens: {tokens_used}")
                print(f"📝 回复长度: {len(answer)}字符")
                print(f"📄 回复预览: {answer[:200]}...")
                
                # 验证是否为真实API调用
                is_real_api = (
                    source == 'deepseek' and 
                    thinking_time > 2.0 and 
                    tokens_used > 0
                )
                
                if is_real_api:
                    print("✅ 确认：真实DeepSeek API调用")
                else:
                    print("⚠️  警告：可能不是真实API调用")
                
                return True, {
                    'elapsed_time': elapsed_time,
                    'thinking_time': thinking_time,
                    'source': source,
                    'tokens_used': tokens_used,
                    'is_real_api': is_real_api,
                    'answer_length': len(answer)
                }
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"📄 错误信息: {response.text}")
                return False, None
                
        except requests.exceptions.Timeout:
            print("⏰ 请求超时")
            return False, None
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False, None
    
    def test_complex_conversation(self):
        """测试复杂对话"""
        print("\n🧠 测试复杂对话...")
        
        test_data = {
            "prompt": "请详细介绍人工智能在控制论中的应用，以及未来的发展趋势"
        }
        
        try:
            print(f"📤 发送复杂请求: {test_data['prompt']}")
            start_time = time.time()
            
            response = requests.post(
                f"{self.backend_url}/ask_professor",
                json=test_data,
                timeout=90
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '')
                source = result.get('source', 'unknown')
                thinking_time = result.get('thinking_time', 0)
                tokens_used = result.get('tokens_used', 0)
                
                print(f"✅ 复杂请求成功")
                print(f"⏱️  总耗时: {elapsed_time:.2f}秒")
                print(f"🧠 AI思考时间: {thinking_time:.2f}秒")
                print(f"🔧 数据源: {source}")
                print(f"🔢 使用tokens: {tokens_used}")
                print(f"📝 回复长度: {len(answer)}字符")
                print(f"📄 回复预览: {answer[:300]}...")
                
                return True, {
                    'elapsed_time': elapsed_time,
                    'thinking_time': thinking_time,
                    'source': source,
                    'tokens_used': tokens_used,
                    'answer_length': len(answer)
                }
            else:
                print(f"❌ 复杂请求失败: {response.status_code}")
                return False, None
                
        except Exception as e:
            print(f"❌ 复杂请求异常: {e}")
            return False, None
    
    def test_multiple_requests(self):
        """测试多个连续请求"""
        print("\n📊 测试多个连续请求...")
        
        questions = [
            "什么是控制论？",
            "人工智能的核心技术有哪些？",
            "机器学习和深度学习的区别是什么？"
        ]
        
        results = []
        total_tokens = 0
        
        for i, question in enumerate(questions, 1):
            print(f"\n📤 请求 {i}/3: {question}")
            
            try:
                start_time = time.time()
                
                response = requests.post(
                    f"{self.backend_url}/ask_professor",
                    json={"prompt": question},
                    timeout=60
                )
                
                elapsed_time = time.time() - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    source = result.get('source', 'unknown')
                    thinking_time = result.get('thinking_time', 0)
                    tokens_used = result.get('tokens_used', 0)
                    
                    print(f"✅ 请求 {i} 成功 - 耗时: {elapsed_time:.2f}s, tokens: {tokens_used}")
                    
                    total_tokens += tokens_used
                    results.append({
                        'question': question,
                        'success': True,
                        'elapsed_time': elapsed_time,
                        'thinking_time': thinking_time,
                        'source': source,
                        'tokens_used': tokens_used
                    })
                else:
                    print(f"❌ 请求 {i} 失败: {response.status_code}")
                    results.append({
                        'question': question,
                        'success': False,
                        'error': response.status_code
                    })
                    
            except Exception as e:
                print(f"❌ 请求 {i} 异常: {e}")
                results.append({
                    'question': question,
                    'success': False,
                    'error': str(e)
                })
            
            # 间隔2秒避免频繁请求
            if i < len(questions):
                time.sleep(2)
        
        print(f"\n📈 多请求测试总结:")
        successful = sum(1 for r in results if r.get('success', False))
        print(f"   - 成功请求: {successful}/{len(questions)}")
        print(f"   - 总tokens消费: {total_tokens}")
        
        return results
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        # 1. 后端健康检查
        health_ok = self.test_backend_health()
        
        if not health_ok:
            print("\n❌ 后端服务器无法访问，请先启动后端服务器")
            return False
        
        # 2. API状态检查
        api_ok = self.test_api_status()
        
        # 3. 简单对话测试
        simple_ok, simple_result = self.test_simple_conversation()
        
        # 4. 复杂对话测试
        complex_ok, complex_result = self.test_complex_conversation()
        
        # 5. 多请求测试
        multiple_results = self.test_multiple_requests()
        
        # 生成测试报告
        self.generate_report(health_ok, api_ok, simple_ok, simple_result, 
                           complex_ok, complex_result, multiple_results)
        
        return health_ok and api_ok and simple_ok and complex_ok
    
    def generate_report(self, health_ok, api_ok, simple_ok, simple_result, 
                       complex_ok, complex_result, multiple_results):
        """生成测试报告"""
        print("\n" + "=" * 70)
        print("📊 后端API调用测试报告")
        print("=" * 70)
        
        # 基础测试结果
        print("🔧 基础功能测试:")
        print(f"   - 后端健康检查: {'✅ 通过' if health_ok else '❌ 失败'}")
        print(f"   - API状态检查: {'✅ 通过' if api_ok else '❌ 失败'}")
        
        # 对话测试结果
        print("\n💬 对话功能测试:")
        print(f"   - 简单对话: {'✅ 通过' if simple_ok else '❌ 失败'}")
        print(f"   - 复杂对话: {'✅ 通过' if complex_ok else '❌ 失败'}")
        
        # 详细统计
        if simple_result:
            print(f"\n📈 简单对话统计:")
            print(f"   - 响应时间: {simple_result['thinking_time']:.2f}秒")
            print(f"   - 使用tokens: {simple_result['tokens_used']}")
            print(f"   - 数据源: {simple_result['source']}")
            print(f"   - 真实API: {'是' if simple_result['is_real_api'] else '否'}")
        
        if complex_result:
            print(f"\n📈 复杂对话统计:")
            print(f"   - 响应时间: {complex_result['thinking_time']:.2f}秒")
            print(f"   - 使用tokens: {complex_result['tokens_used']}")
            print(f"   - 回复长度: {complex_result['answer_length']}字符")
        
        # 多请求统计
        successful_multiple = sum(1 for r in multiple_results if r.get('success', False))
        total_tokens_multiple = sum(r.get('tokens_used', 0) for r in multiple_results)
        
        print(f"\n📊 多请求测试统计:")
        print(f"   - 成功率: {successful_multiple}/{len(multiple_results)}")
        print(f"   - 总tokens: {total_tokens_multiple}")
        
        # 总体评估
        all_passed = health_ok and api_ok and simple_ok and complex_ok
        print(f"\n🎯 总体评估: {'✅ 全部通过' if all_passed else '❌ 存在问题'}")
        
        if all_passed:
            print("🎉 恭喜！后端API调用功能完全正常")
            print("💡 您的数字人项目可以正常使用DeepSeek API")
        else:
            print("⚠️  部分功能存在问题，请检查配置")

def main():
    """主函数"""
    tester = BackendAPITester()
    success = tester.run_full_test()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
