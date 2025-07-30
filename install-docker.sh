#!/bin/bash

# Docker安装脚本

echo "🐳 安装Docker和Docker Compose..."

# 检查操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到Linux系统"
    
    # 更新包管理器
    sudo apt-get update
    
    # 安装必要的包
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # 添加Docker官方GPG密钥
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # 添加Docker仓库
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # 安装Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    
    # 启动Docker服务
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # 将当前用户添加到docker组
    sudo usermod -aG docker $USER
    
    # 安装Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到macOS系统"
    echo "请手动安装Docker Desktop: https://www.docker.com/products/docker-desktop"
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "检测到Windows系统"
    echo "请手动安装Docker Desktop: https://www.docker.com/products/docker-desktop"
    
else
    echo "不支持的操作系统: $OSTYPE"
    exit 1
fi

echo "✅ Docker安装完成！"
echo ""
echo "📋 验证安装:"
echo "   docker --version"
echo "   docker-compose --version"
echo ""
echo "🚀 启动应用:"
echo "   ./start.sh"