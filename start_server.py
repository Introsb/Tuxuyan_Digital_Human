#!/usr/bin/env python3
"""
简化的语音API服务器启动脚本
如果主服务器无法启动，使用这个简化版本
"""

import uvicorn
import io
import time
import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

print("🚀 启动涂序彦教授数字人语音API服务器...")

# 创建FastAPI应用
app = FastAPI(title="涂序彦教授数字人语音API")

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

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
async def health_check():
    """健康检查"""
    return {
        "status": "ok", 
        "message": "涂序彦教授数字人语音API服务器运行正常", 
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.get("/speech_status")
async def speech_status():
    """语音服务状态"""
    return {
        "baidu_speech_available": False,
        "asr_enabled": True,
        "tts_enabled": True,
        "app_id": "模拟模式",
        "message": "使用模拟语音服务 - 适合开发和测试"
    }

@app.post("/asr", response_model=ASRResponse)
async def speech_to_text(audio_file: UploadFile = File(...)):
    """模拟语音识别"""
    print(f"🎤 [ASR] 收到音频文件: {audio_file.filename}")
    print(f"🎤 [ASR] 文件大小: {audio_file.size} bytes")
    
    try:
        # 读取音频数据
        audio_data = await audio_file.read()
        print(f"🎤 [ASR] 处理音频数据: {len(audio_data)} bytes")
        
        # 模拟处理时间
        time.sleep(0.5)
        
        # 返回模拟识别结果
        mock_texts = [
            "你好，我想了解人工智能的发展历程",
            "请介绍一下控制论的基本概念", 
            "什么是知识工程",
            "人工生命有什么特点",
            "请谈谈您对未来AI发展的看法",
            "机器学习和深度学习有什么区别",
            "人工智能在教育领域的应用前景如何"
        ]
        
        import random
        mock_text = random.choice(mock_texts)
        
        print(f"✅ [ASR] 模拟识别结果: {mock_text}")
        
        return ASRResponse(
            text=mock_text,
            confidence=0.95,
            success=True,
            message="模拟识别成功"
        )
        
    except Exception as e:
        print(f"❌ [ASR] 处理异常: {e}")
        return ASRResponse(
            text="",
            success=False,
            message=f"处理失败: {str(e)}"
        )

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """模拟文本转语音"""
    print(f"🔊 [TTS] 合成请求: {request.text[:50]}...")
    print(f"🔊 [TTS] 语音参数: speed={request.speed}, pitch={request.pitch}")
    
    try:
        # 模拟处理时间
        time.sleep(0.3)
        
        # 创建模拟WAV音频数据
        mock_audio = b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x80\x3e\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'
        mock_audio += b'\x00' * 2048  # 添加静音数据
        
        print(f"✅ [TTS] 模拟合成成功，音频大小: {len(mock_audio)} bytes")
        
        return StreamingResponse(
            io.BytesIO(mock_audio),
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=tts_output.wav",
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except Exception as e:
        print(f"❌ [TTS] 处理异常: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"TTS失败: {str(e)}"
        )

@app.post("/ask_professor")
async def ask_professor(request: ChatRequest):
    """模拟AI对话"""
    prompt = request.prompt
    print(f"🤖 [AI] 收到问题: {prompt}")
    
    # 模拟AI回复
    mock_answer = f"""## 感谢您的提问

您问到："{prompt}"

作为涂序彦教授，我很高兴为您解答这个问题。这是一个非常有意思的话题。

### 我的观点

人工智能是一个快速发展的领域，涉及多个学科的交叉融合。从控制论的角度来看，智能系统需要具备感知、决策和执行的能力。

在我多年的研究中，我发现人工智能的发展经历了几个重要阶段：

1. **符号主义时期**：注重逻辑推理和知识表示
2. **连接主义时期**：神经网络和机器学习的兴起
3. **深度学习时代**：大数据和计算能力的突破
4. **当前的大模型时代**：ChatGPT等的出现

### 建议

我建议您深入学习相关的基础理论，同时关注最新的技术发展动态。理论与实践相结合，才能真正掌握人工智能的精髓。

---
*这是模拟回复，实际部署时会连接真实的AI模型*"""
    
    print(f"✅ [AI] 生成回复: {mock_answer[:100]}...")
    
    return {"answer": mock_answer}

if __name__ == "__main__":
    print("🚀 启动服务器...")
    print("📡 端口: 8000")
    print("🔧 模式: 模拟模式（适合开发测试）")
    print("📝 API文档: http://127.0.0.1:8000/docs")
    
    uvicorn.run(
        "start_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
