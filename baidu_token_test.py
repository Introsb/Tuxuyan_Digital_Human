#!/usr/bin/env python3
"""
百度语音API令牌获取和测试脚本
优化版本 - 包含错误处理、配置管理和令牌缓存
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta

class BaiduTokenManager:
    def __init__(self, api_key=None, secret_key=None):
        # 从环境变量或参数获取API凭据
        self.api_key = api_key or os.getenv('BAIDU_API_KEY', 'oOynRSSJJx0HReZxWpghwfdh')
        self.secret_key = secret_key or os.getenv('BAIDU_SECRET_KEY', 'syqCl5ME2ZlkUJLUHRkJZQGCepH4QNa4')
        self.token_cache_file = 'baidu_token_cache.json'
        
    def get_access_token(self, force_refresh=False):
        """
        获取访问令牌，支持缓存和自动刷新
        """
        # 检查缓存的令牌是否有效
        if not force_refresh:
            cached_token = self._load_cached_token()
            if cached_token:
                print("✅ 使用缓存的访问令牌")
                return cached_token
        
        print("🔄 获取新的访问令牌...")
        
        # 构建请求URL
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'client_id': self.api_key,
            'client_secret': self.secret_key,
            'grant_type': 'client_credentials'
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            # 发送请求
            response = requests.post(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            if 'access_token' in result:
                # 保存令牌到缓存
                self._save_token_cache(result)
                print("✅ 成功获取访问令牌")
                return result['access_token']
            else:
                print(f"❌ 获取令牌失败: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ 响应解析失败: {e}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def _load_cached_token(self):
        """加载缓存的令牌"""
        try:
            if os.path.exists(self.token_cache_file):
                with open(self.token_cache_file, 'r') as f:
                    cache = json.load(f)
                
                # 检查令牌是否过期（提前5分钟刷新）
                expire_time = datetime.fromisoformat(cache['expire_time'])
                if datetime.now() < expire_time - timedelta(minutes=5):
                    return cache['access_token']
                else:
                    print("⏰ 缓存的令牌即将过期，需要刷新")
                    
        except Exception as e:
            print(f"⚠️  读取令牌缓存失败: {e}")
            
        return None
    
    def _save_token_cache(self, token_data):
        """保存令牌到缓存"""
        try:
            # 计算过期时间（默认30天，提前5分钟刷新）
            expires_in = token_data.get('expires_in', 2592000)  # 默认30天
            expire_time = datetime.now() + timedelta(seconds=expires_in)
            
            cache = {
                'access_token': token_data['access_token'],
                'expire_time': expire_time.isoformat(),
                'created_time': datetime.now().isoformat()
            }
            
            with open(self.token_cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
                
            print(f"💾 令牌已缓存，过期时间: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"⚠️  保存令牌缓存失败: {e}")
    
    def test_token_validity(self, token):
        """测试令牌有效性"""
        print("🧪 测试令牌有效性...")
        
        # 使用语音识别API测试令牌
        test_url = "https://vop.baidu.com/server_api"
        
        # 创建一个最小的测试音频数据（静音）
        import base64
        test_audio = base64.b64encode(b'\x00' * 1024).decode('utf-8')
        
        test_data = {
            'format': 'wav',
            'rate': 16000,
            'channel': 1,
            'cuid': 'test_client',
            'token': token,
            'speech': test_audio,
            'len': len(test_audio)
        }
        
        try:
            response = requests.post(test_url, json=test_data, timeout=10)
            result = response.json()
            
            if result.get('err_no') == 0:
                print("✅ 令牌有效，可以正常调用语音API")
                return True
            elif result.get('err_no') == 3301:
                print("⚠️  令牌有效，但测试音频格式问题（这是正常的）")
                return True
            else:
                print(f"❌ 令牌测试失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 令牌测试异常: {e}")
            return False

def main():
    """主函数"""
    print("🎯 百度语音API令牌获取和测试")
    print("=" * 50)
    
    # 创建令牌管理器
    token_manager = BaiduTokenManager()
    
    # 显示配置信息
    print(f"📋 API配置:")
    print(f"   - API Key: {token_manager.api_key[:8]}...")
    print(f"   - Secret Key: {token_manager.secret_key[:8]}...")
    print()
    
    # 获取访问令牌
    access_token = token_manager.get_access_token()
    
    if access_token:
        print(f"🔑 访问令牌: {access_token[:20]}...")
        print()
        
        # 测试令牌有效性
        is_valid = token_manager.test_token_validity(access_token)
        
        if is_valid:
            print("\n🎉 百度语音API配置正确，可以正常使用！")
            
            # 显示使用建议
            print("\n💡 使用建议:")
            print("   1. 将此令牌用于语音识别和合成API调用")
            print("   2. 令牌会自动缓存，避免频繁请求")
            print("   3. 建议将API凭据设置为环境变量:")
            print("      export BAIDU_API_KEY='your_api_key'")
            print("      export BAIDU_SECRET_KEY='your_secret_key'")
            
        else:
            print("\n❌ 令牌无效或API配置有问题")
            
    else:
        print("\n❌ 无法获取访问令牌，请检查API凭据和网络连接")
        
        # 显示故障排除建议
        print("\n🔧 故障排除:")
        print("   1. 检查API Key和Secret Key是否正确")
        print("   2. 确认百度云账户状态正常")
        print("   3. 检查网络连接是否正常")
        print("   4. 确认语音技术服务已开通")

if __name__ == '__main__':
    main()
