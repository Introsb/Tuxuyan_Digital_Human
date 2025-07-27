import React, { useState, useRef, useEffect } from 'react';

const VoiceRecorder = ({ onRecordingComplete, onError, disabled = false }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioLevel, setAudioLevel] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);
  const timerRef = useRef(null);
  const animationRef = useRef(null);

  // 清理资源
  const cleanup = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
  };

  // 组件卸载时清理
  useEffect(() => {
    return cleanup;
  }, []);

  // 音量检测
  const detectAudioLevel = () => {
    if (!analyserRef.current) return;
    
    const bufferLength = analyserRef.current.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyserRef.current.getByteFrequencyData(dataArray);
    
    // 计算平均音量
    const average = dataArray.reduce((sum, value) => sum + value, 0) / bufferLength;
    setAudioLevel(Math.min(100, (average / 255) * 100));
    
    if (isRecording) {
      animationRef.current = requestAnimationFrame(detectAudioLevel);
    }
  };

  // 开始录音
  const startRecording = async () => {
    try {
      console.log('🎤 开始录音...');
      
      // 请求麦克风权限
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        }
      });
      
      streamRef.current = stream;
      
      // 设置音频上下文用于音量检测
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;
      
      // 设置MediaRecorder
      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      const audioChunks = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };
      
      mediaRecorderRef.current.onstop = async () => {
        console.log('🎤 录音结束，处理音频数据...');
        setIsProcessing(true);
        
        try {
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
          
          // 转换为WAV格式（如果需要）
          const formData = new FormData();
          formData.append('audio_file', audioBlob, 'recording.webm');  // 明确WebM格式
          
          if (onRecordingComplete) {
            await onRecordingComplete(formData);
          }
        } catch (error) {
          console.error('处理录音数据失败:', error);
          if (onError) {
            onError('处理录音数据失败');
          }
        } finally {
          setIsProcessing(false);
        }
      };
      
      // 开始录音
      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingTime(0);
      
      // 开始计时
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      
      // 开始音量检测
      detectAudioLevel();
      
    } catch (error) {
      console.error('启动录音失败:', error);
      if (onError) {
        onError('无法访问麦克风，请检查权限设置');
      }
      cleanup();
    }
  };

  // 停止录音
  const stopRecording = () => {
    console.log('🎤 停止录音...');
    
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
    }
    
    setIsRecording(false);
    setAudioLevel(0);
    cleanup();
  };

  // 格式化时间显示
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="voice-recorder flex items-center gap-3">
      {/* 录音按钮 - 黑白双色调设计 */}
      <button
        onClick={isRecording ? stopRecording : startRecording}
        disabled={disabled || isProcessing}
        className={`
          voice-recorder-btn
          ${isRecording ? 'recording' : ''}
          ${isProcessing ? 'processing' : ''}
        `}
        title={isRecording ? '停止录音' : '开始录音'}
      >
        {isProcessing ? (
          <div className="w-4 h-4 border-2 border-gray-600 border-t-transparent rounded-full animate-spin"></div>
        ) : isRecording ? (
          <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
          </svg>
        ) : (
          <svg className="w-5 h-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24">
            <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 715 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
          </svg>
        )}

        {/* 录音状态指示环 */}
        {isRecording && (
          <div className="absolute inset-0 rounded-full border-2 border-white opacity-30 animate-ping"></div>
        )}
      </button>

      {/* 录音状态显示 - 优化黑白设计 */}
      {(isRecording || isProcessing) && (
        <div className="recording-status">
          {/* 音量指示器 */}
          {isRecording && (
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-6 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="w-full bg-black rounded-full transition-all duration-100"
                  style={{
                    height: `${Math.max(10, audioLevel)}%`,
                    transform: 'translateY(100%)',
                    animation: audioLevel > 20 ? 'slideUp 0.1s ease-out forwards' : 'none'
                  }}
                ></div>
              </div>
              <div className="flex items-center">
                <div className={`w-2 h-2 rounded-full transition-colors duration-200 ${
                  audioLevel > 20 ? 'bg-black' : audioLevel > 5 ? 'bg-gray-600' : 'bg-gray-400'
                }`}></div>
              </div>
            </div>
          )}

          {/* 时间显示 */}
          <span className="text-sm font-mono text-gray-800 font-medium">
            {isProcessing ? '处理中...' : formatTime(recordingTime)}
          </span>

          {/* 录音状态文字 */}
          <span className="text-sm text-gray-600">
            {isProcessing ? '正在处理录音...' : '正在录音...'}
          </span>

          {/* 录音波形动画 */}
          {isRecording && (
            <div className="flex items-center gap-0.5">
              {[...Array(3)].map((_, i) => (
                <div
                  key={i}
                  className="w-0.5 bg-black rounded-full animate-pulse"
                  style={{
                    height: `${8 + (audioLevel / 100) * 8 + Math.sin(Date.now() / 200 + i) * 2}px`,
                    animationDelay: `${i * 0.1}s`
                  }}
                ></div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;
