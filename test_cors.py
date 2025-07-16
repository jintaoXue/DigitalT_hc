#!/usr/bin/env python3
"""
测试CORS功能
"""

import requests
import json

def test_cors_headers():
    """测试CORS响应头"""
    
    # 测试 synthetic_data.py (端口 1004)
    print("=== 测试 synthetic_data.py CORS ===")
    try:
        response = requests.get("http://localhost:1004/data")
        print(f"状态码: {response.status_code}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not found')}")
        print(f"Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'Not found')}")
        print(f"Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'Not found')}")
    except requests.exceptions.ConnectionError:
        print("无法连接到 synthetic_data 服务器 (端口 1004)")
    
    print("\n" + "="*50 + "\n")
    
    # 测试 listener.py (端口 1005)
    print("=== 测试 listener.py CORS ===")
    try:
        response = requests.get("http://localhost:1005/data")
        print(f"状态码: {response.status_code}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not found')}")
        print(f"Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'Not found')}")
        print(f"Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'Not found')}")
    except requests.exceptions.ConnectionError:
        print("无法连接到 listener 服务器 (端口 1005)")

def test_preflight_request():
    """测试预检请求 (OPTIONS)"""
    
    print("\n=== 测试预检请求 ===")
    
    # 测试 synthetic_data.py
    try:
        response = requests.options("http://localhost:1004/data")
        print(f"synthetic_data OPTIONS 状态码: {response.status_code}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not found')}")
    except requests.exceptions.ConnectionError:
        print("无法连接到 synthetic_data 服务器")
    
    # 测试 listener.py
    try:
        response = requests.options("http://localhost:1005/data")
        print(f"listener OPTIONS 状态码: {response.status_code}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not found')}")
    except requests.exceptions.ConnectionError:
        print("无法连接到 listener 服务器")

if __name__ == "__main__":
    print("CORS 测试开始...")
    print("请确保 synthetic_data.py 和 listener.py 正在运行")
    print("启动命令:")
    print("  python source/synthetic_data.py")
    print("  python source/listener.py")
    print("\n" + "="*50)
    
    test_cors_headers()
    test_preflight_request()
    
    print("\n" + "="*50)
    print("CORS 测试完成") 