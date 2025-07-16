import json
import random
import time
import argparse
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # 启用CORS支持

# JSON文件路径 - 使用os.path确保跨平台兼容
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
JSON_FILE_PATH = os.path.join(parent_dir, 'data', 'data.json')

def generate_user_data(num=10):
    """生成用户数据"""
    data = []
    for i in range(num):
        item = {
            "id": i,
            "name": f"user_{i}",
            "age": random.randint(18, 60),
            "email": f"user_{i}@example.com",
            "created_at": time.time()
        }
        data.append(item)
    return data

def generate_sensor_data(num=10):
    """生成传感器数据"""
    data = []
    # for i in range(num):
    #     item = {
    #         "id": i,
    #         "sensor_type": random.choice(["temperature", "humidity", "pressure", "light"]),
    #         "value": round(random.uniform(0, 100), 2),
    #         "unit": random.choice(["°C", "%", "hPa", "lux"]),
    #         "timestamp": time.time()
    #     }
    #     data.append(item)
    item_0 = {
        "id": 0,
        "name": "Welding robot equipment",
        "sensor_type": random.choice(["Current and Voltage"]),
        "value": [round(random.uniform(0, 100), 2) for _ in range(2)],
        "state_type": "working animation",
        "timestamp": time.time(),

    }
    item_1 = {
        "id": 1,
        "name": "Rotary pipe automatic welding machine",
        "sensor_type": random.choice(["Current and Voltage"]),
        "value": [round(random.uniform(0, 100), 2) for _ in range(2)],
        "state_type": "finished work and reseting animation",
        "timestamp": time.time(),

    }
    data.append(item_0)
    data.append(item_1)
    return data

def generate_data(data_type="user", num=10):
    """根据类型生成数据"""
    if data_type == "user":
        return generate_user_data(num)
    elif data_type == "sensor":
        return generate_sensor_data(num)
    else:
        return generate_user_data(num)

def save_data_to_file(data, filename=None):
    """保存数据到JSON文件"""
    if filename is None:
        filename = JSON_FILE_PATH
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {filename}")
        return True
    except Exception as e:
        print(f"保存数据失败: {e}")
        return False

def load_data_from_file(filename=None):
    """从JSON文件加载数据"""
    if filename is None:
        filename = JSON_FILE_PATH
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        else:
            print(f"文件 {filename} 不存在")
            return []
    except Exception as e:
        print(f"加载数据失败: {e}")
        return []

# Flask API端点
@app.route('/generate', methods=['POST'])
def generate_data_endpoint():
    """生成数据的API端点"""
    try:
        data = request.get_json() or {}
        data_type = data.get('type', 'user')
        num = data.get('num', 10)
        
        generated_data = generate_data(data_type, num)
        
        if save_data_to_file(generated_data):
            return jsonify({
                'status': 'success',
                'message': f'Generated {len(generated_data)} {data_type} records',
                'data': generated_data
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to save data'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating data: {str(e)}'
        }), 500

@app.route('/data', methods=['GET'])
def get_data_endpoint():
    """获取数据的API端点"""
    try:
        data = load_data_from_file()
        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error loading data: {str(e)}'
        }), 500

@app.route('/clear', methods=['POST'])
def clear_data_endpoint():
    """清空数据的API端点"""
    try:
        save_data_to_file([])
        return jsonify({
            'status': 'success',
            'message': 'Data cleared'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error clearing data: {str(e)}'
        }), 500

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='数据生成API服务器')
    parser.add_argument('--port', type=int, default=1004, help='服务器端口号 (默认: 1004)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='服务器主机地址 (默认: 0.0.0.0)')
    args = parser.parse_args()
    
    # 如果作为独立脚本运行，生成默认数据
    print("生成默认用户数据...")
    data = generate_sensor_data(20)
    save_data_to_file(data)
    
    # 启动Flask服务器（可选）
    print("启动数据生成API服务器...")
    print(f"服务器地址: http://{args.host}:{args.port}")
    print("可用端点:")
    print("  POST /generate - 生成新数据")
    print("  GET  /data     - 获取数据")
    print("  POST /clear    - 清空数据")
    
    app.run(host=args.host, port=args.port, debug=True)
    