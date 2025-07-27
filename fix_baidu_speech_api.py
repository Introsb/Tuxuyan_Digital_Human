#!/usr/bin/env python3
"""
百度语音API修复脚本
根据官方文档重新实现ASR和TTS功能
"""

import requests
import json
import base64
import time
from typing import Optional

class BaiduSpeechAPI:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self) -> Optional[str]:
        """获取Access Token"""
        # 检查token是否过期
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
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
                self.access_token = data.get("access_token")
                expires_in = data.get("expires_in", 2592000)  # 默认30天
                self.token_expires_at = time.time() + expires_in - 300  # 提前5分钟刷新
                
                print(f"✅ 获取Access Token成功，有效期: {expires_in}秒")
                return self.access_token
            else:
                print(f"❌ 获取Access Token失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 获取Access Token异常: {e}")
            return None
    
    def asr_json_format(self, audio_data: bytes, audio_format: str = "wav", rate: int = 16000) -> dict:
        """
        使用JSON格式进行语音识别
        根据百度官方文档实现
        """
        token = self.get_access_token()
        if not token:
            return {"err_no": -1, "err_msg": "无法获取Access Token"}
        
        try:
            # 将音频数据进行base64编码
            speech_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            url = "https://vop.baidu.com/server_api"
            
            # 按照官方文档构建请求数据
            payload = {
                "format": audio_format,
                "rate": rate,
                "channel": 1,
                "cuid": "tuxuyan_digital_human",  # 用户唯一标识
                "token": token,
                "dev_pid": 1537,  # 普通话输入法模型
                "speech": speech_base64,
                "len": len(audio_data)  # 原始音频字节数
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
                print(f"响应内容: {response.text}")
                return {"err_no": response.status_code, "err_msg": f"HTTP错误: {response.status_code}"}
                
        except Exception as e:
            print(f"❌ ASR请求异常: {e}")
            return {"err_no": -1, "err_msg": f"请求异常: {str(e)}"}
    
    def asr_raw_format(self, audio_data: bytes, audio_format: str = "pcm", rate: int = 16000) -> dict:
        """
        使用RAW格式进行语音识别
        根据百度官方文档实现
        """
        token = self.get_access_token()
        if not token:
            return {"err_no": -1, "err_msg": "无法获取Access Token"}
        
        try:
            # 构建URL参数
            url = "https://vop.baidu.com/server_api"
            params = {
                "dev_pid": 1537,
                "cuid": "tuxuyan_digital_human",
                "token": token
            }
            
            # 设置Content-Type头
            headers = {
                'Content-Type': f'audio/{audio_format};rate={rate}'
            }
            
            print(f"🎤 发送RAW格式ASR请求，音频大小: {len(audio_data)} bytes")
            
            response = requests.post(
                url,
                params=params,
                headers=headers,
                data=audio_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ RAW ASR请求成功，错误码: {result.get('err_no', 'unknown')}")
                return result
            else:
                print(f"❌ RAW ASR请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return {"err_no": response.status_code, "err_msg": f"HTTP错误: {response.status_code}"}
                
        except Exception as e:
            print(f"❌ RAW ASR请求异常: {e}")
            return {"err_no": -1, "err_msg": f"请求异常: {str(e)}"}
    
    def tts(self, text: str, voice_person: int = 1, speed: int = 5, pitch: int = 5, volume: int = 5) -> bytes:
        """
        文本转语音
        """
        token = self.get_access_token()
        if not token:
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
            
            print(f"🔊 发送TTS请求: {text[:50]}...")
            
            response = requests.post(url, data=params, timeout=30)
            
            if response.status_code == 200:
                # 检查返回的是音频数据还是错误JSON
                content_type = response.headers.get('content-type', '')
                if 'audio' in content_type:
                    print(f"✅ TTS请求成功，音频大小: {len(response.content)} bytes")
                    return response.content
                else:
                    # 可能是错误信息
                    try:
                        error_data = response.json()
                        print(f"❌ TTS返回错误: {error_data}")
                        return b""
                    except:
                        print(f"✅ TTS请求成功，音频大小: {len(response.content)} bytes")
                        return response.content
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
    
    # 初始化API
    api_key = "oOynRSSJJx0HReZxWpghwfdh"
    secret_key = "syqCl5ME2ZlkUJLUHRkJZQGCepH4QNa4"
    
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
        print(f"✅ TTS测试成功，音频大小: {len(audio_data)} bytes")
        
        # 保存测试音频
        with open("test_tts_output.wav", "wb") as f:
            f.write(audio_data)
        print("💾 测试音频已保存到: test_tts_output.wav")
        
        # 测试ASR（使用刚生成的音频）
        print("\n🎤 测试ASR（语音识别）...")
        
        # 测试JSON格式
        print("📤 测试JSON格式ASR...")
        asr_result = speech_api.asr_json_format(audio_data, "wav", 16000)
        
        if asr_result.get('err_no') == 0:
            recognized_text = ''.join(asr_result.get('result', []))
            print(f"✅ JSON格式ASR成功: {recognized_text}")
        else:
            print(f"❌ JSON格式ASR失败: {asr_result.get('err_msg', '未知错误')}")
        
        # 测试RAW格式
        print("📤 测试RAW格式ASR...")
        asr_result_raw = speech_api.asr_raw_format(audio_data, "wav", 16000)
        
        if asr_result_raw.get('err_no') == 0:
            recognized_text_raw = ''.join(asr_result_raw.get('result', []))
            print(f"✅ RAW格式ASR成功: {recognized_text_raw}")
        else:
            print(f"❌ RAW格式ASR失败: {asr_result_raw.get('err_msg', '未知错误')}")
        
        return True
    else:
        print("❌ TTS测试失败")
        return False

def create_fixed_api_server():
    """创建修复后的API服务器代码"""
    print("\n📄 创建修复后的API服务器代码...")
    
    fixed_asr_code = '''
# 修复后的ASR端点实现
# 使用标准的百度语音API

import requests
import json
import base64

class BaiduSpeechAPI:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self) -> Optional[str]:
        """获取Access Token"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
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
                self.access_token = data.get("access_token")
                expires_in = data.get("expires_in", 2592000)
                self.token_expires_at = time.time() + expires_in - 300
                return self.access_token
            else:
                return None
                
        except Exception as e:
            print(f"❌ 获取Access Token异常: {e}")
            return None
    
    def asr(self, audio_data: bytes, audio_format: str = "wav", rate: int = 16000) -> dict:
        """语音识别 - JSON格式"""
        token = self.get_access_token()
        if not token:
            return {"err_no": -1, "err_msg": "无法获取Access Token"}
        
        try:
            speech_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            url = "https://vop.baidu.com/server_api"
            
            payload = {
                "format": audio_format,
                "rate": rate,
                "channel": 1,
                "cuid": "tuxuyan_digital_human",
                "token": token,
                "dev_pid": 1537,
                "speech": speech_base64,
                "len": len(audio_data)
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.post(
                url, 
                headers=headers, 
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"err_no": response.status_code, "err_msg": f"HTTP错误: {response.status_code}"}
                
        except Exception as e:
            return {"err_no": -1, "err_msg": f"请求异常: {str(e)}"}
    
    def tts(self, text: str, voice_person: int = 1, speed: int = 5, pitch: int = 5, volume: int = 5) -> bytes:
        """文本转语音"""
        token = self.get_access_token()
        if not token:
            return b""
        
        try:
            url = "https://tsn.baidu.com/text2audio"
            
            params = {
                "tex": text,
                "tok": token,
                "cuid": "tuxuyan_digital_human",
                "ctp": 1,
                "lan": "zh",
                "spd": speed,
                "pit": pitch,
                "vol": volume,
                "per": voice_person,
                "aue": 6
            }
            
            response = requests.post(url, data=params, timeout=30)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'audio' in content_type:
                    return response.content
                else:
                    try:
                        error_data = response.json()
                        print(f"❌ TTS返回错误: {error_data}")
                        return b""
                    except:
                        return response.content
            else:
                return b""
                
        except Exception as e:
            print(f"❌ TTS请求异常: {e}")
            return b""

# 在API服务器中使用
baidu_speech_api = BaiduSpeechAPI(BAIDU_API_KEY, BAIDU_SECRET_KEY)

@app.post("/asr", response_model=ASRResponse)
async def speech_to_text(audio_file: UploadFile = File(...)):
    """语音识别端点 - 使用标准百度API"""
    try:
        audio_data = await audio_file.read()
        
        # 确定音频格式
        file_ext = os.path.splitext(audio_file.filename or "")[1].lower()
        format_map = {'.wav': 'wav', '.mp3': 'mp3', '.pcm': 'pcm', '.webm': 'wav', '.ogg': 'wav'}
        audio_format = format_map.get(file_ext, 'wav')
        
        # 调用修复后的ASR API
        result = baidu_speech_api.asr(audio_data, audio_format, 16000)
        
        if result.get('err_no') == 0:
            recognized_text = ''.join(result.get('result', []))
            return ASRResponse(
                text=recognized_text,
                confidence=1.0,
                success=True,
                message="识别成功"
            )
        else:
            return ASRResponse(
                text="",
                success=False,
                message=result.get('err_msg', '识别失败')
            )
            
    except Exception as e:
        return ASRResponse(
            text="",
            success=False,
            message=f"语音识别失败: {str(e)}"
        )

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """文本转语音端点 - 使用标准百度API"""
    try:
        # 调用修复后的TTS API
        audio_data = baidu_speech_api.tts(
            request.text,
            voice_person=1,  # 男声
            speed=request.speed,
            pitch=request.pitch,
            volume=request.volume
        )
        
        if audio_data:
            return StreamingResponse(
                io.BytesIO(audio_data),
                media_type="audio/wav",
                headers={
                    "Content-Disposition": "attachment; filename=tts_audio.wav",
                    "Access-Control-Allow-Origin": "*",
                    "Cache-Control": "no-cache"
                }
            )
        else:
            raise HTTPException(status_code=500, detail="TTS合成失败")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文本转语音失败: {str(e)}")
'''
    
    with open("fixed_baidu_speech_implementation.py", "w", encoding="utf-8") as f:
        f.write(fixed_asr_code)
    
    print("✅ 修复后的代码已保存到: fixed_baidu_speech_implementation.py")

def main():
    """主函数"""
    print("🔧 百度语音API修复工具")
    
    # 1. 测试API
    success = test_baidu_speech_api()
    
    # 2. 创建修复代码
    create_fixed_api_server()
    
    if success:
        print("\n🎉 百度语音API测试成功！")
        print("💡 接下来需要:")
        print("   1. 将修复后的代码集成到API服务器")
        print("   2. 重启服务器")
        print("   3. 测试前端语音功能")
    else:
        print("\n❌ 百度语音API测试失败")
        print("💡 请检查:")
        print("   1. API Key和Secret Key是否正确")
        print("   2. 网络连接是否正常")
        print("   3. 百度账户是否有余额")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
