from flask import Flask, jsonify, request
import time
import json
import os

app = Flask(__name__)

# JSON文件路径 - 使用os.path确保跨平台兼容
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
JSON_FILE_PATH = os.path.join(parent_dir, 'data', 'data.json')
MESSAGE_FILE_PATH = os.path.join(parent_dir, 'data', 'message.json')

# 读取本地JSON文件数据
def read_json_data():
    """读取本地JSON文件数据"""
    try:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        else:
            print(f"警告: 文件 {JSON_FILE_PATH} 不存在")
            return []
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return []
    except Exception as e:
        print(f"读取文件错误: {e}")
        return []

# 保存消息到message.json文件
def save_message_to_file(message_data):
    """保存消息数据到message.json文件"""
    try:
        # 读取现有消息（如果文件存在）
        existing_messages = []
        if os.path.exists(MESSAGE_FILE_PATH):
            try:
                with open(MESSAGE_FILE_PATH, 'r', encoding='utf-8') as file:
                    existing_messages = json.load(file)
            except json.JSONDecodeError:
                # 如果文件损坏，重新开始
                existing_messages = []
        
        # 添加新消息
        existing_messages.append(message_data)
        
        # 保存到文件
        with open(MESSAGE_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(existing_messages, file, ensure_ascii=False, indent=2)
        
        print(f"消息已保存到 {MESSAGE_FILE_PATH}")
        return True
    except Exception as e:
        print(f"保存消息失败: {e}")
        return False

# 读取message.json文件数据
def read_message_data():
    """读取message.json文件数据"""
    try:
        if os.path.exists(MESSAGE_FILE_PATH):
            with open(MESSAGE_FILE_PATH, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        else:
            print(f"消息文件 {MESSAGE_FILE_PATH} 不存在")
            return []
    except json.JSONDecodeError as e:
        print(f"消息文件JSON解析错误: {e}")
        return []
    except Exception as e:
        print(f"读取消息文件错误: {e}")
        return []

# 提供数据端点
@app.route('/data', methods=['GET'])
def get_data():
    """获取数据端点 - 读取本地JSON文件并返回数据"""
    try:
        # 读取本地JSON文件数据
        json_data = read_json_data()
        
        if json_data:
            # 添加时间戳和来源信息
            response_data = {
                'timestamp': time.time(),
                'source': 'Ubuntu B',
                'data': json_data,
                'count': len(json_data)
            }
            return jsonify({'status': 'success', 'data': response_data}), 200
        else:
            return jsonify({'status': 'empty', 'message': 'No data available in JSON file'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error reading data: {str(e)}'}), 500

# 接受外部发送的数据
@app.route('/receive', methods=['POST'])
def receive_data():
    """接收外部发送的数据并存储到message.json文件"""
    try:
        # 获取POST请求的JSON数据
        data = request.get_json()
        
        if data is None:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400
        
        # 添加接收时间戳和来源信息
        data['received_at'] = time.time()
        data['received_by'] = 'Ubuntu B'
        
        # 保存消息到message.json文件
        save_success = save_message_to_file(data)
        
        print(f'Received data: {data}')
        
        response = {
            'status': 'success', 
            'message': 'Data received and saved successfully',
            'saved_to_file': save_success
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error processing data: {str(e)}'}), 500

# 获取消息文件中的数据
@app.route('/messages', methods=['GET'])
def get_messages():
    """获取message.json文件中的数据"""
    try:
        messages = read_message_data()
        return jsonify({
            'status': 'success',
            'data': messages,
            'count': len(messages)
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error reading messages: {str(e)}'}), 500

# 清空消息文件
@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    """清空message.json文件"""
    try:
        with open(MESSAGE_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=2)
        return jsonify({'status': 'success', 'message': 'Messages cleared'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error clearing messages: {str(e)}'}), 500

if __name__ == '__main__':
    # 启动Flask服务器，监听Ubuntu电脑B的IP
    print(f"启动服务器，监听端口 1004")
    print(f"可用端点:")
    print(f"  GET  /data           - 读取本地JSON文件数据")
    print(f"  POST /receive        - 接收外部数据并保存到message.json")
    print(f"  GET  /messages       - 获取message.json数据")
    print(f"  POST /clear_messages - 清空消息文件")
    
    app.run(host='0.0.0.0', port=1004, debug=True)