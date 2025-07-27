# complete_api_server.py - 完整的API服务器（聊天+语音功能）
# 合并聊天功能和语音功能

import uvicorn
import asyncio
import time
import base64
import io
import tempfile
import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openai

# 百度语音API - 使用标准HTTP API
import requests
import json
import base64

# ==============================================================================
# 1. 百度语音API类（修复版本）
# ==============================================================================

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

    def synthesis(self, text: str, voice_person: int = 1, speed: int = 5, pitch: int = 5, volume: int = 5) -> bytes:
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

# ==============================================================================
# 2. 配置与初始化
# ==============================================================================

# 创建FastAPI应用
app = FastAPI(
    title="涂序彦教授数字人完整API服务器",
    description="包含聊天功能和语音功能的完整API系统",
    version="8.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API配置
DEEPSEEK_API_KEY = "sk-15c714316ccd4eceb9c5df6c7835c484"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# 百度语音API配置
BAIDU_APP_ID = "119601523"
BAIDU_API_KEY = "oOynRSSJJx0HReZxWpghwfdh"
BAIDU_SECRET_KEY = "syqCl5ME2ZlkUJLUHRkJZQGCepH4QNa4"

# 初始化百度语音客户端（修复版本）
try:
    baidu_speech_api = BaiduSpeechAPI(BAIDU_API_KEY, BAIDU_SECRET_KEY)
    # 测试获取Access Token
    token = baidu_speech_api.get_access_token()
    if token:
        print("✅ 百度语音API初始化成功")
        BAIDU_SPEECH_AVAILABLE = True
    else:
        print("❌ 百度语音API初始化失败：无法获取Access Token")
        BAIDU_SPEECH_AVAILABLE = False
except Exception as e:
    print(f"❌ 百度语音API初始化失败: {e}")
    baidu_speech_api = None
    BAIDU_SPEECH_AVAILABLE = False

# 初始化OpenAI客户端
openai_client = openai.OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    timeout=30.0
)

# ==============================================================================
# 2. 数据模型
# ==============================================================================

class UserQuery(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class BotResponse(BaseModel):
    answer: str
    source: str  # "deepseek", "error", "timeout"
    thinking_time: Optional[float] = None

class ThinkingStatus(BaseModel):
    status: str
    elapsed_time: float

# 语音相关数据模型
class ASRRequest(BaseModel):
    audio_data: str  # base64编码的音频数据
    format: str = "wav"
    rate: int = 16000

class ASRResponse(BaseModel):
    text: str
    confidence: float = 0.0
    success: bool = True
    message: str = ""

class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-female"
    speed: int = 5
    pitch: int = 5
    volume: int = 5

# ==============================================================================
# 3. 工具函数
# ==============================================================================

def print_log(message: str):
    """打印带时间戳的日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

async def call_deepseek_api(message: str, timeout: float = 25.0) -> tuple[str, float]:
    """调用DeepSeek API"""
    start_time = time.time()
    
    try:
        print_log(f"🤖 调用DeepSeek API: {message[:50]}...")
        
        # 涂序彦教授的系统提示
        system_prompt = """你是涂序彦教授，中国著名的人工智能专家，北京理工大学教授。你的回答应该：

1. 体现深厚的学术功底和专业知识
2. 保持谦逊而权威的学者风范  
3. 用通俗易懂的语言解释复杂概念
4. 结合实际应用场景和案例
5. 展现对AI发展的深刻洞察
6. 保持温和、耐心的教学态度

请以涂序彦教授的身份和风格回答问题。"""

        response = openai_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=2000,
            temperature=0.7,
            top_p=0.9
        )
        
        elapsed_time = time.time() - start_time
        
        if response.choices and response.choices[0].message:
            answer = response.choices[0].message.content
            print_log(f"✅ DeepSeek API调用成功，耗时: {elapsed_time:.2f}秒")
            return answer, elapsed_time
        else:
            raise Exception("API返回空响应")
            
    except openai.APITimeoutError:
        elapsed_time = time.time() - start_time
        print_log(f"⏰ DeepSeek API超时，耗时: {elapsed_time:.2f}秒")
        raise Exception("API调用超时")
    except Exception as e:
        elapsed_time = time.time() - start_time
        print_log(f"❌ DeepSeek API调用失败: {e}，耗时: {elapsed_time:.2f}秒")
        raise e

# ==============================================================================
# 4. API端点
# ==============================================================================

@app.get("/")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "message": "涂序彦教授数字人完整API服务器 v8.0",
        "timestamp": datetime.now().isoformat(),
        "version": "8.0.0",
        "server_type": "complete_api_server",
        "features": ["chat", "speech", "asr", "tts"]
    }

@app.post("/ask_professor", response_model=BotResponse)
async def ask_professor_endpoint(query: UserQuery):
    """AI问答接口 - 兼容前端"""
    try:
        print_log(f"💬 收到问题: {query.message}")
        
        # 调用DeepSeek API
        answer, thinking_time = await call_deepseek_api(query.message)
        
        return BotResponse(
            answer=answer,
            source="deepseek",
            thinking_time=thinking_time
        )
        
    except Exception as e:
        print_log(f"❌ 处理问题失败: {e}")
        return BotResponse(
            answer=f"抱歉，我现在无法回答您的问题。错误信息：{str(e)}",
            source="error",
            thinking_time=0.0
        )

@app.post("/chat", response_model=BotResponse)
async def chat_endpoint(query: UserQuery):
    """聊天接口 - 兼容不同前端"""
    return await ask_professor_endpoint(query)

@app.post("/asr", response_model=ASRResponse)
async def speech_to_text(audio_file: UploadFile = File(...)):
    """语音识别端点"""
    if not BAIDU_SPEECH_AVAILABLE:
        print_log("🎤 [ASR] 使用模拟语音识别")
        return ASRResponse(
            text="这是模拟的语音识别结果：您好，我想了解人工智能的发展历程。",
            confidence=0.95,
            success=True,
            message="模拟识别成功（百度语音API不可用）"
        )

    try:
        print_log(f"🎤 [ASR] 收到音频文件: {audio_file.filename}, 大小: {audio_file.size} bytes")

        # 检查文件大小（10MB限制）
        if audio_file.size and audio_file.size > 10 * 1024 * 1024:
            return ASRResponse(
                text="",
                success=False,
                message="音频文件过大，请限制在10MB以内"
            )

        # 检查文件格式
        allowed_formats = ['.wav', '.mp3', '.pcm', '.webm', '.ogg']
        file_ext = os.path.splitext(audio_file.filename or "")[1].lower()
        if file_ext not in allowed_formats:
            return ASRResponse(
                text="",
                success=False,
                message=f"不支持的音频格式，请使用: {', '.join(allowed_formats)}"
            )

        # 读取音频文件
        audio_data = await audio_file.read()

        # 调用修复后的百度语音识别API
        start_time = time.time()

        format_map = {
            '.wav': 'wav',
            '.mp3': 'mp3',
            '.pcm': 'pcm',
            '.webm': 'wav',
            '.ogg': 'wav'
        }
        audio_format = format_map.get(file_ext, 'wav')

        result = baidu_speech_api.asr(audio_data, audio_format, 16000)

        elapsed_time = time.time() - start_time
        print_log(f"🎤 [ASR] 识别耗时: {elapsed_time:.2f}秒")

        if result.get('err_no') == 0:
            recognized_text = ''.join(result.get('result', []))
            confidence = result.get('confidence', 0) / 100.0

            print_log(f"✅ [ASR] 识别成功: {recognized_text}")
            return ASRResponse(
                text=recognized_text,
                confidence=confidence,
                success=True,
                message="识别成功"
            )
        else:
            error_msg = f"识别失败，错误码: {result.get('err_no')}, 错误信息: {result.get('err_msg', '未知错误')}"
            print_log(f"❌ [ASR] {error_msg}")
            return ASRResponse(
                text="",
                success=False,
                message=error_msg
            )

    except Exception as e:
        print_log(f"❌ [ASR] 处理异常: {e}")
        return ASRResponse(
            text="",
            success=False,
            message=f"语音识别失败: {str(e)}"
        )

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """文本转语音端点"""
    if not BAIDU_SPEECH_AVAILABLE:
        print_log("🔊 [TTS] 使用模拟语音合成")
        mock_audio = b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x80\x3e\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'
        mock_audio += b'\x00' * 2048

        return StreamingResponse(
            io.BytesIO(mock_audio),
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=mock_tts_audio.wav",
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache"
            }
        )

    try:
        print_log(f"🔊 [TTS] 合成请求: {request.text[:50]}...")

        if len(request.text) > 1024:
            raise HTTPException(
                status_code=400,
                detail="文本长度超过限制（1024字符）"
            )

        voice_person = 4115  # 度小贤臻品音色，高品质男声，适合教授风格
        professor_speed = max(0, min(15, request.speed + 1))  # 适中语速，+1平衡速度和清晰度
        professor_pitch = max(0, min(15, request.pitch + 1))
        professor_volume = max(0, min(15, request.volume))

        start_time = time.time()

        result = baidu_speech_api.synthesis(
            request.text,
            voice_person,
            professor_speed,
            professor_pitch,
            professor_volume
        )

        elapsed_time = time.time() - start_time
        print_log(f"🔊 [TTS] 合成耗时: {elapsed_time:.2f}秒")

        if not result or len(result) == 0:
            error_msg = "TTS合成失败，返回空音频数据"
            print_log(f"❌ [TTS] {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        print_log(f"✅ [TTS] 合成成功，音频大小: {len(result)} bytes")

        return StreamingResponse(
            io.BytesIO(result),
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=tts_audio.wav",
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print_log(f"❌ [TTS] 处理异常: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"文本转语音失败: {str(e)}"
        )

@app.get("/speech_status")
async def speech_status():
    """语音服务状态检查"""
    return {
        "baidu_speech_available": BAIDU_SPEECH_AVAILABLE,
        "asr_enabled": BAIDU_SPEECH_AVAILABLE,
        "tts_enabled": BAIDU_SPEECH_AVAILABLE,
        "app_id": BAIDU_APP_ID if BAIDU_SPEECH_AVAILABLE else "未配置",
        "message": "百度语音服务正常" if BAIDU_SPEECH_AVAILABLE else "百度语音服务不可用"
    }

@app.get("/api_status")
async def api_status():
    """API状态检查"""
    return {
        "deepseek_available": True,
        "speech_available": BAIDU_SPEECH_AVAILABLE,
        "chat_enabled": True,
        "asr_enabled": BAIDU_SPEECH_AVAILABLE,
        "tts_enabled": BAIDU_SPEECH_AVAILABLE,
        "server_version": "8.0.0",
        "features": ["chat", "speech", "asr", "tts"],
        "message": "完整API服务器正常运行"
    }

# ==============================================================================
# 5. 启动服务器
# ==============================================================================

if __name__ == "__main__":
    print("🚀 启动涂序彦教授数字人完整API服务器 v8.0")
    print("📡 包含聊天功能和语音功能")
    uvicorn.run(
        "complete_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
