#!/usr/bin/env python3
"""
可靠的API服务器 - 涂序彦教授数字人
集成真实DeepSeek API，包含完善的错误处理和日志输出
"""

import uvicorn
import asyncio
import time
import sys
import json
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 创建FastAPI应用
app = FastAPI(
    title="涂序彦教授数字人API服务器",
    description="可靠的DeepSeek API集成服务器",
    version="6.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-15c714316ccd4eceb9c5df6c7835c484"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# 系统提示词
SYSTEM_PROMPT = """你是涂序彦教授，中国著名的人工智能专家、控制论专家。你的回答应该：

1. 体现深厚的学术功底和专业知识
2. 保持谦逊而权威的学者风范  
3. 用通俗易懂的语言解释复杂概念
4. 结合实际应用场景和发展趋势
5. 展现对人工智能、控制论、知识工程等领域的深入理解

请以涂序彦教授的身份，用专业而亲切的语调回答用户的问题。"""

# 数据模型
class UserQuery(BaseModel):
    prompt: str

class BotResponse(BaseModel):
    answer: str
    source: str
    thinking_time: Optional[float] = None
    tokens_used: Optional[int] = None

# 全局统计
class APIStats:
    def __init__(self):
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.total_tokens = 0

stats = APIStats()

def print_log(message: str, level: str = "INFO"):
    """统一的日志输出函数"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def print_separator():
    """打印分隔线"""
    print("=" * 80)

async def call_deepseek_api(prompt: str) -> tuple[Optional[str], str, float, int]:
    """
    调用DeepSeek API
    返回: (回复内容, 状态, 耗时, tokens使用量)
    """
    print_separator()
    print_log(f"🚀 新的API请求")
    print_log(f"📝 用户问题: {prompt}")
    print_log(f"📏 问题长度: {len(prompt)}字符")
    
    start_time = time.time()
    stats.total_calls += 1
    
    try:
        # 动态导入openai，避免启动时的依赖问题
        try:
            import openai
            print_log(f"✅ openai库导入成功，版本: {openai.__version__}")
        except ImportError as e:
            print_log(f"❌ 缺少openai库: {e}", "ERROR")
            print_log("💡 请在虚拟环境中安装: pip install openai", "ERROR")
            elapsed_time = time.time() - start_time
            stats.failed_calls += 1
            return None, "missing_dependency", elapsed_time, 0
        except Exception as e:
            print_log(f"❌ openai库导入异常: {e}", "ERROR")
            elapsed_time = time.time() - start_time
            stats.failed_calls += 1
            return None, "import_error", elapsed_time, 0
        
        print_log(f"🔗 开始调用DeepSeek API...")
        print_log(f"🔑 API Key: {DEEPSEEK_API_KEY[:20]}...")
        print_log(f"🌐 Base URL: {DEEPSEEK_BASE_URL}")
        
        # 创建客户端
        client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            timeout=45.0
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        print_log(f"📤 发送请求到DeepSeek...")
        
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
            
            print_log(f"✅ DeepSeek API调用成功!")
            print_log(f"⏱️  API响应时间: {elapsed_time:.2f}秒")
            print_log(f"🔢 使用tokens: {tokens_used}")
            print_log(f"📊 输入tokens: {response.usage.prompt_tokens if response.usage else 0}")
            print_log(f"📊 输出tokens: {response.usage.completion_tokens if response.usage else 0}")
            print_log(f"📝 回复长度: {len(content)}字符")
            print_log(f"📄 回复预览: {content[:150]}...")
            
            stats.successful_calls += 1
            stats.total_tokens += tokens_used
            print_separator()
            
            return content, "deepseek", elapsed_time, tokens_used
        else:
            print_log(f"❌ DeepSeek API返回空响应", "ERROR")
            elapsed_time = time.time() - start_time
            stats.failed_calls += 1
            print_separator()
            return None, "empty_response", elapsed_time, 0
            
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_type = type(e).__name__
        print_log(f"❌ DeepSeek API调用失败: {error_type}: {e}", "ERROR")
        stats.failed_calls += 1
        print_separator()
        return None, f"error_{error_type.lower()}", elapsed_time, 0

@app.get("/")
async def health_check():
    """健康检查"""
    return {
        "status": "ok", 
        "message": "涂序彦教授数字人API服务器 v6.0 - 可靠版本",
        "timestamp": datetime.now().isoformat(),
        "version": "6.0.0",
        "server_type": "reliable_api_server",
        "api_endpoint": DEEPSEEK_BASE_URL,
        "stats": {
            "total_calls": stats.total_calls,
            "successful_calls": stats.successful_calls,
            "failed_calls": stats.failed_calls,
            "total_tokens": stats.total_tokens,
            "success_rate": f"{(stats.successful_calls/max(stats.total_calls,1)*100):.1f}%"
        }
    }

@app.get("/api_status")
async def api_status():
    """API状态检查"""
    print_log("🔍 API状态检查请求")
    
    try:
        import openai
        
        client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            timeout=10.0
        )
        
        print_log("📤 发送测试请求到DeepSeek...")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "测试"}],
            max_tokens=10
        )
        
        print_log("✅ DeepSeek API连接正常")
        
        return {
            "api_status": "connected",
            "message": "DeepSeek API连接正常",
            "last_check": datetime.now().isoformat()
        }
    except ImportError:
        print_log("❌ 缺少openai库", "ERROR")
        return {
            "api_status": "missing_dependency", 
            "message": "缺少openai库，请安装: pip install openai",
            "last_check": datetime.now().isoformat()
        }
    except Exception as e:
        print_log(f"❌ DeepSeek API连接失败: {e}", "ERROR")
        
        return {
            "api_status": "disconnected", 
            "message": f"DeepSeek API连接失败: {str(e)}",
            "last_check": datetime.now().isoformat()
        }

@app.post("/ask_professor", response_model=BotResponse)
async def ask_professor_endpoint(query: UserQuery):
    """AI问答接口"""
    
    # 调用DeepSeek API
    content, status, elapsed_time, tokens_used = await call_deepseek_api(query.prompt)
    
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

# 简化的语音端点（保持兼容性）
@app.post("/asr")
async def speech_to_text():
    """模拟语音识别"""
    print_log("🎤 收到语音识别请求")
    
    await asyncio.sleep(0.5)
    
    mock_texts = [
        "你好，我想了解人工智能的发展历程",
        "请介绍一下控制论的基本概念", 
        "什么是知识工程",
        "人工生命有什么特点"
    ]
    
    import random
    mock_text = random.choice(mock_texts)
    
    return {
        "text": mock_text,
        "confidence": 0.95,
        "success": True,
        "message": "模拟识别成功"
    }

def main():
    """主函数"""
    print("🚀 启动涂序彦教授数字人API服务器 v6.0")
    print("📡 端口: 8000")
    print("🔧 类型: 可靠的DeepSeek API集成服务器")
    print("📝 日志: 详细的API调用日志输出")
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

if __name__ == "__main__":
    main()
