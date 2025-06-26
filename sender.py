from flask import Flask, jsonify
import time
import requests

app = Flask(__name__)

# 存储待发送的数据
data_queue = []

# 模拟生成数据（可根据实际需求修改）
def generate_data():
    return {'timestamp': time.time(), 'message': 'Data from Ubuntu B', 'from': 'Ubuntu'}

# 提供数据端点
@app.route('/data', methods=['GET'])
def get_data():
    if data_queue:
        # 返回最新数据并清空队列（或根据需求保留）
        data = data_queue.pop(0)
        return jsonify({'status': 'success', 'data': data}), 200
    else:
        return jsonify({'status': 'empty', 'message': 'No data available'}), 200

# 接受外部发送的数据（可选，Windows电脑A可通过POST发送）
@app.route('/receive', methods=['POST'])
def receive_data():
    data = requests.json()
    data_queue.append(data)
    return jsonify({'status': 'success', 'message': 'Data received'}), 200

if __name__ == '__main__':
    # 定时生成测试数据（每5秒）
    import threading
    def periodic_data():
        while True:
            data_queue.append(generate_data())
            print(f'Generated data: {data_queue[-1]}')
            time.sleep(5)
    threading.Thread(target=periodic_data, daemon=True).start()
    
    # 启动Flask服务器，监听Ubuntu电脑B的IP
    app.run(host='0.0.0.0', port=5001)