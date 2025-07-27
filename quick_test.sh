#!/bin/bash

# 快速测试语音API功能

echo "🧪 快速测试语音API功能"
echo "========================"

BASE_URL="http://127.0.0.1:8000"

# 测试健康检查
echo "1. 测试健康检查..."
if curl -s "$BASE_URL/" > /dev/null; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务未启动，请先运行: python api_server.py"
    exit 1
fi

# 测试语音状态
echo "2. 测试语音服务状态..."
curl -s "$BASE_URL/speech_status" | python3 -m json.tool

# 测试TTS
echo "3. 测试TTS功能..."
curl -X POST "$BASE_URL/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，我是涂序彦教授", "voice": "zh-CN-male"}' \
  --output test_tts.wav \
  --silent

if [ -f "test_tts.wav" ] && [ -s "test_tts.wav" ]; then
    echo "✅ TTS测试成功，音频已保存为 test_tts.wav"
else
    echo "❌ TTS测试失败"
fi

# 测试ASR (创建模拟音频文件)
echo "4. 测试ASR功能..."
echo -e "RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x80\x3e\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00" > test_audio.wav
curl -X POST "$BASE_URL/asr" \
  -F "audio_file=@test_audio.wav" \
  --silent | python3 -m json.tool

# 清理临时文件
rm -f test_audio.wav

echo ""
echo "🎉 测试完成！"
echo "如果所有测试都通过，语音功能已正常工作。"
