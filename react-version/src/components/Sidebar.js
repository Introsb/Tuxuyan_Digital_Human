import React from 'react';

const Sidebar = ({ isVisible }) => {
  // 模拟聊天历史 - 添加文本截断处理
  const chatHistory = [
    { id: 1, title: '北京科技大学智能科学与技术学院', isActive: false },
    { id: 2, title: '数字人项目定位与安排', isActive: true },
    { id: 3, title: '人工智能发展趋势', isActive: false },
    { id: 4, title: '控制论基础理论', isActive: false },
    { id: 5, title: '深度学习算法原理与实践应用研究', isActive: false },
    { id: 6, title: '机器学习在自然语言处理中的应用', isActive: false },
  ];

  // 文本截断函数
  const truncateText = (text, maxLength = 22) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <aside className={`${isVisible ? 'w-[260px]' : 'w-0 p-0 overflow-hidden transform -translate-x-full'}
      sidebar-container flex-shrink-0 transition-all ease-in-out duration-300 min-h-screen`}>
      {isVisible && (
        <div className="flex flex-col h-full min-h-screen">
          {/* 顶部区域 - 标题和新建按钮 */}
          <div className="px-5 pt-6 pb-3 border-b border-border/30">
            <div className="text-sm font-semibold text-text-primary tracking-wide mb-4">
              对话历史
            </div>

            <button className="sidebar-new-chat-btn w-full py-2.5 px-4 text-text-primary rounded-xl flex items-center justify-center gap-3 text-sm font-medium group">
              <span className="plus-icon text-text-secondary text-lg group-hover:text-text-primary transition-colors">＋</span>
              <span>新建对话</span>
            </button>
          </div>

          {/* 中间区域 - 聊天历史列表 */}
          <div className="flex-1 px-4 py-2 overflow-hidden">
            <div className="chat-history-container h-full overflow-y-auto sidebar-scroll">
              <ul className="space-y-0.5 list-none p-0 m-0">
                {chatHistory.map((chat) => (
                  <li
                    key={chat.id}
                    className={`chat-history-item relative py-1.5 px-3 rounded-lg cursor-pointer text-sm text-text-primary group
                      ${chat.isActive
                        ? 'active bg-tertiary font-semibold shadow-sm'
                        : 'hover:bg-tertiary/70 hover:shadow-sm'
                      }`}
                  >
                    <div className="truncate group-hover:text-text-primary" title={chat.title}>
                      {truncateText(chat.title)}
                    </div>
                  </li>
                ))}
              </ul>

              {/* 空状态提示 */}
              {chatHistory.length === 0 && (
                <div className="text-center py-12 text-text-secondary">
                  <div className="text-2xl mb-2">💬</div>
                  <div className="text-sm">暂无对话历史</div>
                  <div className="text-xs mt-1">开始新对话来创建历史记录</div>
                </div>
              )}
            </div>
          </div>

          {/* 底部区域 - 数字人模型展示 */}
          <div className="px-4 py-4 border-t border-border/30 mt-auto">
            <div className="text-xs font-medium text-text-secondary mb-2 tracking-wide">
              AI 助手
            </div>
            <div className="digital-human-area w-full aspect-[9/16] max-h-[280px] rounded-2xl flex flex-col justify-start items-center text-text-secondary pt-8">
              <div className="text-4xl mb-3">🤖</div>
              <div className="digital-human-status text-sm font-medium text-text-primary">涂序彦教授</div>
              <div className="digital-human-status text-xs mt-1 text-center px-3">
                人工智能领域专家
              </div>
              <div className="status-indicator w-2 h-2 bg-green-400 rounded-full mt-4"></div>
            </div>

            {/* 底部信息 */}
            <div className="mt-3 pt-3">
              <div className="sidebar-divider mb-3"></div>
              <div className="text-xs text-text-secondary text-center">
                <div>智能对话系统 v3.0</div>
                <div className="mt-0.5 opacity-70">基于 DeepSeek API</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;