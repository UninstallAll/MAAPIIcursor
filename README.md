# 个人网站项目

这是一个使用Nest.js和Python构建的个人网站项目。

## 技术栈

- **前端**: React, TypeScript, Tailwind CSS
- **主要后端**: Nest.js (Node.js框架)
- **辅助后端**: Python Flask API
- **数据库**: MongoDB

## 项目结构

```
personal-website/
├── frontend/                # React前端应用
├── backend/                 # Nest.js后端应用
├── python-services/         # Python服务
├── docker-compose.yml       # Docker配置
└── README.md                # 项目说明
```

## 功能特点

- 响应式设计
- 博客文章管理
- 项目展示
- 联系表单
- 数据分析（Python实现）

## 安装与运行

### 前提条件

- Node.js (v16+)
- Python (v3.8+)
- Docker & Docker Compose (可选)

### 本地开发环境设置

1. 克隆仓库
```bash
git clone [仓库URL]
cd personal-website
```

2. 安装依赖并启动Nest.js后端
```bash
cd backend
npm install
npm run start:dev
```

3. 安装依赖并启动React前端
```bash
cd ../frontend
npm install
npm start
```

4. 设置Python虚拟环境并启动Python服务
```bash
cd ../python-services
python -m venv venv
source venv/bin/activate  # Windows使用: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 使用Docker

或者，您可以使用Docker Compose一键启动整个应用：

```bash
docker-compose up
```

应用将在以下地址运行：
- 前端: http://localhost:3000
- Nest.js API: http://localhost:4000
- Python API: http://localhost:5000

## 部署

本项目可部署到各种云平台：
- AWS
- Heroku
- Vercel
- Netlify (前端)

详细部署指南请参见各平台文档。 