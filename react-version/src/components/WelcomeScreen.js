import React, { useState, useEffect } from 'react';
import useTypewriter from '../hooks/useTypewriter';

const WelcomeScreen = ({ message }) => {
  const { displayText, isTyping } = useTypewriter(message, 100); // 调整为100ms，更流畅的速度
  const [animationKey, setAnimationKey] = useState(0);

  // 当消息改变时，触发动画重新开始
  useEffect(() => {
    setAnimationKey(prev => prev + 1);
  }, [message]);

  return (
    <div className="flex flex-col items-center justify-center text-center p-8">
      <div className="max-w-md mx-auto space-y-4">
        <div className="text-center">
          <p
            key={animationKey}
            className="text-3xl font-bold text-gray-800 leading-relaxed welcome-message animate-fade-in"
            style={{
              minHeight: '4rem', // 确保高度一致，避免布局跳动
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            {displayText}
            {isTyping && <span className="typing-cursor animate-pulse ml-1">|</span>}
          </p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;