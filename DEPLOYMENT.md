# 视频音频标注工具 - Docker 部署指南

## 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 4GB RAM
- 至少 10GB 可用磁盘空间

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd video-audio-annotation-tool
```

### 2. 启动服务

```bash
# 使用启动脚本（推荐）
./start.sh

# 或手动启动
docker-compose up -d
```

### 3. 访问应用

- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **MinIO管理**: http://localhost:9001 (用户名/密码: minioadmin/minioadmin)

### 4. 默认用户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| annotator | annotator123 | 标注员 |
| reviewer | reviewer123 | 审阅员 |
| project_manager | manager123 | 项目经理 |

## 服务架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Celery        │    │   Redis         │
                       │   (Worker)      │◄──►│   (Cache)       │
                       │   Port: -       │    │   Port: 6379    │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   MinIO         │
                       │   (Storage)     │
                       │   Port: 9000    │
                       └─────────────────┘
```

## 详细配置

### 环境变量

创建 `.env` 文件来自定义配置：

```bash
# 数据库配置
DATABASE_URL=postgresql://annotation_user:annotation_password@postgres:5432/annotation_db

# Redis配置
REDIS_URL=redis://redis:6379

# JWT配置
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MinIO配置
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=annotation-media

# 文件上传配置
MAX_FILE_SIZE=104857600  # 100MB
```

### 端口映射

| 服务 | 内部端口 | 外部端口 | 说明 |
|------|----------|----------|------|
| Frontend | 3000 | 3000 | React应用 |
| Backend | 8000 | 8000 | FastAPI后端 |
| PostgreSQL | 5432 | 5432 | 数据库 |
| Redis | 6379 | 6379 | 缓存 |
| MinIO | 9000 | 9000 | 对象存储 |
| MinIO Console | 9001 | 9001 | MinIO管理界面 |

## 管理命令

### 启动服务

```bash
# 后台启动
docker-compose up -d

# 前台启动（查看日志）
docker-compose up
```

### 停止服务

```bash
# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec postgres psql -U annotation_user -d annotation_db
```

## 数据备份

### 备份数据库

```bash
docker-compose exec postgres pg_dump -U annotation_user annotation_db > backup.sql
```

### 恢复数据库

```bash
docker-compose exec -T postgres psql -U annotation_user annotation_db < backup.sql
```

### 备份MinIO数据

```bash
# 备份MinIO数据目录
docker cp annotation_minio:/data ./minio_backup
```

## 性能优化

### 增加资源限制

在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### 优化数据库

```yaml
services:
  postgres:
    environment:
      POSTGRES_DB: annotation_db
      POSTGRES_USER: annotation_user
      POSTGRES_PASSWORD: annotation_password
      # 性能优化参数
      POSTGRES_SHARED_BUFFERS: 256MB
      POSTGRES_EFFECTIVE_CACHE_SIZE: 1GB
      POSTGRES_WORK_MEM: 4MB
```

## 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 检查端口占用
   netstat -tulpn | grep :3000
   
   # 修改docker-compose.yml中的端口映射
   ports:
     - "3001:3000"  # 改为3001端口
   ```

2. **内存不足**
   ```bash
   # 增加Docker内存限制
   # 在Docker Desktop设置中增加内存限制
   ```

3. **磁盘空间不足**
   ```bash
   # 清理Docker缓存
   docker system prune -a
   
   # 清理数据卷
   docker volume prune
   ```

4. **服务启动失败**
   ```bash
   # 查看详细日志
   docker-compose logs backend
   
   # 重新构建镜像
   docker-compose build --no-cache
   ```

### 日志分析

```bash
# 查看错误日志
docker-compose logs | grep ERROR

# 查看特定时间段的日志
docker-compose logs --since="2024-01-01T00:00:00"
```

## 生产环境部署

### 安全配置

1. **修改默认密码**
   ```bash
   # 修改数据库密码
   # 修改MinIO密码
   # 修改JWT密钥
   ```

2. **启用HTTPS**
   ```bash
   # 配置SSL证书
   # 修改nginx配置
   ```

3. **防火墙配置**
   ```bash
   # 只开放必要端口
   ufw allow 80
   ufw allow 443
   ```

### 监控配置

1. **添加监控服务**
   ```yaml
   # 在docker-compose.yml中添加
   prometheus:
     image: prom/prometheus
     ports:
       - "9090:9090"
   
   grafana:
     image: grafana/grafana
     ports:
       - "3001:3000"
   ```

2. **日志聚合**
   ```yaml
   # 添加ELK栈
   elasticsearch:
     image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
   
   logstash:
     image: docker.elastic.co/logstash/logstash:7.17.0
   
   kibana:
     image: docker.elastic.co/kibana/kibana:7.17.0
   ```

## 更新部署

### 更新代码

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose build --no-cache

# 重启服务
docker-compose up -d
```

### 数据库迁移

```bash
# 运行数据库迁移
docker-compose exec backend alembic upgrade head
```

## 支持

如果遇到问题，请：

1. 查看日志：`docker-compose logs -f`
2. 检查系统资源：`docker stats`
3. 查看服务状态：`docker-compose ps`
4. 提交Issue到项目仓库

## 许可证

本项目采用 MIT 许可证。