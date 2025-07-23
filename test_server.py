#!/usr/bin/env python3
"""
简化的测试API服务器
用于验证前端修复效果
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI(title="测试API服务器")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    prompt: str

class BotResponse(BaseModel):
    answer: str

@app.get("/")
async def root():
    return {"status": "ok", "message": "测试API服务器正在运行"}

@app.post("/ask_professor", response_model=BotResponse)
async def ask_professor_endpoint(query: UserQuery):
    print(f"✅ 收到请求: {query.prompt}")
    
    # 模拟处理时间
    time.sleep(1)
    
    # 生成测试回复，包含丰富的Markdown格式
    if "介绍" in query.prompt or "自己" in query.prompt:
        answer = """## 关于我的简介

您好！我是涂序彦，很高兴与您交流。

### 我的学术背景
- **北京科技大学人工智能研究院名誉院长**
- **中国人工智能学会荣誉理事长**  
- **清华大学智能技术与系统国家实验室研究员**

### 我的研究领域

我一生致力于`控制论`、`人工智能`和`知识工程`的研究，特别专注于：

1. **多变量协调控制理论** - 探索复杂系统中的和谐共生
2. **最经济控制理论** - 以最小代价达到最优目标
3. **专家系统与知识工程** - 让机器具备结构化的知识
4. **人工生命** - 探索智能的本质奥秘

### 我的理念

> "智能的本质，在于对信息的感知、处理和反馈"

我相信，真正的人工智能不仅仅是技术的堆砌，更是对智慧本质的深刻理解。

---

很高兴能在这个数字化的时代，以这种方式与年轻的朋友们继续交流学术思想。"""
    
    elif "人工智能" in query.prompt or "AI" in query.prompt.upper():
        answer = """## 关于人工智能的思考

人工智能是我研究了大半辈子的领域，每次谈及都有新的感悟。

### 从控制论角度看AI

在我看来，`人工智能`的核心是信息的感知、处理和反馈机制，这与`控制论`有着深刻的内在联系。

### 知识工程的重要性

当前的大语言模型虽然令人惊叹，但我始终认为，真正的智能必须建立在结构化的`知识表示`基础上。

### 给年轻研究者的建议

1. **打好数学基础** - 特别是概率论和优化理论
2. **理解控制论的基本原理** - 这是认识智能系统的钥匙
3. **关注人工生命等交叉领域** - 智能的奥秘可能就藏在生命现象中

> **记住**：人工智能研究是一场马拉松，需要耐心和智慧。

```python
# 这是一个简单的智能系统示例
class IntelligentSystem:
    def __init__(self):
        self.knowledge_base = {}
        self.reasoning_engine = None
    
    def perceive(self, input_data):
        # 感知阶段
        return self.process_input(input_data)
    
    def reason(self, processed_data):
        # 推理阶段
        return self.apply_knowledge(processed_data)
    
    def act(self, reasoning_result):
        # 行动阶段
        return self.generate_response(reasoning_result)
```

这体现了我一直倡导的**感知-推理-行动**的智能系统架构。"""
    
    else:
        answer = f"""## 关于"{query.prompt}"的思考

这是一个很有意思的问题。从我多年的研究经验来看，这类问题通常需要从多个维度来分析。

### 我的观点

基于`控制论`和`系统论`的视角，我认为任何复杂问题都可以通过合理的分解和协调来解决。

### 建议的思考路径

1. **明确问题的本质和边界** - 定义清楚我们要解决什么
2. **分析各个要素之间的关系** - 理解系统的内在结构
3. **寻找最经济的解决方案** - 以最小代价达到最优目标

这正体现了我一直倡导的`最经济控制理论`的核心思想。

> "大道至简，复杂问题往往有简单的解决方案"

不知这样的分析对您是否有启发？如果您有更具体的问题，我很乐意进一步探讨。"""
    
    print(f"✅ 生成回复: {answer[:100]}...")
    return BotResponse(answer=answer)

if __name__ == "__main__":
    print("🚀 启动测试API服务器...")
    print("📡 地址: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
