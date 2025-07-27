import React, { useState } from 'react';
import teamLogo from '../assets/team-logo.png'; // 需要拷贝assets文件夹

const Header = ({ toggleSidebar }) => {
  // 使用useState强制组件重新渲染
  const [renderKey, setRenderKey] = useState(Date.now());
  
  // 添加随机参数到URL以避免缓存
  const logoUrl = `https://ai.ustb.edu.cn/images/logo.png?v=${renderKey}`;
  
  // 使用内联样式定义剪裁
  const logoStyle = {
    height: '25px', // 减小高度
    width: 'auto',
    objectFit: 'contain',
    filter: 'brightness(0) saturate(0%)',
    clipPath: 'inset(0 25% 0 0)',
    WebkitClipPath: 'inset(0 25% 0 0)', // 添加WebKit前缀以支持Safari
  };
  
  // 使用内联样式定义团队标志的样式，包括精确的负边距
  const teamLogoStyle = {
    height: '35px', // 减小高度
    filter: 'grayscale(100%)',
    transition: 'filter 0.3s ease',
    marginLeft: '-88px', // 精确的像素级调整，相当于-ml-24
    position: 'relative', // 添加相对定位
    zIndex: 2, // 确保在上层
  };

  // 标题区域的样式，使用更强的定位
  const titleBlockStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    gap: '2px',
    marginLeft: '-45px', // 增加负边距
    position: 'relative', // 添加相对定位
    zIndex: 1, // 确保在下层
  };

  // 强制重新渲染
  React.useEffect(() => {
    // 组件挂载后1秒强制更新一次
    const timer = setTimeout(() => setRenderKey(Date.now()), 1000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <header key={renderKey} className="h-[50px] flex-shrink-0 flex items-center justify-center gap-0 px-4 text-base z-10">
      <button 
        onClick={toggleSidebar} 
        className="fixed top-3.5 left-[196px] bg-transparent border-none text-xl cursor-pointer z-[100] text-text-secondary hover:text-text-primary transition-colors"
        title="切换侧边栏"
      >
        ☰
      </button>
      
      <div className="flex items-center gap-0">
        <img 
          src={logoUrl} 
          alt="USTB Logo" 
          style={logoStyle}
        />
        <img 
          src={`${teamLogo}?v=${renderKey}`}
          alt="实践团徽" 
          style={teamLogoStyle}
          onMouseOver={(e) => e.target.style.filter = 'grayscale(0%)'}
          onMouseOut={(e) => e.target.style.filter = 'grayscale(100%)'}
        />
      </div>
      
      <div style={titleBlockStyle}>
        <h1 className="text-base font-extrabold m-0 text-text-primary leading-none">涂序彦教授数字人模型</h1>
        <p className="text-xs text-text-secondary m-0 font-normal">井溯序焰长明科技实践团</p>
      </div>
    </header>
  );
};

export default Header; 