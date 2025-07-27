import React, { useState, useEffect } from 'react';

const BackendStatusDetector = ({ onStatusChange }) => {
  const [status, setStatus] = useState({
    isOnline: false,
    isChecking: true,
    lastChecked: null,
    error: null,
    apiInfo: null
  });

  // 检查后端状态
  const checkBackendStatus = async () => {
    try {
      setStatus(prev => ({ ...prev, isChecking: true, error: null }));

      // 检查健康状态
      const healthResponse = await fetch('http://127.0.0.1:8000/', {
        method: 'GET',
        timeout: 5000
      });

      if (healthResponse.ok) {
        const healthData = await healthResponse.json();
        
        // 检查API状态
        const apiResponse = await fetch('http://127.0.0.1:8000/api_status', {
          method: 'GET',
          timeout: 5000
        });

        let apiData = null;
        if (apiResponse.ok) {
          apiData = await apiResponse.json();
        }

        const newStatus = {
          isOnline: true,
          isChecking: false,
          lastChecked: new Date(),
          error: null,
          apiInfo: {
            version: healthData.version,
            features: healthData.features,
            deepseekAvailable: apiData?.deepseek_available || false,
            chatEnabled: apiData?.chat_enabled || false,
            speechAvailable: apiData?.speech_available || false
          }
        };

        setStatus(newStatus);
        onStatusChange && onStatusChange(newStatus);
        
        return true;
      } else {
        throw new Error(`HTTP ${healthResponse.status}`);
      }
    } catch (error) {
      const newStatus = {
        isOnline: false,
        isChecking: false,
        lastChecked: new Date(),
        error: error.message,
        apiInfo: null
      };

      setStatus(newStatus);
      onStatusChange && onStatusChange(newStatus);
      
      return false;
    }
  };

  // 组件挂载时检查状态
  useEffect(() => {
    checkBackendStatus();

    // 设置定期检查（每30秒）
    const interval = setInterval(checkBackendStatus, 30000);

    return () => clearInterval(interval);
  }, []);

  // 手动重新检查
  const handleManualCheck = () => {
    checkBackendStatus();
  };

  return {
    status,
    checkStatus: checkBackendStatus,
    manualCheck: handleManualCheck
  };
};

// 状态显示组件
export const BackendStatusIndicator = ({ status, onManualCheck }) => {
  if (status.isChecking) {
    return (
      <div className="flex items-center gap-2 text-sm text-gray-600">
        <div className="w-3 h-3 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
        <span>检测中...</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      {/* 状态指示器 */}
      <div className={`w-3 h-3 rounded-full ${
        status.isOnline ? 'bg-green-500' : 'bg-red-500'
      }`}></div>
      
      {/* 状态文字 */}
      <span className={`text-sm font-medium ${
        status.isOnline ? 'text-green-600' : 'text-red-600'
      }`}>
        {status.isOnline ? '在线' : '离线'}
      </span>

      {/* 详细信息 */}
      {status.isOnline && status.apiInfo && (
        <div className="text-xs text-gray-500">
          v{status.apiInfo.version}
        </div>
      )}

      {/* 错误信息 */}
      {!status.isOnline && status.error && (
        <div className="text-xs text-red-500" title={status.error}>
          连接失败
        </div>
      )}

      {/* 手动刷新按钮 */}
      <button
        onClick={onManualCheck}
        className="ml-1 p-1 text-gray-400 hover:text-gray-600 transition-colors"
        title="手动检查状态"
      >
        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </div>
  );
};

// 详细状态面板组件
export const BackendStatusPanel = ({ status, onManualCheck }) => {
  if (!status) return null;

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-800">后端服务状态</h3>
        <BackendStatusIndicator status={status} onManualCheck={onManualCheck} />
      </div>

      {status.isOnline && status.apiInfo ? (
        <div className="space-y-2 text-xs">
          <div className="flex justify-between">
            <span className="text-gray-600">服务版本:</span>
            <span className="font-mono">{status.apiInfo.version}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">DeepSeek API:</span>
            <span className={status.apiInfo.deepseekAvailable ? 'text-green-600' : 'text-red-600'}>
              {status.apiInfo.deepseekAvailable ? '可用' : '不可用'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">聊天功能:</span>
            <span className={status.apiInfo.chatEnabled ? 'text-green-600' : 'text-red-600'}>
              {status.apiInfo.chatEnabled ? '启用' : '禁用'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">语音功能:</span>
            <span className={status.apiInfo.speechAvailable ? 'text-green-600' : 'text-red-600'}>
              {status.apiInfo.speechAvailable ? '可用' : '不可用'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">可用功能:</span>
            <span className="font-mono text-xs">
              {status.apiInfo.features?.join(', ') || '无'}
            </span>
          </div>
        </div>
      ) : (
        <div className="text-sm text-red-600">
          <div className="mb-2">服务不可用</div>
          {status.error && (
            <div className="text-xs text-gray-500 bg-gray-50 p-2 rounded">
              错误: {status.error}
            </div>
          )}
          <div className="mt-2 text-xs text-gray-600">
            <div>可能的解决方案:</div>
            <ul className="list-disc list-inside mt-1 space-y-1">
              <li>检查后端服务是否启动</li>
              <li>确认端口8000未被占用</li>
              <li>验证API密钥配置</li>
              <li>检查网络连接</li>
            </ul>
          </div>
        </div>
      )}

      {status.lastChecked && (
        <div className="mt-3 pt-2 border-t border-gray-100 text-xs text-gray-500">
          最后检查: {status.lastChecked.toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};

export default BackendStatusDetector;
