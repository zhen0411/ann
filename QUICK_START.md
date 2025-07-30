# 视频音频标注工具 - 快速开始

## 🚀 快速启动

### 方法一：使用Docker（推荐）

```bash
# 1. 安装Docker
./install-docker.sh

# 2. 启动服务
./start.sh
```

### 方法二：本地开发环境

```bash
# 1. 设置演示环境
./demo-setup.sh

# 2. 启动服务
./demo-start.sh
```

## 📋 访问地址

- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **MinIO管理**: http://localhost:9001 (用户名/密码: minioadmin/minioadmin)

## 👤 默认用户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| annotator | annotator123 | 标注员 |
| reviewer | reviewer123 | 审阅员 |
| project_manager | manager123 | 项目经理 |

## 🛠️ 功能特性

### 视频标注
- ✅ 视频播放控制（播放、暂停、快进、慢放）
- ✅ 时间轴打点切分
- ✅ 矩形框标注
- ✅ 多种标注类型支持
- ✅ 快捷键操作

### 音频标注
- ✅ 波形显示
- ✅ 分段标注
- ✅ 多轨道支持
- ✅ 音频播放控制

### 项目管理
- ✅ 多项目管理
- ✅ 用户权限管理
- ✅ 标签配置
- ✅ 进度跟踪

### 系统功能
- ✅ 用户认证
- ✅ 文件上传
- ✅ 标注审阅
- ✅ 数据导出

## 📁 项目结构

```
video-audio-annotation-tool/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── schemas/        # 数据模型
│   │   ├── services/       # 业务服务
│   │   └── tasks/          # 异步任务
│   ├── main.py             # 应用入口
│   └── requirements.txt    # Python依赖
├── frontend/               # React 前端
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   ├── store/          # Redux状态管理
│   │   └── services/       # API服务
│   ├── package.json        # Node.js依赖
│   └── public/             # 静态资源
├── docker-compose.yml      # Docker编排
├── start.sh               # 启动脚本
└── README.md              # 项目说明
```

## 🔧 开发指南

### 后端开发

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端开发

```bash
cd frontend
npm install
npm start
```

### 数据库管理

```bash
# 进入数据库容器
docker-compose exec postgres psql -U annotation_user -d annotation_db

# 备份数据库
docker-compose exec postgres pg_dump -U annotation_user annotation_db > backup.sql
```

## 🐛 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 检查端口占用
   netstat -tulpn | grep :3000
   ```

2. **服务启动失败**
   ```bash
   # 查看日志
   docker-compose logs -f
   ```

3. **数据库连接失败**
   ```bash
   # 检查数据库状态
   docker-compose ps
   ```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📚 技术栈

### 后端
- **FastAPI**: 现代Python Web框架
- **SQLAlchemy**: ORM数据库操作
- **PostgreSQL**: 主数据库
- **Redis**: 缓存和任务队列
- **Celery**: 异步任务处理
- **MinIO**: 对象存储
- **FFmpeg**: 媒体处理

### 前端
- **React**: 用户界面框架
- **Redux Toolkit**: 状态管理
- **TailwindCSS**: 样式框架
- **Video.js**: 视频播放器
- **WaveSurfer.js**: 音频波形

### 部署
- **Docker**: 容器化部署
- **Docker Compose**: 多服务编排
- **Nginx**: 反向代理

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如果您遇到问题或有建议，请：

1. 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 获取详细部署信息
2. 提交 Issue 到项目仓库
3. 联系项目维护者

---

**🎉 感谢使用视频音频标注工具！**