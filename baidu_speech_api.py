#!/usr/bin/env python3
"""
百度云语音API实现
包含ASR（语音识别）和TTS（语音合成）功能
"""

import requests
import json
import base64
import time
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class BaiduSpeechAPI:
    """百度云语音API客户端"""
    
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = None
        self.token_expires_at = None
        self.token_cache_file = 'baidu_token_cache.json'
        
    def get_access_token(self) -> Optional[str]:
        """获取访问令牌，支持缓存"""
        # 检查缓存的令牌是否有效
        if self._load_cached_token():
            return self.access_token
            
        # 获取新令牌
        return self._fetch_new_token()
    
    def _load_cached_token(self) -> bool:
        """从缓存加载令牌"""
        try:
            if os.path.exists(self.token_cache_file):
                with open(self.token_cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                expires_at = datetime.fromisoformat(cache_data['expires_at'])
                if datetime.now() < expires_at - timedelta(minutes=5):  # 提前5分钟刷新
                    self.access_token = cache_data['access_token']
                    self.token_expires_at = expires_at
                    return True
        except Exception as e:
            print(f"⚠️ 加载缓存令牌失败: {e}")
        
        return False
    
    def _fetch_new_token(self) -> Optional[str]:
        """获取新的访问令牌"""
        try:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key
            }
            
            response = requests.post(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.access_token = data['access_token']
                    expires_in = data.get('expires_in', 2592000)  # 默认30天
                    self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                    
                    # 缓存令牌
                    self._cache_token()
                    
                    print(f"✅ 获取百度访问令牌成功")
                    return self.access_token
                else:
                    print(f"❌ 令牌响应格式错误: {data}")
            else:
                print(f"❌ 获取令牌失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except Exception as e:
            print(f"❌ 获取访问令牌异常: {e}")
        
        return None
    
    def _cache_token(self):
        """缓存令牌到文件"""
        try:
            cache_data = {
                'access_token': self.access_token,
                'expires_at': self.token_expires_at.isoformat()
            }
            with open(self.token_cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 缓存令牌失败: {e}")
    
    def asr(self, audio_data: bytes, audio_format: str = 'wav', rate: int = 16000) -> Dict[str, Any]:
        """
        语音识别（ASR）
        
        Args:
            audio_data: 音频数据
            audio_format: 音频格式 (wav, mp3, pcm)
            rate: 采样率
            
        Returns:
            识别结果字典
        """
        token = self.get_access_token()
        if not token:
            return {"err_no": -1, "err_msg": "无法获取访问令牌"}
        
        try:
            # Base64编码音频数据
            speech_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            url = "https://vop.baidu.com/server_api"
            
            payload = {
                "format": audio_format,
                "rate": rate,
                "channel": 1,
                "cuid": "tuxuyan_digital_human",
                "token": token,
                "dev_pid": 1537,  # 普通话模型
                "speech": speech_base64,
                "len": len(audio_data)
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            print(f"🎤 发送ASR请求，音频大小: {len(audio_data)} bytes")
            
            response = requests.post(
                url, 
                headers=headers, 
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ ASR请求成功，错误码: {result.get('err_no', 'unknown')}")
                return result
            else:
                print(f"❌ ASR请求失败，状态码: {response.status_code}")
                return {"err_no": response.status_code, "err_msg": f"HTTP错误: {response.status_code}"}
                
        except Exception as e:
            print(f"❌ ASR请求异常: {e}")
            return {"err_no": -1, "err_msg": f"请求异常: {str(e)}"}
    
    def tts(self, text: str, voice_person: int = 4115, speed: int = 5, pitch: int = 6, volume: int = 5) -> bytes:
        """
        文本转语音（TTS）

        Args:
            text: 要合成的文本
            voice_person: 发音人 (1-男声, 0-女声, 3-情感男声, 4-情感女声, 4115-度小贤臻品)
            speed: 语速 (0-15)
            pitch: 音调 (0-15)
            volume: 音量 (0-15)

        Returns:
            音频数据（bytes）
        """
        token = self.get_access_token()
        if not token:
            print("❌ 无法获取访问令牌")
            return b""
        
        try:
            url = "https://tsn.baidu.com/text2audio"
            
            params = {
                "tex": text,
                "tok": token,
                "cuid": "tuxuyan_digital_human",
                "ctp": 1,  # 客户端类型
                "lan": "zh",  # 语言
                "spd": speed,  # 语速
                "pit": pitch,  # 音调
                "vol": volume,  # 音量
                "per": voice_person,  # 发音人
                "aue": 6  # 音频编码，6为wav格式
            }
            
            print(f"🔊 发送TTS请求，文本长度: {len(text)} 字符")
            
            response = requests.post(url, data=params, timeout=30)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'audio' in content_type:
                    print(f"✅ TTS合成成功，音频大小: {len(response.content)} bytes")
                    return response.content
                else:
                    # 可能是错误响应
                    try:
                        error_data = response.json()
                        print(f"❌ TTS返回错误: {error_data}")
                    except:
                        print(f"❌ TTS返回非音频内容: {response.text[:200]}")
                    return b""
            else:
                print(f"❌ TTS请求失败，状态码: {response.status_code}")
                return b""
                
        except Exception as e:
            print(f"❌ TTS请求异常: {e}")
            return b""


def test_baidu_speech_api():
    """测试百度语音API"""
    print("=" * 80)
    print("🧪 百度语音API测试")
    print("=" * 80)
    
    # 从环境变量获取配置
    api_key = os.getenv('BAIDU_API_KEY', 'oOynRSSJJx0HReZxWpghwfdh')
    secret_key = os.getenv('BAIDU_SECRET_KEY', 'syqCl5ME2ZlkUJLUHRkJZQGCepH4QNa4')
    
    speech_api = BaiduSpeechAPI(api_key, secret_key)
    
    # 测试获取Access Token
    print("\n🔑 测试获取Access Token...")
    token = speech_api.get_access_token()
    if token:
        print(f"✅ Access Token获取成功: {token[:20]}...")
    else:
        print("❌ Access Token获取失败")
        return False
    
    # 测试TTS
    print("\n🔊 测试TTS（文本转语音）...")
    test_text = "您好，我是涂序彦教授，欢迎来到人工智能的世界。"
    audio_data = speech_api.tts(test_text)
    
    if audio_data:
        print(f"✅ TTS测试成功，生成音频大小: {len(audio_data)} bytes")
        
        # 保存测试音频文件
        with open('test_tts_output.wav', 'wb') as f:
            f.write(audio_data)
        print("💾 测试音频已保存为 test_tts_output.wav")
    else:
        print("❌ TTS测试失败")
    
    print("\n" + "=" * 80)
    print("🎉 百度语音API测试完成")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    test_baidu_speech_api()
