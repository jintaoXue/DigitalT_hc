from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS支持

@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'