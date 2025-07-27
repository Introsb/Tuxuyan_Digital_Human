import React from 'react';

const WelcomePanel = ({ onSuggestionClick }) => {
  // 示例问题卡片数据
  const suggestionPrompts = [
    {
      id: 1,
      title: "控制论基础",
      question: "请介绍一下控制论的基本概念和发展历程"
    },
    {
      id: 2,
      title: "人工智能发展",
      question: "人工智能技术的发展趋势和未来展望是什么？"
    },
    {
      id: 3,
      title: "智能系统设计",
      question: "如何设计一个高效的智能控制系统？"
    },
    {
      id: 4,
      title: "学术研究方向",
      question: "北京科技大学智能科学与技术学院的主要研究方向有哪些？"
    }
  ];

  return (
    <div className="welcome-panel flex flex-col items-center justify-center h-full max-w-4xl mx-auto px-8">
      {/* 头像区域 */}
      <div className="avatar-container mb-8">
        <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100 flex items-center justify-center shadow-lg border-4 border-white">
          <div className="text-4xl">👨‍🏫</div>
        </div>
      </div>

      {/* 主标题 */}
      <h1 className="text-3xl font-bold text-gray-800 mb-4 text-center">
        涂序彦教授
      </h1>

      {/* 欢迎语 */}
      <p className="text-lg text-gray-600 mb-12 text-center max-w-2xl leading-relaxed">
        欢迎来到北京科技大学智能科学与技术学院！我是涂序彦教授的数字人模型，
        很高兴与您交流控制论、人工智能和智能系统相关的话题。
      </p>

      {/* 示例问题卡片 */}
      <div className="suggestion-prompts w-full max-w-3xl">
        <h3 className="text-sm font-medium text-gray-500 mb-4 text-center">
          您可以尝试问我这些问题：
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {suggestionPrompts.map((prompt) => (
            <button
              key={prompt.id}
              onClick={() => onSuggestionClick(prompt.question)}
              className="suggestion-card p-4 text-left bg-white border border-gray-200 rounded-xl hover:border-gray-300 hover:shadow-md transition-all duration-200 group"
            >
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center group-hover:bg-blue-100 transition-colors">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-blue-600">
                    <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>
                  </svg>
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-medium text-gray-800 mb-1 group-hover:text-gray-900">
                    {prompt.title}
                  </h4>
                  <p className="text-sm text-gray-600 line-clamp-2 group-hover:text-gray-700">
                    {prompt.question}
                  </p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* 底部提示 */}
      <div className="mt-12 text-center">
        <p className="text-sm text-gray-500">
          💡 您也可以直接在下方输入框中提出任何问题
        </p>
      </div>
    </div>
  );
};

export default WelcomePanel;
