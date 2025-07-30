#!/bin/bash

# 演示启动脚本

echo "🚀 启动视频音频标注工具演示..."

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "❌ 配置文件不存在，请先运行: ./demo-setup.sh"
    exit 1
fi

# 启动后端
echo "🔧 启动后端服务..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 5

# 启动前端
echo "🎨 启动前端服务..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ 服务启动完成！"
echo ""
echo "🌐 访问地址:"
echo "   前端应用: http://localhost:3000"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "👤 默认用户:"
echo "   管理员: admin / admin123"
echo "   标注员: annotator / annotator123"
echo "   审阅员: reviewer / reviewer123"
echo ""
echo "🛑 停止服务: Ctrl+C"

# 等待用户中断
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait