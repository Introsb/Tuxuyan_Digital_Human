#!/bin/bash

# 涂序彦教授数字人 - 语音功能安装脚本
# 自动安装和配置ASR/TTS功能

set -e  # 遇到错误立即退出

echo "🎯 涂序彦教授数字人 - 语音功能安装脚本"
echo "=================================================="

# 检查conda环境
check_conda_env() {
    echo "🔍 检查conda环境..."
    
    if ! command -v conda &> /dev/null; then
        echo "❌ conda未找到，请先安装Miniconda或Anaconda"
        exit 1
    fi
    
    if conda env list | grep -q "tuxuyan_env"; then
        echo "✅ 找到tuxuyan_env环境"
    else
        echo "❌ 未找到tuxuyan_env环境，请先创建"
        echo "   conda create -n tuxuyan_env python=3.10"
        exit 1
    fi
}

# 激活conda环境
activate_env() {
    echo "🔄 激活conda环境..."
    source /opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh
    conda activate tuxuyan_env
    echo "✅ 环境激活成功"
}

# 安装Python依赖
install_python_deps() {
    echo "📦 安装Python依赖..."
    
    # 基础依赖
    pip install --upgrade pip
    
    # 百度语音SDK
    echo "   - 安装百度语音SDK..."
    pip install baidu-aip
    
    # 字符编码支持
    echo "   - 安装字符编码支持..."
    pip install chardet
    
    # Web框架依赖
    echo "   - 安装Web框架依赖..."
    pip install fastapi uvicorn python-multipart
    
    # HTTP客户端
    echo "   - 安装HTTP客户端..."
    pip install requests
    
    echo "✅ Python依赖安装完成"
}

# 检查前端依赖
check_frontend_deps() {
    echo "🔍 检查前端依赖..."
    
    if [ ! -d "react-version/node_modules" ]; then
        echo "📦 安装前端依赖..."
        cd react-version
        npm install
        cd ..
        echo "✅ 前端依赖安装完成"
    else
        echo "✅ 前端依赖已存在"
    fi
}

# 测试API功能
test_api() {
    echo "🧪 测试API功能..."
    
    # 启动后端服务（后台）
    echo "   - 启动后端服务..."
    python api_server.py &
    SERVER_PID=$!
    
    # 等待服务启动
    sleep 5
    
    # 测试健康检查
    if curl -s http://127.0.0.1:8000/ > /dev/null; then
        echo "✅ 后端服务启动成功"
    else
        echo "❌ 后端服务启动失败"
        kill $SERVER_PID 2>/dev/null || true
        exit 1
    fi
    
    # 测试语音状态
    if curl -s http://127.0.0.1:8000/speech_status > /dev/null; then
        echo "✅ 语音API端点正常"
    else
        echo "❌ 语音API端点异常"
    fi
    
    # 停止后端服务
    kill $SERVER_PID 2>/dev/null || true
    sleep 2
}

# 创建启动脚本
create_start_scripts() {
    echo "📝 创建启动脚本..."
    
    # 后端启动脚本
    cat > start_backend.sh << 'EOF'
#!/bin/bash
echo "🚀 启动涂序彦教授数字人后端服务..."
source /opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh
conda activate tuxuyan_env
python api_server.py
EOF
    
    # 前端启动脚本
    cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "🚀 启动涂序彦教授数字人前端服务..."
cd react-version
npm start
EOF
    
    # 完整启动脚本
    cat > start_all.sh << 'EOF'
#!/bin/bash
echo "🚀 启动涂序彦教授数字人完整服务..."

# 启动后端
echo "启动后端服务..."
./start_backend.sh &
BACKEND_PID=$!

# 等待后端启动
sleep 5

# 启动前端
echo "启动前端服务..."
./start_frontend.sh &
FRONTEND_PID=$!

echo "✅ 服务启动完成！"
echo "   - 后端: http://127.0.0.1:8000"
echo "   - 前端: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo '停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
EOF
    
    # 设置执行权限
    chmod +x start_backend.sh start_frontend.sh start_all.sh
    
    echo "✅ 启动脚本创建完成"
}

# 显示使用说明
show_usage() {
    echo ""
    echo "🎉 安装完成！"
    echo "=================================================="
    echo ""
    echo "📋 使用说明:"
    echo ""
    echo "1. 启动完整服务:"
    echo "   ./start_all.sh"
    echo ""
    echo "2. 分别启动服务:"
    echo "   ./start_backend.sh   # 后端服务"
    echo "   ./start_frontend.sh  # 前端服务"
    echo ""
    echo "3. 手动启动:"
    echo "   # 后端"
    echo "   conda activate tuxuyan_env"
    echo "   python api_server.py"
    echo ""
    echo "   # 前端 (新终端)"
    echo "   cd react-version"
    echo "   npm start"
    echo ""
    echo "4. 测试API:"
    echo "   python test_speech_api.py"
    echo ""
    echo "📖 详细文档:"
    echo "   - SPEECH_INTEGRATION_GUIDE.md"
    echo ""
    echo "🌐 访问地址:"
    echo "   - 前端界面: http://localhost:3000"
    echo "   - 后端API: http://127.0.0.1:8000"
    echo ""
    echo "🎤 语音功能:"
    echo "   - 点击录音按钮开始语音输入"
    echo "   - 开启TTS开关自动播放AI回复"
    echo "   - 支持手动播放每条AI消息"
}

# 主安装流程
main() {
    echo "开始安装语音功能..."
    echo ""
    
    check_conda_env
    activate_env
    install_python_deps
    check_frontend_deps
    test_api
    create_start_scripts
    show_usage
    
    echo ""
    echo "🎯 安装完成！现在可以使用完整的语音交互功能了。"
}

# 错误处理
handle_error() {
    echo ""
    echo "❌ 安装过程中出现错误！"
    echo "请检查错误信息并重试。"
    echo ""
    echo "常见问题:"
    echo "1. 确保conda环境正确安装"
    echo "2. 检查网络连接"
    echo "3. 确认权限设置"
    exit 1
}

# 设置错误处理
trap handle_error ERR

# 运行主程序
main
