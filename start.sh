#!/bin/bash

# 视频音频标注工具启动脚本

echo "🚀 启动视频音频标注工具..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建必要的目录
mkdir -p logs
mkdir -p data

echo "📦 构建Docker镜像..."
docker-compose build

echo "🔄 启动服务..."
docker-compose up -d

echo "⏳ 等待服务启动..."
sleep 30

echo "✅ 服务启动完成！"
echo ""
echo "🌐 访问地址:"
echo "   前端应用: http://localhost:3000"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo "   MinIO管理: http://localhost:9001"
echo ""
echo "👤 默认用户:"
echo "   管理员: admin / admin123"
echo "   标注员: annotator / annotator123"
echo "   审阅员: reviewer / reviewer123"
echo "   项目经理: project_manager / manager123"
echo ""
echo "📋 查看日志: docker-compose logs -f"
echo "🛑 停止服务: docker-compose down"