#!/usr/bin/env python3
"""
生产环境部署脚本
构建并部署涂序彦教授数字人项目
"""

import subprocess
import time
import sys
import shutil
from pathlib import Path
import json

class ProductionDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.react_dir = self.project_root / "react-version"
        self.build_dir = self.react_dir / "build"
        
    def print_banner(self):
        """显示部署横幅"""
        print("=" * 80)
        print("🚀 涂序彦教授数字人项目 - 生产环境部署")
        print("=" * 80)
        print("🎯 部署流程:")
        print("   - 构建React生产版本")
        print("   - 优化静态资源")
        print("   - 准备部署文件")
        print("   - 提供部署选项")
        print("=" * 80)
    
    def check_prerequisites(self):
        """检查部署前提条件"""
        print("\n🔍 检查部署前提条件...")
        
        # 检查react-version目录
        if not self.react_dir.exists():
            print("❌ react-version 目录不存在")
            return False
        
        # 检查package.json
        package_json = self.react_dir / "package.json"
        if not package_json.exists():
            print("❌ package.json 不存在")
            return False
        
        # 检查node_modules
        node_modules = self.react_dir / "node_modules"
        if not node_modules.exists():
            print("⚠️  node_modules 不存在，需要先运行 npm install")
            return False
        
        print("✅ 部署前提条件检查通过")
        return True
    
    def build_production(self):
        """构建生产版本"""
        print("\n📦 构建React生产版本...")
        
        try:
            # 清理旧的构建文件
            if self.build_dir.exists():
                print("🧹 清理旧的构建文件...")
                shutil.rmtree(self.build_dir)
            
            # 运行构建命令
            print("⚙️  运行 npm run build...")
            result = subprocess.run([
                "npm", "run", "build"
            ], cwd=self.react_dir, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ React生产版本构建成功")
                
                # 检查构建结果
                if self.build_dir.exists():
                    build_size = sum(f.stat().st_size for f in self.build_dir.rglob('*') if f.is_file())
                    print(f"📊 构建大小: {build_size / 1024 / 1024:.2f} MB")
                    
                    # 列出主要文件
                    main_files = list(self.build_dir.glob("static/js/*.js"))
                    css_files = list(self.build_dir.glob("static/css/*.css"))
                    
                    print(f"📄 JavaScript文件: {len(main_files)} 个")
                    print(f"🎨 CSS文件: {len(css_files)} 个")
                    
                    return True
                else:
                    print("❌ 构建目录未生成")
                    return False
            else:
                print("❌ 构建失败")
                print(f"错误输出: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 构建超时（5分钟）")
            return False
        except Exception as e:
            print(f"❌ 构建异常: {e}")
            return False
    
    def create_deployment_package(self):
        """创建部署包"""
        print("\n📦 创建部署包...")
        
        try:
            # 创建部署目录
            deploy_dir = self.project_root / "deployment"
            if deploy_dir.exists():
                shutil.rmtree(deploy_dir)
            deploy_dir.mkdir()
            
            # 复制前端构建文件
            frontend_deploy = deploy_dir / "frontend"
            shutil.copytree(self.build_dir, frontend_deploy)
            print("✅ 前端文件已复制到部署包")
            
            # 复制后端文件
            backend_deploy = deploy_dir / "backend"
            backend_deploy.mkdir()
            
            backend_files = [
                "complete_api_server.py",
                "requirements.txt"
            ]
            
            for file_name in backend_files:
                src_file = self.project_root / file_name
                if src_file.exists():
                    shutil.copy2(src_file, backend_deploy)
                    print(f"✅ 已复制 {file_name}")
            
            # 创建部署说明
            self.create_deployment_instructions(deploy_dir)
            
            print(f"📦 部署包已创建: {deploy_dir}")
            return True
            
        except Exception as e:
            print(f"❌ 创建部署包失败: {e}")
            return False
    
    def create_deployment_instructions(self, deploy_dir):
        """创建部署说明"""
        instructions = """# 🚀 涂序彦教授数字人项目部署说明

## 📁 文件结构
```
deployment/
├── frontend/          # React构建文件
│   ├── index.html
│   ├── static/
│   └── ...
├── backend/           # Python后端文件
│   ├── complete_api_server.py
│   └── requirements.txt
└── DEPLOYMENT.md      # 本说明文件
```

## 🌐 部署选项

### 1. 静态文件服务器部署
```bash
# 使用Python内置服务器
cd deployment/frontend
python3 -m http.server 3000

# 使用Node.js serve
npx serve -s deployment/frontend -l 3000

# 使用Nginx
cp -r deployment/frontend/* /var/www/html/
```

### 2. 后端API部署
```bash
cd deployment/backend

# 安装依赖
pip install -r requirements.txt

# 启动后端
python3 complete_api_server.py
```

### 3. Docker部署
```dockerfile
# Dockerfile示例
FROM node:16-alpine AS frontend
COPY deployment/frontend /app
WORKDIR /app
EXPOSE 3000
CMD ["npx", "serve", "-s", ".", "-l", "3000"]

FROM python:3.9-slim AS backend
COPY deployment/backend /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "complete_api_server.py"]
```

### 4. 云平台部署

#### Vercel (推荐前端)
1. 上传frontend文件夹到GitHub
2. 连接Vercel到GitHub仓库
3. 自动部署

#### Railway (推荐后端)
1. 上传backend文件夹到GitHub
2. 连接Railway到GitHub仓库
3. 配置环境变量

#### Heroku
```bash
# 前端
heroku create your-app-frontend
git subtree push --prefix=deployment/frontend heroku main

# 后端
heroku create your-app-backend
git subtree push --prefix=deployment/backend heroku main
```

## ⚙️ 环境配置

### 前端环境变量
```env
REACT_APP_API_URL=https://your-backend-url.com
```

### 后端环境变量
```env
DEEPSEEK_API_KEY=your-deepseek-key
BAIDU_API_KEY=your-baidu-key
BAIDU_SECRET_KEY=your-baidu-secret
```

## 🔧 生产优化

### 前端优化
- ✅ 代码分割和懒加载
- ✅ 静态资源压缩
- ✅ 缓存策略
- ✅ CDN加速

### 后端优化
- 使用Gunicorn或uWSGI
- 配置反向代理（Nginx）
- 启用HTTPS
- 配置日志和监控

## 📊 性能监控
- 前端：Google Analytics, Sentry
- 后端：Prometheus, Grafana
- 日志：ELK Stack

## 🛡️ 安全配置
- HTTPS证书
- CORS配置
- API密钥保护
- 防火墙设置

## 📞 技术支持
如有问题，请检查：
1. 服务器日志
2. 网络连接
3. API密钥配置
4. 依赖版本兼容性
"""
        
        with open(deploy_dir / "DEPLOYMENT.md", "w", encoding="utf-8") as f:
            f.write(instructions)
        
        print("✅ 部署说明已创建")
    
    def create_docker_files(self):
        """创建Docker配置文件"""
        print("\n🐳 创建Docker配置文件...")
        
        # Dockerfile for frontend
        frontend_dockerfile = """FROM node:16-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
        
        # Dockerfile for backend
        backend_dockerfile = """FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python3", "complete_api_server.py"]
"""
        
        # docker-compose.yml
        docker_compose = """version: '3.8'
services:
  frontend:
    build: ./deployment/frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000

  backend:
    build: ./deployment/backend
    ports:
      - "8000:8000"
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - BAIDU_API_KEY=${BAIDU_API_KEY}
      - BAIDU_SECRET_KEY=${BAIDU_SECRET_KEY}
"""
        
        # 保存Docker文件
        with open("Dockerfile.frontend", "w") as f:
            f.write(frontend_dockerfile)
        
        with open("Dockerfile.backend", "w") as f:
            f.write(backend_dockerfile)
        
        with open("docker-compose.yml", "w") as f:
            f.write(docker_compose)
        
        print("✅ Docker配置文件已创建")
    
    def show_deployment_summary(self, build_success, package_success):
        """显示部署总结"""
        print("\n" + "=" * 80)
        print("📊 生产环境部署总结")
        print("=" * 80)
        
        if build_success and package_success:
            print("🎉 部署准备完成！")
            print("\n📦 已创建的文件:")
            print("   ✅ deployment/ - 部署包")
            print("   ✅ DEPLOYMENT.md - 部署说明")
            print("   ✅ docker-compose.yml - Docker配置")
            print("   ✅ Dockerfile.* - Docker镜像配置")
            
            print("\n🚀 快速部署命令:")
            print("   # 本地测试")
            print("   cd deployment/frontend && npx serve -s . -l 3000")
            print("   cd deployment/backend && python3 complete_api_server.py")
            
            print("   # Docker部署")
            print("   docker-compose up -d")
            
            print("\n🌐 推荐部署平台:")
            print("   前端: Vercel, Netlify, GitHub Pages")
            print("   后端: Railway, Heroku, DigitalOcean")
            
            return True
        else:
            print("❌ 部署准备失败")
            if not build_success:
                print("   - 构建失败，请检查代码")
            if not package_success:
                print("   - 打包失败，请检查文件权限")
            return False
    
    def deploy(self):
        """执行部署流程"""
        self.print_banner()
        
        # 1. 检查前提条件
        if not self.check_prerequisites():
            return False
        
        # 2. 构建生产版本
        build_success = self.build_production()
        
        # 3. 创建部署包
        package_success = False
        if build_success:
            package_success = self.create_deployment_package()
        
        # 4. 创建Docker文件
        if build_success:
            self.create_docker_files()
        
        # 5. 显示总结
        success = self.show_deployment_summary(build_success, package_success)
        
        return success

def main():
    """主函数"""
    deployer = ProductionDeployer()
    success = deployer.deploy()
    
    if success:
        print("\n🎯 生产环境部署准备完成！")
        print("💡 请查看 DEPLOYMENT.md 了解详细部署步骤")
    else:
        print("\n❌ 部署准备失败")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
