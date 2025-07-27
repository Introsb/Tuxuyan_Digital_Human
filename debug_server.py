#!/usr/bin/env python3
"""
调试服务器 - 用于诊断语音API问题
"""

import uvicorn
import io
import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

print("🔍 启动调试服务器...")

# 创建FastAPI应用
app = FastAPI(title="语音API调试服务器")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class ASRResponse(BaseModel):
    text: str
    confidence: float = 0.95
    success: bool = True
    message: str = ""

class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-male"
    speed: int = 5
    pitch: int = 5
    volume: int = 5

@app.get("/")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "调试服务器运行正常", "timestamp": time.time()}

@app.get("/speech_status")
async def speech_status():
    """语音服务状态"""
    return {
        "baidu_speech_available": False,
        "asr_enabled": True,
        "tts_enabled": True,
        "app_id": "调试模式",
        "message": "调试模式 - 使用模拟语音服务"
    }

@app.post("/asr", response_model=ASRResponse)
async def speech_to_text(audio_file: UploadFile = File(...)):
    """模拟语音识别"""
    print(f"🎤 [DEBUG ASR] 收到音频文件: {audio_file.filename}")
    print(f"🎤 [DEBUG ASR] 文件大小: {audio_file.size} bytes")
    print(f"🎤 [DEBUG ASR] 内容类型: {audio_file.content_type}")
    
    try:
        # 读取音频数据
        audio_data = await audio_file.read()
        print(f"🎤 [DEBUG ASR] 读取音频数据: {len(audio_data)} bytes")
        
        # 模拟处理时间
        time.sleep(0.5)
        
        # 返回模拟识别结果
        mock_texts = [
            "你好，我想了解人工智能的发展历程",
            "请介绍一下控制论的基本概念", 
            "什么是知识工程",
            "人工生命有什么特点",
            "请谈谈您对未来AI发展的看法"
        ]
        
        import random
        mock_text = random.choice(mock_texts)
        
        print(f"✅ [DEBUG ASR] 模拟识别结果: {mock_text}")
        
        return ASRResponse(
            text=mock_text,
            confidence=0.95,
            success=True,
            message="调试模式 - 模拟识别成功"
        )
        
    except Exception as e:
        print(f"❌ [DEBUG ASR] 处理异常: {e}")
        return ASRResponse(
            text="",
            success=False,
            message=f"调试模式 - 处理失败: {str(e)}"
        )

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """模拟文本转语音"""
    print(f"🔊 [DEBUG TTS] 合成请求: {request.text[:50]}...")
    print(f"🔊 [DEBUG TTS] 语音参数: speed={request.speed}, pitch={request.pitch}")
    
    try:
        # 模拟处理时间
        time.sleep(0.3)
        
        # 创建模拟WAV音频数据
        mock_audio = b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x80\x3e\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'
        mock_audio += b'\x00' * 2048  # 添加静音数据
        
        print(f"✅ [DEBUG TTS] 模拟合成成功，音频大小: {len(mock_audio)} bytes")
        
        return StreamingResponse(
            io.BytesIO(mock_audio),
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=debug_tts.wav",
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except Exception as e:
        print(f"❌ [DEBUG TTS] 处理异常: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"调试模式 - TTS失败: {str(e)}"
        )

@app.post("/ask_professor")
async def ask_professor(request: dict):
    """真实AI对话 - 调用DeepSeek API"""
    prompt = request.get("prompt", "")

    print("=" * 80)
    print(f"🚀 [REQUEST] 新的API请求 - {time.strftime('%H:%M:%S')}")
    print("=" * 80)
    print(f"📝 [INPUT] 用户问题: {prompt}")
    print(f"📏 [INPUT] 问题长度: {len(prompt)}字符")

    try:
        # 导入openai库
        try:
            import openai
            print(f"✅ [IMPORT] openai库导入成功，版本: {openai.__version__}")
        except ImportError as e:
            print(f"❌ [ERROR] 缺少openai库: {e}")
            print("💡 [HINT] 请安装: pip install openai")
            return {"answer": "服务器配置错误：缺少openai库", "source": "missing_dependency"}
        except Exception as e:
            print(f"❌ [ERROR] openai库导入异常: {e}")
            return {"answer": f"服务器配置错误：{str(e)}", "source": "import_error"}

        # DeepSeek API配置
        api_key = "sk-15c714316ccd4eceb9c5df6c7835c484"
        base_url = "https://api.deepseek.com/v1"

        print(f"\n🔗 [API] 开始调用DeepSeek API...")
        print(f"🔑 [API] API Key: {api_key[:20]}...")
        print(f"🌐 [API] Base URL: {base_url}")

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

        print(f"📤 [SENDING] 发送请求到DeepSeek...")
        start_time = time.time()

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

            print(f"\n✅ [SUCCESS] DeepSeek API调用成功!")
            print(f"⏱️  [TIME] API响应时间: {elapsed_time:.2f}秒")
            print(f"🔢 [TOKENS] 使用tokens: {tokens_used}")
            print(f"📊 [USAGE] 输入tokens: {response.usage.prompt_tokens if response.usage else 0}")
            print(f"📊 [USAGE] 输出tokens: {response.usage.completion_tokens if response.usage else 0}")
            print(f"📝 [OUTPUT] 回复长度: {len(content)}字符")
            print(f"📄 [PREVIEW] 回复预览: {content[:150]}...")
            print("=" * 80)

            return {
                "answer": content,
                "source": "deepseek",
                "thinking_time": elapsed_time,
                "tokens_used": tokens_used
            }
        else:
            print(f"❌ [ERROR] DeepSeek API返回空响应")
            print("=" * 80)
            return {"answer": "抱歉，AI服务暂时不可用。", "source": "error"}

    except ImportError:
        print(f"❌ [ERROR] 缺少openai库，请安装: pip install openai")
        print("=" * 80)
        return {"answer": "服务器配置错误：缺少必要的库", "source": "config_error"}

    except Exception as e:
        print(f"❌ [ERROR] DeepSeek API调用失败: {e}")
        print("=" * 80)
        return {"answer": f"抱歉，AI服务调用失败：{str(e)}", "source": "api_error"}

if __name__ == "__main__":
    print("🚀 启动调试服务器...")
    print("📡 端口: 8000")
    print("🔧 模式: 调试模式（模拟语音API）")
    
    uvicorn.run(
        "debug_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
