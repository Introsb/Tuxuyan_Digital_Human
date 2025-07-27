import React from 'react';

const Sidebar = ({ isVisible, toggleSidebar }) => {
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

  // 调试信息
  console.log("Sidebar isVisible:", isVisible);

  return (
    <>
      {/* 侧边栏主体 - 展开状态或超窄矩形条状态 */}
      <aside
        className={`${isVisible ? 'w-[260px]' : 'w-[35px]'}
          sidebar-container flex-shrink-0 transition-all ease-in-out duration-300 min-h-screen bg-gray-100 relative`}
        style={{
          width: isVisible ? '260px' : '35px',
          minWidth: isVisible ? '260px' : '35px',
          maxWidth: isVisible ? '260px' : '35px'
        }}
      >
        {isVisible ? (
          <div className="flex flex-col h-full min-h-screen">
            {/* 顶部区域 - 汉堡按钮和标题 */}
            <div className="px-5 pt-4 pb-3 border-b border-border/30">
              {/* 汉堡菜单按钮 - 侧边栏内部 */}
              <div className="flex items-center justify-between mb-4">
                <div className="text-sm font-semibold text-text-primary tracking-wide">
                  对话历史
                </div>
                <button
                  onClick={toggleSidebar}
                  className="group relative bg-white hover:bg-gray-50 border border-gray-200 hover:border-gray-300 shadow-sm hover:shadow-md text-gray-600 hover:text-gray-800 transition-all duration-300 rounded-lg w-9 h-9 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                  title="收起侧边栏"
                >
                  {/* 汉堡菜单图标 - 展开状态显示X */}
                  <div className="hamburger-icon w-4 h-4 flex flex-col justify-center items-center space-y-1">
                    <span className="hamburger-line block w-4 h-0.5 bg-current transform transition-all duration-300 rotate-45 translate-y-1.5"></span>
                    <span className="hamburger-line block w-4 h-0.5 bg-current transform transition-all duration-300 opacity-0"></span>
                    <span className="hamburger-line block w-4 h-0.5 bg-current transform transition-all duration-300 -rotate-45 -translate-y-1.5"></span>
                  </div>
                </button>
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
                    className={`chat-history-item relative py-3 px-3 rounded-lg cursor-pointer text-sm transition-all duration-200 group
                      ${chat.isActive
                        ? 'bg-gray-100 text-gray-900 font-medium'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                  >
                    <div className="flex items-center">
                      <div className="truncate flex-1" title={chat.title}>
                        {truncateText(chat.title)}
                      </div>
                    </div>
                  </li>
                ))}
              </ul>

              {/* 空状态提示 */}
              {chatHistory.length === 0 && (
                <div className="text-center py-12 text-text-secondary">
                  <div className="text-sm">暂无对话历史</div>
                  <div className="text-xs mt-1">开始新对话来创建历史记录</div>
                </div>
              )}
            </div>
          </div>

          {/* 底部区域 - 简化信息 */}
          <div className="px-4 py-4 border-t border-border/30 mt-auto">
            <div className="text-xs text-text-secondary text-center">
              <div>涂序彦教授数字人模型</div>
              <div className="mt-0.5 opacity-70">井溯序焰长明科技实践团</div>
            </div>
          </div>
        </div>
        ) : (
          /* 收起状态 - 紧凑的汉堡菜单按钮 */
          <div className="flex flex-col h-full min-h-screen items-center pt-4">
            <button
              onClick={toggleSidebar}
              className="group relative bg-white hover:bg-gray-50 border border-gray-200 hover:border-gray-300 shadow-sm hover:shadow-md text-gray-600 hover:text-gray-800 transition-all duration-300 rounded-md w-7 h-7 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
              title="展开侧边栏"
            >
              {/* 汉堡菜单图标 - 收起状态显示三条线 */}
              <div className="hamburger-icon w-3 h-3 flex flex-col justify-center items-center space-y-0.5">
                <span className="hamburger-line block w-3 h-0.5 bg-current transform transition-all duration-300"></span>
                <span className="hamburger-line block w-3 h-0.5 bg-current transform transition-all duration-300"></span>
                <span className="hamburger-line block w-3 h-0.5 bg-current transform transition-all duration-300"></span>
              </div>
            </button>
          </div>
        )}
      </aside>
    </>
  );
};

export default Sidebar;