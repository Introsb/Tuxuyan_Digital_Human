# 涂序彦教授数字人AI系统

一个基于React + FastAPI的智能对话系统，模拟涂序彦教授的学术风格和知识体系。

## 🎯 项目概述

本项目包含一个完整的AI数字人对话系统，具备以下特性：

- **🎤 语音交互**：支持语音录音、语音识别(ASR)和文本转语音(TTS)
- **🤖 智能对话**：集成AI模型，提供教授风格的专业回复
- **🎨 现代UI**：基于React 18 + Tailwind CSS，黑白双色调设计
- **📱 响应式**：完美适配桌面端和移动端设备
- **🚀 一键启动**：统一启动脚本，同时启动前后端服务
- **🛠️ 开发友好**：完整的测试脚本和调试工具

## 🏗️ 项目结构

```
├── README.md                    # 项目说明文档
├── api_server.py               # FastAPI后端服务器
├── react-version/              # React前端应用
│   ├── src/                    # 前端源代码
│   ├── public/                 # 静态资源
│   ├── package.json            # 前端依赖配置
│   └── README.md               # 前端详细说明
├── test_api.py                 # API测试脚本
├── test_server.py              # 服务器测试脚本
└── test_ui_fixes.md            # UI修复测试文档
```

## 🚀 快速启动

### 方法1: 统一启动（推荐）
```bash
# 一键启动前端和后端服务
python start_unified.py
```

### 方法2: 分别启动
```bash
# 启动后端 (终端1)
python debug_server.py

# 启动前端 (终端2)
cd react-version && npm start
```

### 🌐 访问地址
- **前端界面**: http://localhost:3000
- **后端API**: http://127.0.0.1:8000

## 📦 构建和部署

### 开发环境构建
```bash
# 构建React生产版本
cd react-version
npm run build

# 本地预览构建结果
npx serve -s build -l 3000
```

### 生产环境部署
```bash
# 运行自动化部署脚本
python3 deploy_production.py

# 手动部署
cd react-version
npm run build
# 将build文件夹部署到您的服务器
```

### Docker部署
```bash
# 使用Docker Compose一键部署
docker-compose up -d

# 分别构建镜像
docker build -f Dockerfile.frontend -t tuxuyan-frontend .
docker build -f Dockerfile.backend -t tuxuyan-backend .
```

### 云平台部署
- **前端**: Vercel, Netlify, GitHub Pages
- **后端**: Railway, Heroku, DigitalOcean
- **完整应用**: AWS, Google Cloud, Azure
- **API文档**: http://127.0.0.1:8000/docs

### 环境要求

- **Python**: 3.10+
- **Node.js**: 16+
- **npm**: 8+

### 后端启动

1. 安装Python依赖：
```bash
pip install fastapi uvicorn openai python-dotenv
```

2. 配置环境变量：
```bash
# 创建.env文件并添加您的API密钥
DEEPSEEK_API_KEY=your_api_key_here
```

3. 启动后端服务器：
```bash
python api_server.py
```

后端服务将运行在 `http://localhost:8000`

### 前端启动

1. 进入前端目录：
```bash
cd react-version
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm start
```

前端应用将运行在 `http://localhost:3000`

## ✨ 主要功能

### 🎨 前端特性
- **现代化UI设计**：简洁优雅的用户界面
- **思考状态显示**：AI处理时的实时状态反馈
- **打字机效果**：逐字显示AI回复，增强交互体验
- **Markdown支持**：完整的Markdown渲染和代码高亮
- **响应式布局**：适配各种屏幕尺寸

### 🔧 后端特性
- **高性能API**：基于FastAPI的异步处理
- **AI集成**：DeepSeek API集成，支持长文本生成
- **CORS支持**：跨域请求处理
- **错误处理**：完善的异常处理机制
- **日志记录**：详细的请求和响应日志

### 🤖 AI功能
- **角色扮演**：模拟涂序彦教授的学术风格
- **深度回答**：支持最多3200 tokens的详细回复
- **多角度分析**：从不同角度分析问题
- **实例说明**：提供具体案例和类比

## 🛠️ 开发指南

### 前端开发

前端使用React + Tailwind CSS开发，主要组件包括：

- `ChatArea`: 主聊天区域
- `MessageList`: 消息列表显示
- `InputArea`: 用户输入区域
- `Sidebar`: 侧边栏导航
- `Header`: 顶部导航栏

### 后端开发

后端使用FastAPI开发，主要端点：

- `POST /ask_professor`: 发送问题给AI教授
- `GET /health`: 健康检查端点

### 环境配置

创建`.env`文件配置环境变量：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

## 📦 部署

### 前端部署

```bash
cd react-version
npm run build
# 将build目录部署到静态文件服务器
```

### 后端部署

```bash
# 使用uvicorn部署
uvicorn api_server:app --host 0.0.0.0 --port 8000

# 或使用gunicorn
gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👨‍💼 关于涂序彦教授

涂序彦教授是中国人工智能领域的泰斗，在控制论、人工智能、知识工程等领域有着深厚的学术造诣。本项目旨在传承和发扬教授的学术思想和教育理念。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发起 Pull Request
- 邮件联系：[您的邮箱]

---

**注意**：本项目仅用于学术研究和教育目的，请勿用于商业用途。
