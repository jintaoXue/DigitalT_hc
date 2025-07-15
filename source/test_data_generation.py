#!/usr/bin/env python3
"""
测试数据生成功能
"""

import requests
import json
import time

def test_synthetic_data_api():
    """测试synthetic_data.py的API功能"""
    base_url = "http://localhost:5002"
    
    print("=== 测试数据生成API ===")
    
    # 测试生成用户数据
    print("\n1. 生成用户数据...")
    response = requests.post(f"{base_url}/generate", json={
        "type": "user",
        "num": 5
    })
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试生成传感器数据
    print("\n2. 生成传感器数据...")
    response = requests.post(f"{base_url}/generate", json={
        "type": "sensor",
        "num": 3
    })
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试获取数据
    print("\n3. 获取当前数据...")
    response = requests.get(f"{base_url}/data")
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"数据条数: {data.get('count', 0)}")
    
    # 测试清空数据
    print("\n4. 清空数据...")
    response = requests.post(f"{base_url}/clear")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")

def test_listener_api():
    """测试listener.py的API功能"""
    base_url = "http://localhost:1004"
    
    print("\n=== 测试Listener API ===")
    
    # 测试获取数据
    print("\n1. 获取数据...")
    try:
        response = requests.get(f"{base_url}/data")
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"数据条数: {data.get('data', {}).get('count', 0)}")
    except requests.exceptions.ConnectionError:
        print("无法连接到listener服务器，请确保listener.py正在运行")
        return
    
    # 测试发送数据到receive端点
    print("\n2. 发送测试数据到receive端点...")
    test_data = {
        "message": "测试数据1",
        "timestamp": time.time(),
        "source": "test_script"
    }
    try:
        response = requests.post(f"{base_url}/receive", json=test_data)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {result}")
        print(f"是否保存到文件: {result.get('saved_to_file', False)}")
    except requests.exceptions.ConnectionError:
        print("无法连接到listener服务器，请确保listener.py正在运行")
        return
    
    # 测试发送更多数据
    print("\n3. 发送更多测试数据...")
    test_data2 = {
        "message": "测试数据2",
        "user_id": 123,
        "action": "login",
        "timestamp": time.time()
    }
    try:
        response = requests.post(f"{base_url}/receive", json=test_data2)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {result}")
    except requests.exceptions.ConnectionError:
        print("无法连接到listener服务器")
        return
    
    # 测试获取消息文件数据
    print("\n4. 获取message.json数据...")
    try:
        response = requests.get(f"{base_url}/messages")
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"消息文件数据条数: {data.get('count', 0)}")
        if data.get('data'):
            print("消息内容预览:")
            for i, msg in enumerate(data['data'][:2]):  # 只显示前2条
                print(f"  消息{i+1}: {msg.get('message', 'N/A')}")
    except requests.exceptions.ConnectionError:
        print("无法连接到listener服务器")
        return

def test_message_persistence():
    """测试消息持久化功能"""
    base_url = "http://localhost:1004"
    
    print("\n=== 测试消息持久化 ===")
    
    # 发送不同类型的消息
    messages = [
        {"type": "info", "content": "系统启动", "level": "info"},
        {"type": "error", "content": "连接失败", "level": "error"},
        {"type": "warning", "content": "磁盘空间不足", "level": "warning"}
    ]
    
    for i, msg in enumerate(messages):
        print(f"\n发送消息 {i+1}: {msg['content']}")
        try:
            response = requests.post(f"{base_url}/receive", json=msg)
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"保存状态: {result.get('saved_to_file', False)}")
        except requests.exceptions.ConnectionError:
            print("无法连接到listener服务器")
            return
    
    # 验证消息是否保存到文件
    print("\n验证消息保存...")
    try:
        response = requests.get(f"{base_url}/messages")
        data = response.json()
        print(f"总消息数: {data.get('count', 0)}")
        
        # 显示所有消息
        if data.get('data'):
            print("所有消息:")
            for i, msg in enumerate(data['data']):
                print(f"  {i+1}. {msg}")
    except requests.exceptions.ConnectionError:
        print("无法连接到listener服务器")

def test_message_management():
    """测试消息管理功能"""
    base_url = "http://localhost:1004"
    
    print("\n=== 测试消息管理 ===")
    
    # 测试清空消息
    print("\n1. 清空消息文件...")
    try:
        response = requests.post(f"{base_url}/clear_messages")
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {result}")
    except requests.exceptions.ConnectionError:
        print("无法连接到listener服务器")
        return
    
    # 验证消息是否已清空
    print("\n2. 验证消息是否已清空...")
    try:
        response = requests.get(f"{base_url}/messages")
        data = response.json()
        print(f"清空后消息数: {data.get('count', 0)}")
    except requests.exceptions.ConnectionError:
        print("无法连接到listener服务器")
        return

if __name__ == "__main__":
    print("开始测试数据生成功能...")
    
    # 测试synthetic_data API
    test_synthetic_data_api()
    
    # 测试listener API
    test_listener_api()
    
    # 测试消息持久化
    test_message_persistence()
    
    # 测试消息管理
    test_message_management()
    
    print("\n测试完成！")
    