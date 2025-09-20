#!/bin/bash

# AI城建系统本地启动脚本
# 作者: AI Assistant
# 日期: $(date +%Y-%m-%d)

echo "=========================================="
echo "    AI城建系统本地部署启动脚本"
echo "=========================================="

# 检查Python环境
echo "1. 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python版本: $PYTHON_VERSION"

# 检查依赖包
echo "2. 检查依赖包..."
if ! python3 -c "import flask, pandas, plotly" &> /dev/null; then
    echo "⚠️  正在安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖包安装失败"
        exit 1
    fi
else
    echo "✅ 依赖包检查通过"
fi

# 创建必要的目录
echo "3. 创建必要目录..."
mkdir -p instance
mkdir -p logs
mkdir -p uploads
mkdir -p backup
echo "✅ 目录创建完成"

# 启动应用
echo "4. 启动AI城建系统..."
echo "   访问地址: http://localhost:8080"
echo "   基础数据: http://localhost:8080/basic_data"
echo "   智能图表: http://localhost:8080/smart_charts"
echo ""
echo "按 Ctrl+C 停止服务"
echo "=========================================="

# 启动应用
python3 app.py
