#!/bin/bash

# 启动语音功能调试服务器
# 解决语音识别功能故障的临时方案

echo "🎤 启动涂序彦教授数字人 - 语音功能调试模式"
echo "=================================================="

# 检查conda环境
check_env() {
    if ! command -v conda &> /dev/null; then
        echo "❌ conda未找到，请先安装conda"
        exit 1
    fi
    
    if ! conda env list | grep -q "tuxuyan_env"; then
        echo "❌ 未找到tuxuyan_env环境"
        exit 1
    fi
    
    echo "✅ conda环境检查通过"
}

# 启动后端调试服务器
start_backend() {
    echo "🚀 启动后端调试服务器..."
    
    # 激活环境并启动服务器
    source /opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh
    conda activate tuxuyan_env
    
    echo "📡 启动调试API服务器 (端口8000)..."
    python debug_server.py &
    BACKEND_PID=$!
    
    # 等待服务器启动
    echo "⏳ 等待服务器启动..."
    sleep 3
    
    # 检查服务器状态
    if curl -s http://127.0.0.1:8000/ > /dev/null; then
        echo "✅ 后端调试服务器启动成功"
        echo "   - API地址: http://127.0.0.1:8000"
        echo "   - 模式: 调试模式（模拟语音API）"
    else
        echo "❌ 后端服务器启动失败"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    
    return $BACKEND_PID
}

# 启动前端服务器
start_frontend() {
    echo "🌐 启动前端服务器..."
    
    if [ ! -d "react-version" ]; then
        echo "❌ 未找到react-version目录"
        exit 1
    fi
    
    cd react-version
    
    # 检查依赖
    if [ ! -d "node_modules" ]; then
        echo "📦 安装前端依赖..."
        npm install
    fi
    
    echo "🚀 启动React开发服务器..."
    npm start &
    FRONTEND_PID=$!
    
    cd ..
    
    echo "✅ 前端服务器启动中..."
    echo "   - 前端地址: http://localhost:3000"
    
    return $FRONTEND_PID
}

# 显示使用说明
show_usage() {
    echo ""
    echo "🎉 语音功能调试服务启动完成！"
    echo "=================================================="
    echo ""
    echo "📱 访问地址:"
    echo "   前端界面: http://localhost:3000"
    echo "   后端API:  http://127.0.0.1:8000"
    echo ""
    echo "🎤 语音功能说明:"
    echo "   - 点击录音按钮开始语音输入"
    echo "   - 录音完成后自动识别并发送给AI"
    echo "   - 开启TTS开关可自动播放AI回复"
    echo "   - 当前使用模拟语音服务（调试模式）"
    echo ""
    echo "🔧 调试信息:"
    echo "   - ASR: 返回预设的识别文本"
    echo "   - TTS: 返回静音音频文件"
    echo "   - 后端日志显示详细处理过程"
    echo ""
    echo "📋 测试建议:"
    echo "   1. 测试录音功能（观察音量指示器）"
    echo "   2. 测试语音识别（查看识别结果）"
    echo "   3. 测试AI对话（发送识别文本）"
    echo "   4. 测试语音播放（播放AI回复）"
    echo ""
    echo "🛑 停止服务: 按 Ctrl+C"
}

# 清理函数
cleanup() {
    echo ""
    echo "🛑 正在停止服务..."
    
    # 停止后端服务器
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ 后端服务器已停止"
    fi
    
    # 停止前端服务器
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ 前端服务器已停止"
    fi
    
    # 清理端口
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    
    echo "🎯 所有服务已停止"
    exit 0
}

# 设置信号处理
trap cleanup INT TERM

# 主程序
main() {
    check_env
    
    # 启动后端
    start_backend
    BACKEND_PID=$!
    
    # 启动前端
    start_frontend  
    FRONTEND_PID=$!
    
    # 显示使用说明
    show_usage
    
    # 等待用户中断
    echo "⏳ 服务运行中，按 Ctrl+C 停止..."
    wait
}

# 运行主程序
main
