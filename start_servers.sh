#!/bin/bash

# 数字孪生系统服务器启动脚本

echo "启动数字孪生系统服务器..."

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "错误: 未找到Python"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
python -c "import flask, flask_cors, requests" 2>/dev/null || {
    echo "安装依赖..."
    pip install -r requirements.txt
}

# 创建数据目录
mkdir -p data

# 启动数据生成服务 (端口 1004)
echo "启动数据生成服务 (端口 1004)..."
python source/synthetic_data.py &
SYNTHETIC_PID=$!

# 等待一秒
sleep 1

# 启动监听服务 (端口 1005)
echo "启动监听服务 (端口 1005)..."
python source/listener.py &
LISTENER_PID=$!

echo ""
echo "服务器已启动!"
echo "数据生成服务: http://localhost:1004"
echo "监听服务: http://localhost:1005"
echo ""
echo "测试命令:"
echo "  python test_cors.py"
echo "  python test_data_generation.py"
echo ""
echo "或者打开 test_cors.html 在浏览器中测试"
echo ""
echo "按 Ctrl+C 停止所有服务器"

# 等待用户中断
trap "echo '停止服务器...'; kill $SYNTHETIC_PID $LISTENER_PID 2>/dev/null; exit" INT
wait 