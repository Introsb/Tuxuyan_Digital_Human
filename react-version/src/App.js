import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';

const App = () => {
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const [messages, setMessages] = useState([]);
  const [isWelcomingState, setIsWelcomingState] = useState(true);
  
  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  const addMessage = (message) => {
    console.log("App.js - 添加消息:", message);
    console.log("App.js - 当前消息列表长度:", messages.length);

    setMessages(prevMessages => {
      const newMessages = [...prevMessages, message];
      console.log("App.js - 新消息列表长度:", newMessages.length);
      return newMessages;
    });

    if (isWelcomingState) {
      setIsWelcomingState(false);
    }
  };

  // 新增：更新现有消息的函数
  const updateMessage = (updatedMessage) => {
    console.log("App.js - 更新消息:", updatedMessage);

    setMessages(prevMessages => {
      const messageIndex = prevMessages.findIndex(msg => msg.id === updatedMessage.id);
      if (messageIndex !== -1) {
        // 找到消息，更新它
        const newMessages = [...prevMessages];
        newMessages[messageIndex] = updatedMessage;
        console.log("App.js - 消息已更新，索引:", messageIndex);
        return newMessages;
      } else {
        // 没找到消息，添加新消息
        console.log("App.js - 消息不存在，添加新消息");
        return [...prevMessages, updatedMessage];
      }
    });
  };

  return (
    <div
      className="h-screen grid transition-all duration-300 ease-out"
      style={{
        gridTemplateColumns: sidebarVisible ? '260px 1fr' : '35px 1fr',
        '--sidebar-width': sidebarVisible ? '260px' : '35px'
      }}
    >
      {/* Sidebar */}
      <Sidebar isVisible={sidebarVisible} toggleSidebar={toggleSidebar} />

      {/* Main content area - 使用 Grid 自动占据剩余空间 */}
      <main className="bg-gray-100 overflow-hidden">
        <ChatArea
          isWelcoming={isWelcomingState}
          messages={messages}
          addMessage={addMessage}
          updateMessage={updateMessage}
        />
      </main>
    </div>
  );
};

export default App; 