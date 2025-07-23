import React, { useState } from 'react';
import teamLogo from '../assets/team-logo.png'; // 需要拷贝assets文件夹

const Header = ({ toggleSidebar, sidebarVisible }) => {
  // 使用useState强制组件重新渲染
  const [renderKey, setRenderKey] = useState(Date.now());
  
  // 添加随机参数到URL以避免缓存
  const logoUrl = `https://ai.ustb.edu.cn/images/logo.png?v=${renderKey}`;
  
  // 使用内联样式定义剪裁
  const logoStyle = {
    height: '38px', // 与队徽保持一致的大小
    width: 'auto',
    objectFit: 'contain',
    filter: 'brightness(0) saturate(0%)',
    clipPath: 'inset(0 25% 0 0)',
    WebkitClipPath: 'inset(0 25% 0 0)', // 添加WebKit前缀以支持Safari
  };

  // 使用内联样式定义团队标志的样式，包括精确的负边距
  const teamLogoStyle = {
    height: '38px', // 与校徽保持一致的大小
    filter: 'grayscale(100%)',
    transition: 'filter 0.3s ease',
    marginLeft: '-103px', // 再向左一点点，实现更紧凑的logo组合
    position: 'relative', // 添加相对定位
    zIndex: 1, // 降低层级，避免遮挡文字
  };

  // 移除内联样式，改用CSS类

  // 强制重新渲染
  React.useEffect(() => {
    // 组件挂载后1秒强制更新一次
    const timer = setTimeout(() => setRenderKey(Date.now()), 1000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <header key={renderKey} className="main-header flex-shrink-0 text-base z-10">
      <button
        onClick={toggleSidebar}
        className={`fixed top-3.5 bg-transparent border-none text-xl cursor-pointer z-[100] text-text-secondary hover:text-text-primary transition-all duration-300 ${
          sidebarVisible ? 'left-[240px]' : 'left-[20px]'
        }`}
        title="切换侧边栏"
      >
        ☰
      </button>

      <div className="logo-container">
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

      <div className="header-title-block">
        <h1 className="header-main-title text-text-primary">涂序彦教授数字人模型</h1>
        <p className="header-subtitle text-text-secondary">井溯序焰长明科技实践团</p>
      </div>
    </header>
  );
};

export default Header; 