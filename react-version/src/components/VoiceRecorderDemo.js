import React, { useState } from 'react';

const VoiceRecorderDemo = () => {
  const [demoState, setDemoState] = useState('idle'); // idle, recording, processing

  const handleStateChange = (newState) => {
    setDemoState(newState);
    
    // 自动重置状态用于演示
    if (newState === 'recording') {
      setTimeout(() => setDemoState('processing'), 3000);
    } else if (newState === 'processing') {
      setTimeout(() => setDemoState('idle'), 2000);
    }
  };

  return (
    <div className="p-8 bg-white">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">语音录音按钮设计演示</h2>
      
      {/* 按钮状态演示 */}
      <div className="space-y-8">
        
        {/* 未录音状态 */}
        <div className="flex items-center gap-4">
          <button
            className="voice-recorder-btn"
            onClick={() => handleStateChange('recording')}
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 715 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
            </svg>
          </button>
          <div>
            <h3 className="font-semibold text-gray-800">未录音状态</h3>
            <p className="text-sm text-gray-600">黑色麦克风图标，透明背景，灰色边框</p>
          </div>
        </div>

        {/* 录音状态 */}
        <div className="flex items-center gap-4">
          <button
            className="voice-recorder-btn recording"
            onClick={() => handleStateChange('processing')}
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 715 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
            </svg>
            <div className="absolute inset-0 rounded-full border-2 border-white opacity-30 animate-ping"></div>
          </button>
          <div>
            <h3 className="font-semibold text-gray-800">录音状态</h3>
            <p className="text-sm text-gray-600">白色麦克风图标，黑色背景，脉冲动画</p>
          </div>
        </div>

        {/* 处理状态 */}
        <div className="flex items-center gap-4">
          <button
            className="voice-recorder-btn processing"
            disabled
          >
            <div className="w-5 h-5 border-2 border-gray-600 border-t-transparent rounded-full animate-spin"></div>
          </button>
          <div>
            <h3 className="font-semibold text-gray-800">处理状态</h3>
            <p className="text-sm text-gray-600">加载动画，禁用状态</p>
          </div>
        </div>

      </div>

      {/* 当前演示状态 */}
      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-semibold mb-2">当前演示状态: {demoState}</h3>
        <div className="flex items-center gap-4">
          <button
            className={`voice-recorder-btn ${demoState === 'recording' ? 'recording' : ''} ${demoState === 'processing' ? 'processing' : ''}`}
            onClick={() => {
              if (demoState === 'idle') handleStateChange('recording');
              else if (demoState === 'recording') handleStateChange('processing');
              else setDemoState('idle');
            }}
            disabled={demoState === 'processing'}
          >
            {demoState === 'processing' ? (
              <div className="w-5 h-5 border-2 border-gray-600 border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <>
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 715 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
                </svg>
                {demoState === 'recording' && (
                  <div className="absolute inset-0 rounded-full border-2 border-white opacity-30 animate-ping"></div>
                )}
              </>
            )}
          </button>
          
          {/* 模拟录音状态显示 */}
          {(demoState === 'recording' || demoState === 'processing') && (
            <div className="recording-status">
              {demoState === 'recording' && (
                <div className="flex items-center gap-2">
                  <div className="w-1.5 h-6 bg-gray-200 rounded-full overflow-hidden">
                    <div className="w-full bg-black rounded-full transition-all duration-100 animate-pulse" style={{ height: '60%', transform: 'translateY(40%)' }}></div>
                  </div>
                  <div className="w-2 h-2 rounded-full bg-black animate-pulse"></div>
                </div>
              )}
              
              <span className="text-sm font-mono text-gray-800 font-medium">
                {demoState === 'processing' ? '处理中...' : '0:03'}
              </span>
              
              <span className="text-sm text-gray-600">
                {demoState === 'processing' ? '正在处理录音...' : '正在录音...'}
              </span>
              
              {demoState === 'recording' && (
                <div className="flex items-center gap-0.5">
                  {[...Array(3)].map((_, i) => (
                    <div
                      key={i}
                      className="w-0.5 bg-black rounded-full animate-pulse"
                      style={{
                        height: `${12 + Math.sin(Date.now() / 200 + i) * 4}px`,
                        animationDelay: `${i * 0.1}s`
                      }}
                    ></div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* 设计说明 */}
      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-800 mb-2">设计特点</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• <strong>黑白双色调</strong>：与整体界面保持和谐</li>
          <li>• <strong>清晰状态区分</strong>：未录音（透明）、录音中（黑色）、处理中（灰色）</li>
          <li>• <strong>平滑过渡动画</strong>：300ms缓动效果</li>
          <li>• <strong>视觉反馈</strong>：悬停效果、焦点状态、脉冲动画</li>
          <li>• <strong>无障碍设计</strong>：清晰的对比度、键盘导航支持</li>
        </ul>
      </div>
    </div>
  );
};

export default VoiceRecorderDemo;
