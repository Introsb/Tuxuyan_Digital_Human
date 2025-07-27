import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import AudioPlayer from './AudioPlayer';

const MessageList = ({ messages, isTtsOn = false, onRetryMessage }) => {
  console.log("MessageList - 渲染消息列表，消息数量:", messages.length);
  console.log("MessageList - 消息列表:", messages);

  if (!messages.length) return null;

  return (
    <div className="flex flex-col gap-6 w-full py-6">
      {messages.map((message, index) => {
        console.log(`MessageList - 渲染消息 ${index}:`, message);
        return (
          <div
            key={message.id}
            className={`flex w-full max-w-3xl mx-auto ${
              message.sender === 'user'
                ? 'justify-end'
                : 'justify-center'
            }`}
          >
          {message.sender === 'user' ? (
            // 用户消息
            <div className="self-end max-w-[65%] mr-0">
              <div className="user-message-bubble">
                {message.text}
              </div>
            </div>
          ) : (
            // AI消息
            <div className="w-full max-w-[85%]">
              {/* 思考状态显示 - 气泡包裹效果 */}
              {message.isThinking ? (
                <div className="thinking-bubble-wrapper mb-3">
                  <div className="thinking-bubble flex items-center gap-2">
                    <div className="thinking-dots">
                      <span className="dot"></span>
                      <span className="dot"></span>
                      <span className="dot"></span>
                    </div>
                    <span className="thinking-text">正在思考...</span>
                  </div>
                </div>
              ) : null}

              {/* 完成状态显示 - 气泡包裹效果 */}
              {message.isCompleted && message.duration ? (
                <div className="completion-bubble-wrapper mb-3">
                  <div className="completion-bubble">
                    <span className="completion-text">思考完成，用时 {message.duration} 秒</span>
                  </div>
                </div>
              ) : null}

              {/* AI消息内容 */}
              {!message.isThinking ? (
                <div className={`ai-message-content bg-transparent text-text-primary w-full ${message.isTyping ? 'typing-cursor' : ''}`}>
                  <ReactMarkdown
                  components={{
                    // 代码块处理
                    code({node, inline, className, children, ...props}) {
                      const match = /language-(\w+)/.exec(className || '');
                      return !inline && match ? (
                        <SyntaxHighlighter
                          style={tomorrow}
                          language={match[1]}
                          PreTag="div"
                          {...props}
                        >
                          {String(children).replace(/\n$/, '')}
                        </SyntaxHighlighter>
                      ) : (
                        <code className="inline-code" {...props}>
                          {children}
                        </code>
                      );
                    },
                    // 段落处理
                    p({children}) {
                      return <p className="markdown-paragraph">{children}</p>;
                    },
                    // 标题处理 - 统一字体系列，添加分界线
                    h1({children}) {
                      return (
                        <div className="markdown-h1-container">
                          <h1 className="markdown-h1">{children}</h1>
                          <div className="markdown-h1-divider"></div>
                        </div>
                      );
                    },
                    h2({children}) {
                      return (
                        <div className="markdown-h2-container">
                          <h2 className="markdown-h2">{children}</h2>
                          <div className="markdown-h2-divider"></div>
                        </div>
                      );
                    },
                    h3({children}) {
                      return <h3 className="markdown-h3">{children}</h3>;
                    },
                    h4({children}) {
                      return <h4 className="markdown-h4">{children}</h4>;
                    },
                    h5({children}) {
                      return <h5 className="markdown-h5">{children}</h5>;
                    },
                    h6({children}) {
                      return <h6 className="markdown-h6">{children}</h6>;
                    },
                    // 列表处理 - 修复序号问题
                    ul({children}) {
                      return <ul className="markdown-ul">{children}</ul>;
                    },
                    ol({children, start}) {
                      return <ol className="markdown-ol" start={start}>{children}</ol>;
                    },
                    li({children, index, ordered}) {
                      return <li className="markdown-li">{children}</li>;
                    },
                    // 引用块处理
                    blockquote({children}) {
                      return <blockquote className="markdown-blockquote">{children}</blockquote>;
                    },
                    // 加粗文本处理 - 保持加粗效果
                    strong({children}) {
                      return <strong className="markdown-strong">{children}</strong>;
                    },
                    // 斜体文本处理
                    em({children}) {
                      return <em className="markdown-em">{children}</em>;
                    },
                    // 链接处理
                    a({href, children}) {
                      return <a className="markdown-link" href={href} target="_blank" rel="noopener noreferrer">{children}</a>;
                    },
                    // 分隔线处理
                    hr() {
                      return <hr className="markdown-hr" />;
                    }
                  }}
                >
                  {message.text}
                </ReactMarkdown>

                {/* 重试按钮 - 只在错误消息且可重试时显示 */}
                {message.isError && message.canRetry && onRetryMessage && (
                  <div className="mt-3 flex justify-center">
                    <button
                      onClick={() => onRetryMessage(message.originalPrompt)}
                      className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200 text-sm font-medium"
                    >
                      重试发送
                    </button>
                  </div>
                )}

                {/* 音频播放器 - 只在AI消息完成时显示 */}
                {!message.isThinking && message.text && !message.isError && (
                  <AudioPlayer
                    text={message.text}
                    isTtsOn={isTtsOn}
                    autoPlay={message.isNew && isTtsOn} // 新消息且TTS开启时自动播放
                  />
                )}
                </div>
              ) : null}
            </div>
          )}
          </div>
        );
      })}
    </div>
  );
};

export default MessageList; 