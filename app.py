from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'


if __name__ == '__main__':
    # 定时生成测试数据（每5秒）
    import threading
    def periodic_data():
        while True:
            hello()
    threading.Thread(target=periodic_data, daemon=True).start()
    
    # 启动Flask服务器，监听Ubuntu电脑B的IP
    app.run(host='0.0.0.0', port=5002)