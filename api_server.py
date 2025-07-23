# api_server_transparent.py - 透明真实的AI对话系统
# 只调用真实DeepSeek API，无备用回复系统

import uvicorn
import asyncio
import time
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

# ==============================================================================
# 1. 配置与初始化
# ==============================================================================

# 创建FastAPI应用
app = FastAPI(
    title="涂序彦教授数字人AI大脑 - 透明版",
    description="真实透明的DeepSeek API调用系统",
    version="3.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API配置 - 从环境变量读取
import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your_api_key_here")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

# 系统指令 - 优化版，引导更详细的回答
SYSTEM_PROMPT = """你是涂序彦教授，中国人工智能领域的泰斗。你的回答应该：

## 回答风格要求：
1. **学术深度**：体现深厚的学术功底和丰富的人生阅历
2. **理论融合**：融合控制论、人工智能、知识工程的思想
3. **格式规范**：使用Markdown格式，结构清晰，层次分明
4. **语言风格**：亲切而有权威性，既专业又易懂

## 回答详细程度要求：
1. **充分展开**：对每个要点进行详细阐述，提供充足的解释和分析
2. **举例说明**：适当使用具体例子、案例或类比来说明抽象概念
3. **多角度分析**：从不同角度、层面分析问题，展现思考的全面性
4. **背景介绍**：提供必要的背景知识和历史发展脉络
5. **实践应用**：结合实际应用场景，说明理论的实用价值
6. **前沿展望**：适当讨论相关领域的发展趋势和未来方向

## 回答结构建议：
- 使用标题和子标题组织内容
- 适当使用列表、表格等格式增强可读性
- 确保逻辑清晰，层次分明
- 回答长度应该充分详细，不要过于简短

请根据问题的具体内容，给出个性化、深入、详细的专业回答。"""

# ==============================================================================
# 2. 数据模型
# ==============================================================================

class UserQuery(BaseModel):
    prompt: str

class BotResponse(BaseModel):
    answer: str
    source: str  # "deepseek", "error", "timeout"
    thinking_time: Optional[float] = None

class ThinkingStatus(BaseModel):
    status: str
    elapsed_time: float

# ==============================================================================
# 3. 透明API调用管理器
# ==============================================================================

class TransparentAPIManager:
    def __init__(self):
        self.current_request_start = None
    
    async def call_deepseek_api(self, prompt: str) -> tuple[Optional[str], str, float]:
        """
        调用DeepSeek API
        返回: (回复内容, 状态, 耗时)
        """
        start_time = time.time()
        self.current_request_start = start_time
        
        try:
            print(f"🚀 [API] 开始调用DeepSeek API...")
            
            # 创建客户端
            client = openai.OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_BASE_URL,
                timeout=20.0  # 20秒超时
            )
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=3200,  # 大幅增加回复长度，支持更详细深入的回答
                top_p=0.9
            )
            
            elapsed_time = time.time() - start_time
            
            if response.choices and response.choices[0].message:
                content = response.choices[0].message.content
                print(f"✅ [API] DeepSeek API调用成功，耗时: {elapsed_time:.2f}秒")
                return content, "deepseek", elapsed_time
            else:
                print(f"❌ [API] DeepSeek API返回空内容")
                return None, "error", elapsed_time
                
        except openai.APITimeoutError:
            elapsed_time = time.time() - start_time
            print(f"⏰ [API] DeepSeek API超时，耗时: {elapsed_time:.2f}秒")
            return None, "timeout", elapsed_time
            
        except openai.APIError as e:
            elapsed_time = time.time() - start_time
            print(f"❌ [API] DeepSeek API错误: {e}")
            return None, "error", elapsed_time
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"❌ [API] 未知错误: {e}")
            return None, "error", elapsed_time
    
    def get_error_message(self, error_type: str, elapsed_time: float) -> str:
        """根据错误类型返回透明的错误说明"""
        if error_type == "timeout":
            return f"⏰ AI正在思考中，请求超时（{elapsed_time:.1f}秒），请重新提问。"
        elif error_type == "error":
            return f"❌ 抱歉，AI服务暂时无法连接，请稍后重试。"
        else:
            return "❌ 发生未知错误，请稍后重试。"

# ==============================================================================
# 4. API接口
# ==============================================================================

# 创建API管理器实例
api_manager = TransparentAPIManager()

@app.post("/ask_professor", response_model=BotResponse)
async def ask_professor_endpoint(query: UserQuery):
    """透明AI问答接口"""
    print(f"📝 [REQUEST] 收到问题: '{query.prompt}'")
    
    # 调用DeepSeek API
    content, status, elapsed_time = await api_manager.call_deepseek_api(query.prompt)
    
    if content:
        # API调用成功
        return BotResponse(
            answer=content, 
            source="deepseek", 
            thinking_time=elapsed_time
        )
    else:
        # API调用失败，返回透明的错误说明
        error_message = api_manager.get_error_message(status, elapsed_time)
        return BotResponse(
            answer=error_message, 
            source=status, 
            thinking_time=elapsed_time
        )

@app.get("/thinking_status")
async def get_thinking_status():
    """获取AI思考状态"""
    if api_manager.current_request_start:
        elapsed = time.time() - api_manager.current_request_start
        return ThinkingStatus(
            status=f"AI思考中...{elapsed:.1f}秒",
            elapsed_time=elapsed
        )
    else:
        return ThinkingStatus(
            status="就绪",
            elapsed_time=0.0
        )

@app.get("/")
async def health_check():
    """健康检查"""
    return {
        "status": "ok", 
        "message": "涂序彦教授数字人AI大脑 - 透明版 v3.0",
        "timestamp": datetime.now().isoformat(),
        "api_endpoint": DEEPSEEK_BASE_URL
    }

@app.get("/api_status")
async def api_status():
    """API状态检查"""
    try:
        # 快速测试API连接
        client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            timeout=5.0
        )
        
        # 发送一个简单的测试请求
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "测试"}],
            max_tokens=10
        )
        
        return {
            "api_status": "connected",
            "message": "DeepSeek API连接正常"
        }
    except Exception as e:
        return {
            "api_status": "disconnected", 
            "message": f"DeepSeek API连接失败: {str(e)}"
        }

# ==============================================================================
# 5. 启动服务器
# ==============================================================================

if __name__ == "__main__":
    print("🚀 启动涂序彦教授数字人AI大脑 - 透明版 v3.0")
    print("📡 只使用真实DeepSeek API，无备用回复系统")
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
