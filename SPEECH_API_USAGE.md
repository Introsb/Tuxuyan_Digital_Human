# 涂序彦数字人语音功能使用说明

## 🎯 功能概述

涂序彦数字人现已集成百度云语音服务，支持：
- **ASR（语音识别）**：将语音转换为文字
- **TTS（语音合成）**：将文字转换为语音
- **AI对话**：与涂序彦教授进行智能对话

## 🚀 快速开始

### 1. 启动服务

```bash
# 启动后端服务器
python3 simple_api_server.py

# 启动前端应用（另一个终端）
cd react-version
npx react-scripts start
```

### 2. 访问应用

- **前端界面**：http://localhost:3000
- **API文档**：http://localhost:8000/docs

## 📡 API端点

### 🎤 语音识别 (ASR)

**端点**：`POST /asr`

**请求格式**：multipart/form-data
```bash
curl -X POST http://127.0.0.1:8000/asr \
  -F "audio_file=@your_audio.wav"
```

**响应格式**：
```json
{
  "text": "识别出的文字内容",
  "confidence": 0.95,
  "success": true,
  "message": "识别成功"
}
```

**支持的音频格式**：
- WAV (推荐)
- MP3
- PCM
- WebM (转换为WAV)
- OGG (转换为WAV)

### 🔊 语音合成 (TTS)

**端点**：`POST /tts`

**请求格式**：application/json
```bash
curl -X POST http://127.0.0.1:8000/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，我是涂序彦教授",
    "speed": 5,
    "pitch": 5,
    "volume": 5
  }' \
  --output audio.wav
```

**请求参数**：
- `text` (必需)：要合成的文本
- `speed` (可选)：语速 (0-15，默认5)
- `pitch` (可选)：音调 (0-15，默认5)
- `volume` (可选)：音量 (0-15，默认5)

**响应**：音频文件流 (WAV格式)

### 💬 AI对话

**端点**：`POST /ask_professor`

**请求格式**：application/json
```bash
curl -X POST http://127.0.0.1:8000/ask_professor \
  -H "Content-Type: application/json" \
  -d '{"prompt": "请介绍一下人工智能的发展历程"}'
```

**响应格式**：
```json
{
  "answer": "涂序彦教授的回答内容...",
  "source": "deepseek",
  "thinking_time": 2.5,
  "tokens_used": 150
}
```

## 🎮 前端使用

### 语音输入
1. 点击麦克风图标开始录音
2. 说话后点击停止录音
3. 系统自动识别语音并填入输入框
4. 点击发送按钮发送消息

### 语音播放
1. 点击扬声器图标开启/关闭语音播放
2. 开启后，AI回复会自动转换为语音播放
3. 可以手动点击播放按钮重新播放

## 🔧 配置说明

### 环境变量

在 `.env` 文件中配置：

```env
# 百度云语音API配置
BAIDU_APP_ID=your_app_id
BAIDU_API_KEY=your_api_key
BAIDU_SECRET_KEY=your_secret_key

# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

### 语音参数调优

**TTS参数建议**：
- **语速 (speed)**：5-7 (适中到稍快)
- **音调 (pitch)**：5-6 (自然到稍高)
- **音量 (volume)**：5 (正常音量)

**ASR优化**：
- 使用16kHz采样率
- 单声道录音
- 启用回声消除和噪声抑制

## 🧪 测试工具

运行完整功能测试：
```bash
python3 test_speech_endpoints.py
```

测试单个功能：
```bash
# 测试TTS
curl -X POST http://127.0.0.1:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "测试语音合成"}' \
  --output test.wav

# 测试ASR
curl -X POST http://127.0.0.1:8000/asr \
  -F "audio_file=@test.wav"
```

## 📊 性能指标

**典型性能**：
- **TTS合成**：1-2秒 (短文本)
- **ASR识别**：1-3秒 (5秒音频)
- **AI对话**：5-15秒 (取决于问题复杂度)

**音频质量**：
- **TTS输出**：16kHz WAV格式
- **ASR输入**：支持多种格式，推荐16kHz WAV

## ❗ 注意事项

1. **网络要求**：需要稳定的网络连接访问百度云API
2. **音频大小**：建议单次音频文件不超过60秒
3. **文本长度**：TTS单次合成建议不超过500字符
4. **并发限制**：百度云API有调用频率限制
5. **错误处理**：网络异常时会返回相应错误信息

## 🔍 故障排除

### 常见问题

**1. 语音识别失败**
- 检查音频格式是否支持
- 确认网络连接正常
- 验证百度云API密钥

**2. 语音合成无声音**
- 检查音频播放设备
- 确认TTS请求成功返回
- 验证音频文件完整性

**3. API调用失败**
- 检查服务器是否启动
- 确认端口8000未被占用
- 查看后端日志错误信息

### 日志查看

后端服务器会输出详细的操作日志，包括：
- API调用时间
- 音频文件大小
- 识别/合成结果
- 错误信息

## 📞 技术支持

如遇问题，请检查：
1. 服务器启动日志
2. 浏览器控制台错误
3. 网络连接状态
4. API密钥配置

---

*最后更新：2025-07-27*
