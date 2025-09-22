#!/bin/bash
# AI城建系统启动脚本

echo "🚀 启动AI城建系统..."
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查依赖
if ! python3 -c "import flask" &> /dev/null; then
    echo "⚠️ 警告: 依赖包未安装，正在安装..."
    pip3 install -r requirements.txt
fi

# 创建必要目录
mkdir -p instance logs uploads backup

# 启动应用
echo "🌐 启动Web服务器..."
echo "📱 访问地址: http://localhost:8082"
echo "🔐 默认登录: admin / admin123"
echo "================================"
echo "按 Ctrl+C 停止服务器"
echo ""

python3 app.py
