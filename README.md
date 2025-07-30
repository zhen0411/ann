# 视频音频标注工具 (Video Audio Annotation Tool)

一个功能完整的视频与音频标注系统，支持精细化的标注操作与项目管理。

## 功能特性

- 🎬 **视频标注**: 支持视频切分打点、时间轴拉框标注、多种标注类型
- 🎵 **音频标注**: 波形显示、分段标注、多轨道支持
- 👥 **权限管理**: 多级权限控制（管理员/项目负责人/标注员/审阅员）
- 📊 **项目管理**: 多项目支持、任务分配、进度跟踪
- 🏷️ **标签配置**: 自定义标签、模板管理、JSON配置导入导出
- ⚡ **快捷键支持**: 所有操作支持快捷键自定义
- 🔄 **审阅机制**: 标注审核、退回、评论功能

## 技术栈

- **前端**: React.js + Redux + TailwindCSS + video.js/audio.js
- **后端**: Python FastAPI
- **数据库**: PostgreSQL + Redis
- **任务队列**: Celery + Redis
- **对象存储**: MinIO
- **部署**: Docker + Docker Compose

## 快速开始

### 使用 Docker Compose 启动

```bash
# 克隆项目
git clone <repository-url>
cd video-audio-annotation-tool

# 启动所有服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端API: http://localhost:8000
# MinIO管理: http://localhost:9000
```

### 手动启动

```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 前端
cd frontend
npm install
npm start
```

## 项目结构

```
├── backend/                 # FastAPI 后端
├── frontend/               # React 前端
├── docker-compose.yml      # Docker 编排
├── nginx/                  # Nginx 配置
└── docs/                  # 文档
```

## 开发指南

详细的开发文档请参考 `docs/` 目录。