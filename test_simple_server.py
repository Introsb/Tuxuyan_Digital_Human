#!/usr/bin/env python3
# 简单的测试服务器

from fastapi import FastAPI
import uvicorn
import openai

app = FastAPI(title="简单测试服务器")

# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-15c714316ccd4eceb9c5df6c7835c484"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

@app.get("/")
async def root():
    return {"message": "服务器运行正常"}

@app.get("/test_deepseek")
async def test_deepseek():
    try:
        client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            timeout=10.0
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "你好，请简单回复"}],
            max_tokens=50
        )
        
        return {
            "status": "success",
            "response": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    print("🚀 启动简单测试服务器...")
    uvicorn.run(
        "test_simple_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
