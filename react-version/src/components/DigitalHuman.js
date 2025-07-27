import React, { useState, useEffect } from 'react';
import teamLogo from '../assets/team-logo.png';
import BackendStatusDetector, { BackendStatusIndicator } from './BackendStatusDetector';

const DigitalHuman = ({ isThinking, isWelcoming, welcomeMessage }) => {
  const [renderKey] = useState(Date.now());
  const [backendStatus, setBackendStatus] = useState(null);

  // 使用后端状态检测器
  const { status, manualCheck } = BackendStatusDetector({
    onStatusChange: setBackendStatus
  });

  // 更新状态
  useEffect(() => {
    setBackendStatus(status);
  }, [status]);

  // 队徽样式 - 原色显示
  const teamLogoStyle = {
    height: '36px', // 与校徽保持一致的高度
    width: 'auto',
    filter: 'none', // 移除灰度滤镜，显示原色
    transition: 'filter 0.3s ease',
  };

  return (
    <div className="flex flex-col h-full digital-human-content">
      {/* 顶部队徽和介绍区域 - 水平排列，完美居中 */}
      <div className="flex flex-row items-center justify-center p-3 flex-shrink-0">
        {/* 队徽图标 - 左侧 */}
        <img
          src={`${teamLogo}?v=${renderKey}`}
          alt="实践团徽"
          style={teamLogoStyle}
          onMouseOver={(e) => e.target.style.filter = 'brightness(1.1) saturate(1.2)'}
          onMouseOut={(e) => e.target.style.filter = 'none'}
          className="mr-3 flex-shrink-0"
        />

        {/* 介绍文字 - 右侧 */}
        <div className="flex flex-col">
          <h3 className="text-sm font-bold text-gray-800 mb-1">井溯序焰长明科技实践团</h3>
          <p className="text-xs text-gray-600">涂序彦教授数字人模型</p>
        </div>
      </div>

      {/* 数字人头像/视频区域 - 确保填满剩余空间 */}
      <div className="flex-1 flex flex-col items-center justify-center p-6 digital-human-content">
        {/* 数字人头像占位符 */}
        <div className="digital-human-avatar w-48 h-48 md:w-56 md:h-56 lg:w-64 lg:h-64 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-6 shadow-lg border-4 border-white">
          <div className="text-6xl md:text-7xl lg:text-8xl">
            👨‍🏫
          </div>
        </div>

        {/* 数字人状态显示 - 向上移动 */}
        <div
          className="text-center space-y-4 max-w-xs"
          style={{
            transform: 'translateY(-20px)', // 向上移动20px
            transition: 'transform 0.3s ease-in-out'
          }}
        >
          {/* 欢迎消息或状态 - 紧凑布局 */}
          {isWelcoming ? (
            <div className="space-y-1">
              <h2 className="text-lg font-semibold text-gray-800">
                涂序彦教授
              </h2>
              <p className="text-gray-600 text-sm leading-relaxed">
                {welcomeMessage || "我是涂序彦教授，很高兴与您交流。"}
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              <h2 className="text-lg font-medium text-gray-800">
                涂序彦教授
              </h2>
              
              {/* 状态指示器 - 集成后端状态检测 */}
              {isThinking ? (
                <div className="flex items-center justify-center">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <BackendStatusIndicator
                    status={status}
                    onManualCheck={manualCheck}
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>

    </div>
  );
};

export default DigitalHuman;
