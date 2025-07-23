import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
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
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar isVisible={sidebarVisible} />

      {/* Main content area */}
      <main className="flex-grow flex flex-col h-screen bg-primary">
        <Header toggleSidebar={toggleSidebar} sidebarVisible={sidebarVisible} />
        
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