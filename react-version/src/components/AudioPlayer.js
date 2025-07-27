import React, { useState, useRef, useEffect } from 'react';

const AudioPlayer = ({ text, isTtsOn = false, autoPlay = false }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isAudioReady, setIsAudioReady] = useState(false);

  const audioRef = useRef(null);

  // 生成音频
  const generateAudio = async () => {
    if (audioUrl && isAudioReady) return audioUrl; // 如果已有音频且准备就绪，直接返回

    try {
      setIsLoading(true);
      setError(null);
      setIsAudioReady(false);

      console.log('🔊 开始TTS合成...');

      // 调用TTS API
      const response = await fetch('http://127.0.0.1:8000/tts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          voice: 'zh-CN-male',
          speed: 6,  // 适中的语速，平衡速度和清晰度
          pitch: 6,  // 稍高的音调，增加权威感
          volume: 5  // 正常音频
        }),
      });

      if (!response.ok) {
        throw new Error(`TTS服务错误: ${response.status}`);
      }

      // 获取音频数据
      const audioBlob = await response.blob();
      const newAudioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(newAudioUrl);

      console.log('✅ TTS合成完成');
      return newAudioUrl;

    } catch (err) {
      console.error('TTS合成失败:', err);
      setError(err.message);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  // 播放/暂停切换
  const togglePlayPause = async () => {
    if (isLoading) return;

    try {
      // 如果没有音频，先生成
      if (!audioUrl || !isAudioReady) {
        const url = await generateAudio();
        if (!url || !audioRef.current) return;

        // 设置音频源并准备播放
        audioRef.current.src = url;
        setIsAudioReady(true);
      }

      if (!audioRef.current) return;

      if (isPlaying) {
        // 暂停播放
        audioRef.current.pause();
        setIsPlaying(false);
      } else {
        // 继续播放（从当前位置）
        audioRef.current.play();
        setIsPlaying(true);
      }

    } catch (err) {
      console.error('音频播放失败:', err);
      setError(err.message);
    }
  };

  // 重新播放（从头开始）
  const replayAudio = async () => {
    if (isLoading) return;

    try {
      // 如果没有音频，先生成
      if (!audioUrl || !isAudioReady) {
        const url = await generateAudio();
        if (!url || !audioRef.current) return;

        audioRef.current.src = url;
        setIsAudioReady(true);
      }

      if (!audioRef.current) return;

      // 重置到开头并播放
      audioRef.current.currentTime = 0;
      audioRef.current.play();
      setIsPlaying(true);

    } catch (err) {
      console.error('音频重播失败:', err);
      setError(err.message);
    }
  };

  // 音频事件处理
  const handleAudioEnd = () => {
    setIsPlaying(false);
    setCurrentTime(0);
  };

  const handleAudioError = () => {
    setIsPlaying(false);
    setError('音频播放失败');
    setIsAudioReady(false);
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
      setIsAudioReady(true);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleCanPlay = () => {
    setIsAudioReady(true);
  };

  // 自动播放逻辑
  useEffect(() => {
    if (autoPlay && isTtsOn && text && !isPlaying && !isLoading) {
      const timer = setTimeout(() => {
        togglePlayPause();
      }, 500); // 延迟500ms开始播放

      return () => clearTimeout(timer);
    }
  }, [autoPlay, isTtsOn, text]);

  // 格式化时间显示
  const formatTime = (time) => {
    if (isNaN(time)) return '0:00';
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="audio-player flex items-center gap-2 mt-2">
      <audio
        ref={audioRef}
        onEnded={handleAudioEnd}
        onError={handleAudioError}
        onLoadedMetadata={handleLoadedMetadata}
        onTimeUpdate={handleTimeUpdate}
        onCanPlay={handleCanPlay}
        style={{ display: 'none' }}
      />

      {/* 主播放/暂停按钮 */}
      <button
        onClick={togglePlayPause}
        disabled={isLoading}
        className={`
          flex items-center justify-center w-8 h-8 rounded-full
          transition-all duration-200 ease-in-out
          ${isLoading
            ? 'bg-blue-100 cursor-wait text-blue-500'
            : isPlaying
            ? 'bg-blue-100 hover:bg-blue-200 text-blue-600'
            : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
          }
        `}
        title={
          isLoading
            ? '生成中...'
            : isPlaying
            ? '暂停播放'
            : (audioUrl && isAudioReady)
            ? '继续播放'
            : '播放语音'
        }
      >
        {isLoading ? (
          // 加载动画
          <div className="w-3 h-3 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        ) : isPlaying ? (
          // 暂停图标
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        ) : (audioUrl && isAudioReady) ? (
          // 播放图标（继续播放）
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
          </svg>
        ) : (
          // 扬声器图标（首次播放）
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.617.824L4.5 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.5l3.883-3.824a1 1 0 011.617.824zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 11-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.983 5.983 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.984 3.984 0 00-1.172-2.828 1 1 0 010-1.415z" clipRule="evenodd" />
          </svg>
        )}
      </button>

      {/* 重播按钮 - 只在有音频时显示 */}
      {(audioUrl && isAudioReady) && (
        <button
          onClick={replayAudio}
          disabled={isLoading}
          className="flex items-center justify-center w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-600 transition-all duration-200 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
          title="重新播放"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
          </svg>
        </button>
      )}

      {/* 错误提示 - 只在出错时显示 */}
      {error && (
        <span className="text-xs text-red-500 ml-1" title={error}>
          ⚠️
        </span>
      )}
    </div>
  );
};

export default AudioPlayer;
