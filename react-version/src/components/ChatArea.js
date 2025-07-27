import React, { useState, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import InputArea from './InputArea';
import WelcomeScreen from './WelcomeScreen';
import DigitalHuman from './DigitalHuman';
import ChatHeader from './ChatHeader';

// 随机欢迎消息数组
const randomWelcomeMessages = [
  "在忙什么？",
  "糊涂居士玩转AI！",
  "您好！我是涂先生数字人模型。",
  "很高兴见到您!",
  "Hello USTB!",
  "I love AI!"
];

const ChatArea = ({ isWelcoming, messages, addMessage, updateMessage }) => {
  const [welcomeMessage, setWelcomeMessage] = useState(randomWelcomeMessages[
    Math.floor(Math.random() * randomWelcomeMessages.length)
  ]);
  const [isTtsOn, setIsTtsOn] = useState(false);
  const contentRef = useRef(null);

  // 欢迎语随机刷新效果
  useEffect(() => {
    if (isWelcoming) {
      const interval = setInterval(() => {
        // 确保选择不同的欢迎消息
        setWelcomeMessage(prevMessage => {
          const availableMessages = randomWelcomeMessages.filter(msg => msg !== prevMessage);
          const randomIndex = Math.floor(Math.random() * availableMessages.length);
          return availableMessages[randomIndex] || randomWelcomeMessages[0];
        });
      }, 4000); // 每4秒刷新一次，给打字机效果足够时间

      return () => clearInterval(interval);
    }
  }, [isWelcoming]);

  // 动态视口高度计算（处理移动端浏览器地址栏）
  useEffect(() => {
    const updateViewportHeight = () => {
      // 获取真实的视口高度
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    };

    // 初始设置
    updateViewportHeight();

    // 监听窗口大小变化
    window.addEventListener('resize', updateViewportHeight);
    window.addEventListener('orientationchange', updateViewportHeight);

    // 清理事件监听器
    return () => {
      window.removeEventListener('resize', updateViewportHeight);
      window.removeEventListener('orientationchange', updateViewportHeight);
    };
  }, []);

  // 自动滚动到底部
  useEffect(() => {
    if (contentRef.current && !isWelcoming) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [messages, isWelcoming]);

  // 处理发送消息
  const handleSendMessage = async (messageText, audioBlob = null) => {
    console.log("ChatArea - 处理发送消息:", messageText);

    if (!messageText.trim() && !audioBlob) return;

    // 添加用户消息
    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date(),
      audioBlob: audioBlob
    };

    addMessage(userMessage);

    // 添加AI思考状态
    const thinkingMessage = {
      id: Date.now() + 1,
      text: '',
      sender: 'ai',
      timestamp: new Date(),
      isThinking: true
    };

    addMessage(thinkingMessage);

    try {
      // 调用真正的后端API
      console.log("🚀 调用后端AI API...");

      // 创建AbortController用于超时控制
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60秒超时

      const response = await fetch('http://127.0.0.1:8000/ask_professor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: messageText
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId); // 清除超时定时器

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API调用失败: ${response.status} ${response.statusText}\n详情: ${errorText}`);
      }

      const result = await response.json();
      console.log("✅ AI API响应:", result);

      // 更新AI消息
      const aiResponse = {
        id: thinkingMessage.id,
        text: result.answer || '抱歉，我暂时无法回答这个问题。',
        sender: 'ai',
        timestamp: new Date(),
        isThinking: false,
        isNew: true,  // 标记为新消息，用于自动播放
        source: result.source || 'unknown',
        thinking_time: result.thinking_time || 0
      };

      updateMessage(aiResponse);

      // 清除isNew标记，避免重复自动播放
      setTimeout(() => {
        updateMessage({ ...aiResponse, isNew: false });
      }, 1000);

    } catch (error) {
      console.error("❌ AI API调用失败:", error);

      let errorMessage = "抱歉，AI服务暂时不可用。";
      let canRetry = false;

      if (error.name === 'AbortError') {
        errorMessage = "⏰ 请求超时（60秒），AI可能正在处理复杂问题。";
        canRetry = true;
      } else if (error.message.includes('Failed to fetch')) {
        errorMessage = "🌐 网络连接失败，请检查网络连接。";
        canRetry = true;
      } else if (error.message.includes('500')) {
        errorMessage = "🔧 服务器内部错误，请稍后重试。";
        canRetry = true;
      } else if (error.message.includes('404')) {
        errorMessage = "❓ API端点不存在，请检查后端服务器配置。";
      } else {
        errorMessage = `❌ 未知错误：${error.message}`;
        canRetry = true;
      }

      // 显示错误消息
      const errorResponse = {
        id: thinkingMessage.id,
        text: `${errorMessage}\n\n${canRetry ? '💡 您可以点击重试按钮重新发送消息。' : ''}`,
        sender: 'ai',
        timestamp: new Date(),
        isThinking: false,
        isError: true,
        canRetry: canRetry,
        originalPrompt: messageText
      };

      updateMessage(errorResponse);
    }
  };

  // 检查是否有AI正在思考
  const isAiThinking = messages.some(msg => msg.isThinking);

  return (
    <div className="h-full flex flex-col fullscreen-chat-container">
      {/* 主要内容区域 - 全屏高度数字人和聊天卡片布局 */}
      <div className="flex-1 p-4 lg:p-6 xl:p-8 min-h-0">
        <div className="h-full max-w-7xl mx-auto">
          {/* 卡片容器 - 全屏高度适配 */}
          <div className="h-full max-w-5xl mx-auto">
            <div className="h-full flex gap-4 lg:gap-6 transition-all duration-300 ease-out fullscreen-grid golden-ratio-layout">

              {/* 数字人卡片 - 与聊天卡片同高，9:16比例 */}
              <div className="digital-human-container fullscreen-card-height">
                <div className="digital-human-card">
                  <DigitalHuman
                    isThinking={isAiThinking}
                    isWelcoming={isWelcoming}
                    welcomeMessage={welcomeMessage}
                  />
                </div>
              </div>

              {/* 统一聊天卡片 - 黄金比例宽度，全屏高度 */}
              <div className="chat-container fullscreen-card-height flex-1">
                <div className="h-full bg-white rounded-2xl shadow-sm border border-gray-200 flex flex-col overflow-hidden fullscreen-chat-card">
                  {/* 聊天卡片顶部 - 校徽区域，固定高度 */}
                  <div className="flex-shrink-0">
                    <ChatHeader />
                  </div>

                  {/* 聊天内容区域 - 可滚动，占据剩余空间 */}
                  <div ref={contentRef} className="flex-1 min-h-0 overflow-y-auto chat-messages-container">
                    <div className="p-4 h-full">
                      {isWelcoming ? (
                        <div className="flex items-center justify-center h-full min-h-[300px]">
                          <WelcomeScreen message={welcomeMessage} />
                        </div>
                      ) : (
                        <MessageList
                          messages={messages}
                          isTtsOn={isTtsOn}
                          onRetryMessage={handleSendMessage}
                        />
                      )}
                    </div>
                  </div>

                  {/* 输入框区域 - 固定在底部，增加左右边距 */}
                  <div className="flex-shrink-0 px-6 py-4 bg-gray-50/50 chat-input-fixed">
                    <InputArea
                      onSendMessage={handleSendMessage}
                      isTtsOn={isTtsOn}
                      setIsTtsOn={setIsTtsOn}
                      isWelcoming={isWelcoming}
                      inlineStyle={true}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatArea;
