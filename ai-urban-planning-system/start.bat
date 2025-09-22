@echo off
chcp 65001 >nul
echo 🚀 启动AI城建系统...
echo ================================

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查依赖
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 警告: 依赖包未安装，正在安装...
    pip install -r requirements.txt
)

REM 创建必要目录
if not exist "instance" mkdir instance
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "backup" mkdir backup

REM 启动应用
echo 🌐 启动Web服务器...
echo 📱 访问地址: http://localhost:8081
echo 🔐 默认登录: admin / admin123
echo ================================
echo 按 Ctrl+C 停止服务器
echo.

python app.py
pause
