import React, { useState } from 'react';

const ChatHeader = () => {
  const [renderKey] = useState(Date.now());
  
  // 校徽URL和样式
  const logoUrl = `https://ai.ustb.edu.cn/images/logo.png?v=${renderKey}`;
  
  const logoStyle = {
    height: '36px', // 增加校徽高度
    width: 'auto',
    objectFit: 'contain',
    filter: 'brightness(0) saturate(0%)',
    clipPath: 'inset(0 25% 0 0)', // 裁剪右侧25%
    WebkitClipPath: 'inset(0 25% 0 0)',
  };

  return (
    <div className="flex items-center justify-center p-4 w-full">
      <div
        className="flex items-center justify-center"
        style={{
          transform: 'translateX(60px)', // 向右移动60px，增加右移距离
          transition: 'transform 0.3s ease-in-out'
        }}
      >
        <img
          src={logoUrl}
          alt="USTB Logo"
          style={logoStyle}
        />
      </div>
    </div>
  );
};

export default ChatHeader;
