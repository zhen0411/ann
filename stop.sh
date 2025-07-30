#!/bin/bash

# 视频音频标注工具停止脚本

echo "🛑 停止视频音频标注工具..."

# 停止所有服务
docker-compose down

echo "🧹 清理完成！"
echo ""
echo "💡 提示:"
echo "   要完全清理数据: docker-compose down -v"
echo "   要重新启动: ./start.sh"