import React, { useState, useRef, useEffect } from 'react';

// WAV格式转换函数
const convertToWav = async (audioBlob) => {
  try {
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    // 转换为16kHz单声道WAV
    const targetSampleRate = 16000;
    const targetChannels = 1;

    // 重采样到16kHz
    const resampledBuffer = audioContext.createBuffer(
      targetChannels,
      Math.floor(audioBuffer.length * targetSampleRate / audioBuffer.sampleRate),
      targetSampleRate
    );

    // 简单的重采样（线性插值）
    const sourceData = audioBuffer.getChannelData(0);
    const targetData = resampledBuffer.getChannelData(0);
    const ratio = sourceData.length / targetData.length;

    for (let i = 0; i < targetData.length; i++) {
      const sourceIndex = Math.floor(i * ratio);
      targetData[i] = sourceData[sourceIndex] || 0;
    }

    // 转换为WAV格式
    const wavBuffer = audioBufferToWav(resampledBuffer);
    return new Blob([wavBuffer], { type: 'audio/wav' });
  } catch (error) {
    console.error('WAV转换失败:', error);
    return audioBlob; // 转换失败时返回原始数据
  }
};

// 将AudioBuffer转换为WAV格式
const audioBufferToWav = (buffer) => {
  const length = buffer.length;
  const arrayBuffer = new ArrayBuffer(44 + length * 2);
  const view = new DataView(arrayBuffer);

  // WAV文件头
  const writeString = (offset, string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };

  writeString(0, 'RIFF');
  view.setUint32(4, 36 + length * 2, true);
  writeString(8, 'WAVE');
  writeString(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, buffer.sampleRate, true);
  view.setUint32(28, buffer.sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeString(36, 'data');
  view.setUint32(40, length * 2, true);

  // 写入音频数据
  const channelData = buffer.getChannelData(0);
  let offset = 44;
  for (let i = 0; i < length; i++) {
    const sample = Math.max(-1, Math.min(1, channelData[i]));
    view.setInt16(offset, sample * 0x7FFF, true);
    offset += 2;
  }

  return arrayBuffer;
};

const VoiceRecorderOptimized = ({ onRecordingComplete, disabled = false }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioLevel, setAudioLevel] = useState(0);
  const [error, setError] = useState('');

  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);
  const timerRef = useRef(null);
  const animationRef = useRef(null);

  // 格式化时间显示
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // 音量检测
  const updateAudioLevel = () => {
    if (analyserRef.current) {
      const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
      analyserRef.current.getByteFrequencyData(dataArray);
      
      const average = dataArray.reduce((sum, value) => sum + value, 0) / dataArray.length;
      const normalizedLevel = Math.min(100, (average / 255) * 100);
      setAudioLevel(normalizedLevel);
      
      if (isRecording) {
        animationRef.current = requestAnimationFrame(updateAudioLevel);
      }
    }
  };

  // 开始录音
  const startRecording = async () => {
    try {
      setError('');
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        } 
      });
      
      streamRef.current = stream;

      // 设置音频分析
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;

      // 设置MediaRecorder - 使用浏览器支持的格式，后续转换为WAV
      let mimeType;
      if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
        mimeType = 'audio/webm;codecs=opus';
      } else if (MediaRecorder.isTypeSupported('audio/webm')) {
        mimeType = 'audio/webm';
      } else if (MediaRecorder.isTypeSupported('audio/wav')) {
        mimeType = 'audio/wav';
      } else {
        mimeType = 'audio/ogg';
      }

      console.log('🎤 使用录音格式:', mimeType);

      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: mimeType
      });

      const audioChunks = [];
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: mimeType });

        console.log('🎤 录音完成，原始音频大小:', audioBlob.size, 'bytes, 格式:', mimeType);

        // 检查音频大小
        if (audioBlob.size < 1000) {
          setError('录音时间太短，请重新录音');
          setIsProcessing(false);
          return;
        }

        // 转换为WAV格式（如果不是WAV）
        let finalBlob = audioBlob;
        let fileName = 'recording.wav';

        if (!mimeType.includes('wav')) {
          console.log('🔄 转换音频格式为WAV...');
          try {
            finalBlob = await convertToWav(audioBlob);
            console.log('✅ WAV转换成功，新大小:', finalBlob.size, 'bytes');
          } catch (error) {
            console.error('❌ WAV转换失败:', error);
            // 转换失败时使用原始格式
            if (mimeType.includes('webm')) {
              fileName = 'recording.webm';
            } else {
              fileName = 'recording.ogg';
            }
            finalBlob = audioBlob;
          }
        }

        // 创建FormData
        const formData = new FormData();
        formData.append('audio_file', finalBlob, fileName);

        console.log('🎤 准备上传音频文件:', fileName, '最终大小:', finalBlob.size, 'bytes');

        // 停止所有轨道
        stream.getTracks().forEach(track => track.stop());

        // 处理录音
        setIsProcessing(true);
        try {
          await onRecordingComplete(formData);
        } catch (error) {
          console.error('🎤 录音处理错误:', error);
          setError('处理录音时出错: ' + error.message);
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
      updateAudioLevel();
      
    } catch (error) {
      console.error('录音启动失败:', error);
      setError('无法访问麦克风，请检查权限设置');
    }
  };

  // 停止录音
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      // 清理计时器
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      
      // 清理动画
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
        animationRef.current = null;
      }
      
      // 清理音频上下文
      if (audioContextRef.current) {
        audioContextRef.current.close();
        audioContextRef.current = null;
      }
      
      setAudioLevel(0);
    }
  };

  // 清理资源
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  return (
    <div className="flex items-center gap-3">
      {/* 录音按钮 - 内部布局尺寸为32px (w-8 h-8) */}
      <button
        onClick={isRecording ? stopRecording : startRecording}
        disabled={disabled || isProcessing}
        className={`
          relative flex items-center justify-center w-8 h-8 rounded-full
          transition-all duration-300 ease-in-out transform
          ${isRecording
            ? 'bg-black hover:bg-gray-800 scale-105 shadow-lg'
            : 'bg-transparent hover:bg-gray-50 border-2 border-gray-300 hover:border-gray-400'
          }
          ${disabled || isProcessing
            ? 'opacity-50 cursor-not-allowed'
            : 'cursor-pointer hover:shadow-md'
          }
          focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50
        `}
        title={isRecording ? '停止录音' : '开始录音'}
      >
        {isProcessing ? (
          <div className="w-4 h-4 border-2 border-gray-600 border-t-transparent rounded-full animate-spin"></div>
        ) : isRecording ? (
          <>
            {/* 标准麦克风图标 - 录音状态 */}
            <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C10.34 2 9 3.34 9 5V11C9 12.66 10.34 14 12 14C13.66 14 15 12.66 15 11V5C15 3.34 13.66 2 12 2ZM12 4C12.55 4 13 4.45 13 5V11C13 11.55 12.55 12 12 12C11.45 12 11 11.55 11 11V5C11 4.45 11.45 4 12 4ZM17 11C17 14.53 14.39 17.44 11 17.93V21H13C13.55 21 14 21.45 14 22C14 22.55 13.55 23 13 23H11C10.45 23 10 22.55 10 22C10 21.45 10.45 21 11 21V17.93C7.61 17.44 5 14.53 5 11H7C7 13.76 9.24 16 12 16C14.76 16 17 13.76 17 11H17Z"/>
            </svg>
            {/* 录音状态指示环 */}
            <div className="absolute inset-0 rounded-full border-2 border-white opacity-30 animate-ping"></div>
          </>
        ) : (
          /* 标准麦克风图标 - 未录音状态 */
          <svg className="w-5 h-5 text-gray-700" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C10.34 2 9 3.34 9 5V11C9 12.66 10.34 14 12 14C13.66 14 15 12.66 15 11V5C15 3.34 13.66 2 12 2ZM12 4C12.55 4 13 4.45 13 5V11C13 11.55 12.55 12 12 12C11.45 12 11 11.55 11 11V5C11 4.45 11.45 4 12 4ZM17 11C17 14.53 14.39 17.44 11 17.93V21H13C13.55 21 14 21.45 14 22C14 22.55 13.55 23 13 23H11C10.45 23 10 22.55 10 22C10 21.45 10.45 21 11 21V17.93C7.61 17.44 5 14.53 5 11H7C7 13.76 9.24 16 12 16C14.76 16 17 13.76 17 11H17Z"/>
          </svg>
        )}
      </button>

      {/* 简化的录音状态显示 - 仅在录音时显示时间 */}
      {(isRecording || isProcessing) && (
        <div className="flex items-center gap-2 px-2 py-1 bg-gray-50 rounded-md border border-gray-200">
          {/* 音量指示器 - 简化版 */}
          {isRecording && (
            <div className="w-1 h-4 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="w-full bg-red-500 rounded-full transition-all duration-100"
                style={{
                  height: `${Math.max(20, audioLevel)}%`,
                  transform: 'translateY(100%)',
                  animation: audioLevel > 20 ? 'slideUp 0.1s ease-out forwards' : 'none'
                }}
              ></div>
            </div>
          )}

          {/* 时间显示 - 简化版 */}
          <span className="text-xs font-mono text-gray-700">
            {isProcessing ? '处理中' : formatTime(recordingTime)}
          </span>
        </div>
      )}

      {/* 错误提示 */}
      {error && (
        <div className="px-3 py-2 bg-red-50 border border-red-200 rounded-lg">
          <span className="text-sm text-red-600">🎤 {error}</span>
        </div>
      )}
    </div>
  );
};

export default VoiceRecorderOptimized;
