from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# 存储待发送的数据
data_queue = []

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
    data = request.get_json()
    data_queue.append(data)
    return jsonify({'status': 'success', 'message': 'Data received'}), 200

if __name__ == '__main__':
    # 启动Flask服务器，监听Ubuntu电脑B的IP
    app.run(host='0.0.0.0', port=1005)