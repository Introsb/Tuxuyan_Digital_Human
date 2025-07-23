import React, { useState, useRef } from 'react';
import { MicrophoneIcon, SpeakerWaveIcon, PaperAirplaneIcon } from './Icons';

const InputArea = ({ onSendMessage, isTtsOn, setIsTtsOn, isWelcoming, inlineStyle }) => {
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedInput = userInput.trim();
    
    if (!trimmedInput || isLoading) return;
    
    setIsLoading(true);
    await onSendMessage(trimmedInput);
    setUserInput('');
    setIsLoading(false);
    
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };
  
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 250)}px`;
    }
  };
  
  const handleInputChange = (e) => {
    setUserInput(e.target.value);
    adjustTextareaHeight();
  };

  // 内联样式：用于欢迎页面中的输入框
  if (inlineStyle) {
    return (
      <div className="w-full transition-all duration-300">
        <div className="relative w-full p-3 border border-border rounded-3xl bg-primary shadow-sm">
          <form onSubmit={handleSubmit} className="flex flex-col">
            <textarea
              ref={textareaRef}
              className="w-full min-h-[32px] max-h-[250px] p-1.5 px-4 text-base resize-none box-border font-normal leading-6 border-none bg-transparent focus:outline-none"
              placeholder="询问任何问题"
              value={userInput}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              rows={1}
            />
            
            <div className="flex items-center gap-2 self-end mt-2">
              {/* Voice input button */}
              <button 
                type="button" 
                className="bg-none border-none p-1.5 cursor-pointer text-text-secondary w-9 h-9 flex items-center justify-center rounded-lg hover:bg-tertiary transition-colors"
                title="语音输入"
              >
                <MicrophoneIcon />
              </button>
              
              {/* TTS toggle button */}
              <button
                type="button"
                onClick={() => setIsTtsOn(!isTtsOn)}
                className={`bg-none border-none p-1.5 cursor-pointer w-9 h-9 flex items-center justify-center rounded-full transition-colors ${
                  isTtsOn 
                    ? 'bg-text-primary text-white' 
                    : 'text-text-secondary hover:bg-tertiary'
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
                    ? 'bg-text-primary text-white hover:bg-black' 
                    : 'text-text-secondary opacity-50 cursor-not-allowed'
                }`}
                title="发送消息"
              >
                {isLoading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <PaperAirplaneIcon />
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  // 常规样式：用于聊天页面底部的输入框
  return (
    <div className="w-full py-4 bg-primary border-t border-transparent z-10 transition-all duration-300">
      <div className="relative max-w-3xl mx-auto p-3 border border-border rounded-3xl bg-primary shadow-sm">
        <form onSubmit={handleSubmit} className="flex flex-col">
          <textarea
            ref={textareaRef}
            className="w-full min-h-[32px] max-h-[250px] p-1.5 px-4 text-base resize-none box-border font-normal leading-6 border-none bg-transparent focus:outline-none"
            placeholder="询问任何问题"
            value={userInput}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            rows={1}
          />
          
          <div className="flex items-center gap-2 self-end mt-2">
            {/* Voice input button */}
            <button 
              type="button" 
              className="bg-none border-none p-1.5 cursor-pointer text-text-secondary w-9 h-9 flex items-center justify-center rounded-lg hover:bg-tertiary transition-colors"
              title="语音输入"
            >
              <MicrophoneIcon />
            </button>
            
            {/* TTS toggle button */}
            <button
              type="button"
              onClick={() => setIsTtsOn(!isTtsOn)}
              className={`bg-none border-none p-1.5 cursor-pointer w-9 h-9 flex items-center justify-center rounded-full transition-colors ${
                isTtsOn 
                  ? 'bg-text-primary text-white' 
                  : 'text-text-secondary hover:bg-tertiary'
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
                  ? 'bg-text-primary text-white hover:bg-black' 
                  : 'text-text-secondary opacity-50 cursor-not-allowed'
              }`}
              title="发送消息"
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <PaperAirplaneIcon />
              )}
            </button>
          </div>
        </form>
      </div>
      
      <small className="block mt-1 text-[0.65rem] text-text-secondary text-center">
        本数字人模型已接入 deepseek-R1 模型。请核查重要信息。
      </small>
    </div>
  );
};

export default InputArea; 