import React, { useState, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import InputArea from './InputArea';
import WelcomeScreen from './WelcomeScreen';

// 随机欢迎消息
const randomWelcomeMessages = [
  "我是涂序彦。", 
  "今天想和我交流什么？", 
  "很高兴能与您交流。",
  "有什么可以帮您的吗？", 
  "探索AI，从这里开始。"
];

const ChatArea = ({ isWelcoming, messages, addMessage, updateMessage }) => {
  const [welcomeMessage] = useState(randomWelcomeMessages[
    Math.floor(Math.random() * randomWelcomeMessages.length)
  ]);
  const [isTtsOn, setIsTtsOn] = useState(true);
  const contentRef = useRef(null);

  // 生成唯一ID的函数
  const generateUniqueId = () => {
    return `msg-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;
  };

  // 打字机效果函数 - 重新设计
  const typewriterEffect = (text, thinkingMessageId, startTime, updateMessage) => {
    const words = text.split(' ');
    let currentText = '';
    let wordIndex = 0;

    const typeInterval = setInterval(() => {
      if (wordIndex < words.length) {
        currentText += (wordIndex > 0 ? ' ' : '') + words[wordIndex];

        // 更新思考消息为当前打字内容
        const updatedMessage = {
          id: thinkingMessageId,
          text: currentText,
          sender: 'bot',
          timestamp: Date.now(),
          isTyping: true,
          isThinking: false
        };

        updateMessage(updatedMessage);
        wordIndex++;
      } else {
        // 打字完成，显示完成状态
        const endTime = Date.now();
        const duration = ((endTime - startTime) / 1000).toFixed(1);

        const finalMessage = {
          id: thinkingMessageId,
          text: text,
          sender: 'bot',
          timestamp: Date.now(),
          isTyping: false,
          isThinking: false,
          duration: duration,
          isCompleted: true
        };

        updateMessage(finalMessage);
        clearInterval(typeInterval);
      }
    }, 180); // 调整为180ms每词，更舒适的阅读速度
  };

  // 真实API调用 - 重新设计，避免重复消息
  const handleSendMessage = async (text) => {
    const userMessageId = generateUniqueId();
    const startTime = Date.now();

    console.log("发送消息，用户消息ID:", userMessageId);

    // 添加用户消息
    const userMessage = {
      id: userMessageId,
      text,
      sender: 'user',
      timestamp: Date.now()
    };

    addMessage(userMessage);
    console.log("用户消息已添加:", userMessage);

    // 记录开始时间

    // 添加唯一的思考状态消息
    const thinkingMessageId = generateUniqueId();
    const thinkingMessage = {
      id: thinkingMessageId,
      text: "正在思考...",
      sender: 'bot',
      timestamp: Date.now(),
      isThinking: true
    };
    addMessage(thinkingMessage);

    // 使用传入的updateMessage函数

    try {
      console.log("发送请求到后端API...");

      // 真实API请求
      const response = await fetch('http://127.0.0.1:8000/ask_professor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: text }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API错误 ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log("收到API响应:", data);

      if (!data || !data.answer) {
        throw new Error("API响应格式错误：缺少answer字段");
      }

      // 开始打字机效果，直接更新思考消息
      typewriterEffect(data.answer, thinkingMessageId, startTime, updateMessage);

      console.log("开始打字机效果:", data.answer);

    } catch (error) {
      console.error("API调用错误:", error);

      // 更新思考消息为错误消息
      const errorMessage = {
        id: thinkingMessageId,
        text: `❌ 连接错误: ${error.message}\n\n请确保后端服务器正在运行在 http://127.0.0.1:8000`,
        sender: 'bot',
        timestamp: Date.now(),
        isThinking: false,
        isError: true
      };

      updateMessage(errorMessage);
      console.log("错误消息已更新:", errorMessage);
    }
  };

  // 滚动到底部
  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className={`flex-grow flex flex-col overflow-y-auto px-4 relative ${isWelcoming ? 'items-center' : ''}`}>
      {/* Scrollable content */}
      <div ref={contentRef} className={`flex-grow overflow-y-auto flex flex-col ${isWelcoming ? 'justify-center w-full' : ''}`}>
        {isWelcoming ? (
          <>
            <WelcomeScreen message={welcomeMessage} />
            {/* 在欢迎状态下，将输入框放在内容区域内，以实现真正的垂直居中 */}
            <div className="w-full max-w-3xl mx-auto mt-12">
              <InputArea 
                onSendMessage={handleSendMessage} 
                isTtsOn={isTtsOn}
                setIsTtsOn={setIsTtsOn}
                isWelcoming={isWelcoming}
                inlineStyle={true}
              />
            </div>
          </>
        ) : (
          <MessageList messages={messages} />
        )}
      </div>

      {/* Footer input area - 只在非欢迎状态下显示 */}
      {!isWelcoming && (
        <div className="mt-auto">
          <InputArea 
            onSendMessage={handleSendMessage} 
            isTtsOn={isTtsOn}
            setIsTtsOn={setIsTtsOn}
            isWelcoming={isWelcoming}
            inlineStyle={false}
          />
        </div>
      )}
    </div>
  );
};

export default ChatArea; 