import React, { useState, useRef, useEffect } from 'react';
import { MicrophoneIcon, SpeakerWaveIcon, PaperAirplaneIcon } from './Icons';
import VoiceRecorderOptimized from './VoiceRecorderOptimized';

const InputArea = ({ onSendMessage, isTtsOn, setIsTtsOn, isWelcoming, inlineStyle }) => {
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [voiceError, setVoiceError] = useState(null);
  const [asrStatus, setAsrStatus] = useState(null); // ASR状态管理
  const textareaRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedInput = userInput.trim();

    if (!trimmedInput || isLoading) return;

    setIsLoading(true);

    // 立即清空输入框并保持焦点
    setUserInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'; // 重置高度
      textareaRef.current.focus();
    }

    await onSendMessage(trimmedInput);
    setIsLoading(false);
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // 处理录音完成 - 优化版本
  const handleRecordingComplete = async (formData) => {
    try {
      // 清除之前的错误和状态
      setVoiceError(null);
      setAsrStatus('processing');

      console.log('🎤 开始语音识别...');

      // 调用ASR API
      const response = await fetch('http://127.0.0.1:8000/asr', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`ASR服务错误: ${response.status}`);
      }

      const result = await response.json();
      console.log('🎤 ASR响应:', result);

      if (result.success && result.text && result.text.trim()) {
        const recognizedText = result.text.trim();
        console.log('✅ 语音识别成功:', recognizedText);

        // 设置成功状态
        setAsrStatus('success');

        // 将识别的文本设置到输入框
        setUserInput(recognizedText);

        // 确保文本框获得焦点并调整高度
        setTimeout(() => {
          if (textareaRef.current) {
            textareaRef.current.focus();
            textareaRef.current.setSelectionRange(recognizedText.length, recognizedText.length);
            adjustTextareaHeight();
          }
        }, 100);

        // 3秒后自动清除成功状态
        setTimeout(() => {
          setAsrStatus(null);
        }, 3000);

      } else {
        const errorMsg = result.message || '语音识别失败或未识别到内容';
        console.warn('⚠️ 语音识别问题:', errorMsg);
        setAsrStatus('error');
        setVoiceError(errorMsg);

        // 5秒后自动清除错误状态
        setTimeout(() => {
          setAsrStatus(null);
          setVoiceError(null);
        }, 5000);
      }

    } catch (error) {
      console.error('❌ 语音识别失败:', error);
      setAsrStatus('error');
      setVoiceError(error.message);

      // 5秒后自动清除错误状态
      setTimeout(() => {
        setAsrStatus(null);
        setVoiceError(null);
      }, 5000);
    }
  };

  // 处理录音错误
  const handleRecordingError = (error) => {
    console.error('录音错误:', error);
    setVoiceError(error);
  };
  
  // 自适应高度调整函数 - 优化版本
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      // 重置高度以获取正确的scrollHeight
      textarea.style.height = 'auto';

      // 计算新高度，设置最小和最大高度限制
      const minHeight = 60; // 最小高度
      const maxHeight = 200; // 最大高度
      const newHeight = Math.max(minHeight, Math.min(textarea.scrollHeight, maxHeight));

      // 应用新高度
      textarea.style.height = `${newHeight}px`;

      // 如果内容超过最大高度，显示滚动条
      if (textarea.scrollHeight > maxHeight) {
        textarea.style.overflowY = 'auto';
      } else {
        textarea.style.overflowY = 'hidden';
      }
    }
  };

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
    // 使用setTimeout确保DOM更新后再调整高度
    setTimeout(() => adjustTextareaHeight(), 0);
  };

  // 内联样式：用于聊天卡片底部的输入框
  if (inlineStyle) {
    return (
      <div className="w-full transition-all duration-300">
        <div className="relative w-full">
          <form onSubmit={handleSubmit} className="w-full">
            {/* 主输入区域 - 包含内部按钮 */}
            <div className="relative w-full">
              <textarea
                ref={textareaRef}
                className="w-full min-h-[60px] p-4 pr-32 text-sm resize-none border border-gray-200 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 ease-in-out"
                placeholder="询问任何问题..."
                value={userInput}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                rows={1}
                style={{
                  height: '60px',
                  transition: 'height 0.3s ease-in-out'
                }}
              />

              {/* 内部按钮组 - 录音、语音播放、发送 */}
              <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex items-center gap-1">
                {/* 录音按钮 - 第一位 */}
                <VoiceRecorderOptimized
                  onRecordingComplete={handleRecordingComplete}
                  disabled={isLoading}
                />

                {/* TTS语音播放按钮 - 第二位，统一尺寸 */}
                <button
                  type="button"
                  onClick={() => setIsTtsOn(!isTtsOn)}
                  className={`w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 ${
                    isTtsOn
                      ? 'bg-green-500 text-white shadow-sm hover:bg-green-600 hover:scale-105'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200 hover:scale-105'
                  }`}
                  title={isTtsOn ? '关闭语音播放' : '开启语音播放'}
                >
                  <SpeakerWaveIcon className="w-4 h-4" />
                </button>

                {/* 发送按钮 - 第三位，内部布局 */}
                <button
                  type="submit"
                  disabled={!userInput.trim() || isLoading}
                  className={`w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 ${
                    userInput.trim() && !isLoading
                      ? 'bg-blue-500 text-white hover:bg-blue-600 shadow-sm hover:scale-105'
                      : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  }`}
                  title="发送消息 (Enter)"
                >
                  {isLoading ? (
                    <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <PaperAirplaneIcon className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>
          </form>

          {/* 语音错误提示 */}
          {voiceError && (
            <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded-lg text-red-600 text-xs">
              {voiceError}
            </div>
          )}
        </div>
      </div>
    );
  }

  // 常规样式：用于聊天页面底部的输入框
  return (
    <div className="w-full max-w-3xl mx-auto transition-all duration-300">
      <div className="relative w-full p-3 border border-gray-200 rounded-xl bg-white">
        <form onSubmit={handleSubmit} className="flex flex-col">
          <textarea
            ref={textareaRef}
            className="w-full min-h-[36px] p-2 px-3 text-sm resize-none box-border font-normal leading-5 border-none bg-transparent focus:outline-none transition-all duration-300 ease-in-out"
            placeholder="询问任何问题"
            value={userInput}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            rows={1}
            style={{
              height: '36px',
              transition: 'height 0.3s ease-in-out'
            }}
          />

          <div className="flex items-center gap-2 self-end mt-2">
            {/* 录音组件 - 优化版本 */}
            <VoiceRecorderOptimized
              onRecordingComplete={handleRecordingComplete}
              disabled={isLoading}
            />

            {/* TTS toggle button */}
            <button
              type="button"
              onClick={() => setIsTtsOn(!isTtsOn)}
              className={`bg-none border-none p-1.5 cursor-pointer w-9 h-9 flex items-center justify-center rounded-full transition-colors ${
                isTtsOn
                  ? 'bg-gray-800 text-white'
                  : 'text-text-secondary hover:bg-gray-100'
              }`}
              title={isTtsOn ? '关闭实时播放' : '打开实时播放'}
            >
              <SpeakerWaveIcon />
            </button>

            {/* Send button */}
            <button
              type="submit"
              disabled={!userInput.trim()}
              className={`bg-none border-none p-1.5 cursor-pointer w-9 h-9 flex items-center justify-center rounded-full transition-colors ${
                userInput.trim()
                  ? 'bg-gray-800 text-white hover:bg-gray-900'
                  : 'text-text-secondary opacity-50 cursor-not-allowed'
              }`}
              title="发送消息"
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <PaperAirplaneIcon />
              )}
            </button>
          </div>
        </form>

        {/* ASR状态显示 */}
        {asrStatus && (
          <div className={`mt-2 text-sm p-2 rounded-md transition-all duration-300 ${
            asrStatus === 'processing'
              ? 'text-blue-600 bg-blue-50 border border-blue-200'
              : asrStatus === 'success'
              ? 'text-green-600 bg-green-50 border border-green-200'
              : 'text-red-600 bg-red-50 border border-red-200'
          }`}>
            {asrStatus === 'processing' && '🎤 正在识别语音...'}
            {asrStatus === 'success' && '✅ 语音识别成功！'}
            {asrStatus === 'error' && '❌ 语音识别失败'}
          </div>
        )}

        {/* 语音错误提示 */}
        {voiceError && (
          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded-lg">
            <span className="text-sm text-red-600">🎤 {voiceError}</span>
          </div>
        )}
      </div>

      <small className="block mt-1 text-[0.65rem] text-text-secondary text-center">
        本数字人模型已接入 deepseek-R1 模型。请核查重要信息。
      </small>
    </div>
  );
};

export default InputArea; 