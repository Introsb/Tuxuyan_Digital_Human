#!/usr/bin/env python3
"""
简化的API服务器 - 涂序彦教授数字人
专注于稳定性和可靠性
"""

import uvicorn
import time
import sys
import io
import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# 暂时禁用音频转换工具
AUDIO_CONVERTER_AVAILABLE = False

# 创建FastAPI应用
app = FastAPI(title="涂序彦教授数字人API服务器", version="7.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class UserQuery(BaseModel):
    prompt: str

class BotResponse(BaseModel):
    answer: str
    source: str
    thinking_time: float = 0.0
    tokens_used: int = 0

# 百度云语音相关数据模型
class ASRResponse(BaseModel):
    text: str
    confidence: float = 0.0
    success: bool
    message: str

class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-male"
    speed: int = 5
    pitch: int = 5
    volume: int = 5

# 全局统计
stats = {"total_calls": 0, "successful_calls": 0, "failed_calls": 0, "total_tokens": 0}

def log_message(message: str):
    """简单的日志函数"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

# 初始化百度云语音API
try:
    from baidu_speech_api import BaiduSpeechAPI

    # 从环境变量获取配置
    BAIDU_API_KEY = os.getenv('BAIDU_API_KEY', 'oOynRSSJJx0HReZxWpghwfdh')
    BAIDU_SECRET_KEY = os.getenv('BAIDU_SECRET_KEY', 'syqCl5ME2ZlkUJLUHRkJZQGCepH4QNa4')

    baidu_speech_api = BaiduSpeechAPI(BAIDU_API_KEY, BAIDU_SECRET_KEY)

    # 测试获取Access Token
    token = baidu_speech_api.get_access_token()
    if token:
        log_message("✅ 百度云语音API初始化成功")
        BAIDU_SPEECH_AVAILABLE = True
    else:
        log_message("❌ 百度云语音API初始化失败：无法获取Access Token")
        BAIDU_SPEECH_AVAILABLE = False
        baidu_speech_api = None

except ImportError as e:
    log_message(f"⚠️ 百度云语音API模块导入失败: {e}")
    BAIDU_SPEECH_AVAILABLE = False
    baidu_speech_api = None
except Exception as e:
    log_message(f"❌ 百度云语音API初始化失败: {e}")
    BAIDU_SPEECH_AVAILABLE = False
    baidu_speech_api = None

def call_deepseek_api(prompt: str):
    """调用DeepSeek API"""
    print("=" * 80)
    log_message(f"🚀 新的API请求")
    log_message(f"📝 用户问题: {prompt}")
    
    start_time = time.time()
    stats["total_calls"] += 1
    
    try:
        # 检查openai库
        try:
            import openai
            log_message(f"✅ openai库导入成功，版本: {openai.__version__}")
        except ImportError as e:
            log_message(f"❌ 缺少openai库: {e}")
            elapsed_time = time.time() - start_time
            stats["failed_calls"] += 1
            return None, "missing_dependency", elapsed_time, 0
        
        # DeepSeek API配置
        api_key = "sk-15c714316ccd4eceb9c5df6c7835c484"
        base_url = "https://api.deepseek.com/v1"
        
        log_message(f"🔗 开始调用DeepSeek API...")
        log_message(f"🔑 API Key: {api_key[:20]}...")
        log_message(f"🌐 Base URL: {base_url}")
        
        # 创建客户端
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=45.0
        )
        
        # 系统提示词
        system_prompt = """你是涂序彦教授，中国著名的人工智能专家、控制论专家。你的回答应该：
1. 体现深厚的学术功底和专业知识
2. 保持谦逊而权威的学者风范  
3. 用通俗易懂的语言解释复杂概念
4. 结合实际应用场景和发展趋势
请以涂序彦教授的身份，用专业而亲切的语调回答用户的问题。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        log_message(f"📤 发送请求到DeepSeek...")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            top_p=0.9
        )
        
        elapsed_time = time.time() - start_time
        
        if response.choices and response.choices[0].message:
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            log_message(f"✅ DeepSeek API调用成功!")
            log_message(f"⏱️  API响应时间: {elapsed_time:.2f}秒")
            log_message(f"🔢 使用tokens: {tokens_used}")
            log_message(f"📝 回复长度: {len(content)}字符")
            log_message(f"📄 回复预览: {content[:150]}...")
            
            stats["successful_calls"] += 1
            stats["total_tokens"] += tokens_used
            print("=" * 80)
            
            return content, "deepseek", elapsed_time, tokens_used
        else:
            log_message(f"❌ DeepSeek API返回空响应")
            elapsed_time = time.time() - start_time
            stats["failed_calls"] += 1
            print("=" * 80)
            return None, "empty_response", elapsed_time, 0
            
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_type = type(e).__name__
        log_message(f"❌ DeepSeek API调用失败: {error_type}: {e}")
        stats["failed_calls"] += 1
        print("=" * 80)
        return None, f"error_{error_type.lower()}", elapsed_time, 0

@app.get("/")
async def health_check():
    """健康检查"""
    return {
        "status": "ok", 
        "message": "涂序彦教授数字人API服务器 v7.0 - 简化稳定版",
        "timestamp": datetime.now().isoformat(),
        "version": "7.0.0",
        "server_type": "simple_api_server",
        "stats": stats
    }

@app.get("/api_status")
async def api_status():
    """API状态检查"""
    log_message("🔍 API状态检查请求")
    
    try:
        import openai
        
        client = openai.OpenAI(
            api_key="sk-15c714316ccd4eceb9c5df6c7835c484",
            base_url="https://api.deepseek.com/v1",
            timeout=10.0
        )
        
        log_message("📤 发送测试请求到DeepSeek...")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "测试"}],
            max_tokens=10
        )
        
        log_message("✅ DeepSeek API连接正常")
        
        return {
            "api_status": "connected",
            "message": "DeepSeek API连接正常",
            "last_check": datetime.now().isoformat()
        }
    except ImportError:
        log_message("❌ 缺少openai库")
        return {
            "api_status": "missing_dependency", 
            "message": "缺少openai库，请安装: pip install openai",
            "last_check": datetime.now().isoformat()
        }
    except Exception as e:
        log_message(f"❌ DeepSeek API连接失败: {e}")
        
        return {
            "api_status": "disconnected", 
            "message": f"DeepSeek API连接失败: {str(e)}",
            "last_check": datetime.now().isoformat()
        }

@app.post("/ask_professor", response_model=BotResponse)
async def ask_professor_endpoint(query: UserQuery):
    """AI问答接口"""
    
    # 调用DeepSeek API
    content, status, elapsed_time, tokens_used = call_deepseek_api(query.prompt)
    
    if content and status == "deepseek":
        # API调用成功
        return BotResponse(
            answer=content, 
            source="deepseek", 
            thinking_time=elapsed_time,
            tokens_used=tokens_used
        )
    else:
        # API调用失败，返回错误信息
        error_message = f"""## API调用失败

很抱歉，DeepSeek API调用失败。

### 错误信息
- 状态: {status}
- 耗时: {elapsed_time:.2f}秒

### 可能的原因
- 网络连接问题
- API服务暂时不可用
- 认证或配额问题

请稍后重试。

---
*错误时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""

        return BotResponse(
            answer=error_message,
            source=status,
            thinking_time=elapsed_time,
            tokens_used=0
        )

@app.post("/asr", response_model=ASRResponse)
async def speech_to_text(audio_file: UploadFile = File(...)):
    """语音识别端点 - 使用百度云ASR"""
    if not BAIDU_SPEECH_AVAILABLE:
        return ASRResponse(
            text="",
            success=False,
            message="百度云语音服务不可用"
        )

    try:
        log_message(f"🎤 收到ASR请求，文件: {audio_file.filename}")

        # 读取音频数据
        audio_data = await audio_file.read()

        # 确定音频格式 - 简化处理
        file_ext = os.path.splitext(audio_file.filename or "")[1].lower()

        # 对于WebM格式，尝试作为WAV发送给百度云ASR
        if file_ext in ['.webm', '.ogg']:
            audio_format = 'wav'  # 百度云有时可以处理WebM数据
            log_message(f"🎤 WebM/OGG格式将作为WAV发送，大小: {len(audio_data)} bytes")
        elif file_ext == '.mp3':
            audio_format = 'mp3'
        elif file_ext == '.pcm':
            audio_format = 'pcm'
        else:
            audio_format = 'wav'

        log_message(f"🎤 音频格式: {audio_format}, 大小: {len(audio_data)} bytes")

        # 调用百度云ASR API
        start_time = time.time()
        result = baidu_speech_api.asr(audio_data, audio_format, 16000)
        elapsed_time = time.time() - start_time

        log_message(f"🎤 ASR识别耗时: {elapsed_time:.2f}秒")

        if result.get('err_no') == 0:
            recognized_text = ''.join(result.get('result', []))
            confidence = result.get('confidence', 0) / 100.0

            log_message(f"✅ ASR识别成功: {recognized_text}")
            return ASRResponse(
                text=recognized_text,
                confidence=confidence,
                success=True,
                message="识别成功"
            )
        else:
            error_msg = f"识别失败，错误码: {result.get('err_no')}, 错误信息: {result.get('err_msg', '未知错误')}"
            log_message(f"❌ ASR识别失败: {error_msg}")
            return ASRResponse(
                text="",
                success=False,
                message=error_msg
            )

    except Exception as e:
        log_message(f"❌ ASR处理异常: {e}")
        return ASRResponse(
            text="",
            success=False,
            message=f"语音识别失败: {str(e)}"
        )

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """文本转语音端点 - 使用百度云TTS"""
    if not BAIDU_SPEECH_AVAILABLE:
        raise HTTPException(status_code=503, detail="百度云语音服务不可用")

    try:
        log_message(f"🔊 收到TTS请求，文本长度: {len(request.text)} 字符")

        # 调用百度云TTS API
        start_time = time.time()
        audio_data = baidu_speech_api.tts(
            request.text,
            voice_person=1,  # 标准男声（适合教授形象）
            speed=request.speed,
            pitch=request.pitch,
            volume=request.volume
        )
        elapsed_time = time.time() - start_time

        log_message(f"🔊 TTS合成耗时: {elapsed_time:.2f}秒")

        if audio_data:
            log_message(f"✅ TTS合成成功，音频大小: {len(audio_data)} bytes")
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
            log_message("❌ TTS合成失败：返回空音频数据")
            raise HTTPException(status_code=500, detail="TTS合成失败")

    except Exception as e:
        log_message(f"❌ TTS处理异常: {e}")
        raise HTTPException(status_code=500, detail=f"文本转语音失败: {str(e)}")

if __name__ == "__main__":
    print("🚀 启动涂序彦教授数字人API服务器 v7.0")
    print("📡 端口: 8000")
    print("🔧 类型: 简化稳定版DeepSeek API集成服务器")
    print("=" * 60)
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        sys.exit(1)
