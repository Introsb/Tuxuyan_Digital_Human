
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
