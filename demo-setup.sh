#!/bin/bash

# 演示环境设置脚本

echo "🎬 设置视频音频标注工具演示环境..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，请先安装Python3"
    exit 1
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装，请先安装Node.js"
    exit 1
fi

echo "📦 安装后端依赖..."
cd backend
python3 -m pip install -r requirements.txt

echo "📦 安装前端依赖..."
cd ../frontend
npm install

echo "🔧 创建配置文件..."
cd ..
cat > .env << EOF
# 数据库配置
DATABASE_URL=sqlite:///./annotation.db

# Redis配置
REDIS_URL=redis://localhost:6379

# JWT配置
SECRET_KEY=demo-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MinIO配置
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=annotation-media

# 文件上传配置
MAX_FILE_SIZE=104857600
EOF

echo "✅ 演示环境设置完成！"
echo ""
echo "🚀 启动演示服务:"
echo "   ./demo-start.sh"
echo ""
echo "📋 访问地址:"
echo "   前端: http://localhost:3000"
echo "   后端: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"