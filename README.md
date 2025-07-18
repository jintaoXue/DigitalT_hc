# 数字孪生，数据生成和传输系统模块

这是一个数据生成和传输系统，包含数据生成服务和数据监听服务。

## 文件说明

### 1. `synthetic_data.py` - 数据生成服务
**端口**: 1004

**功能**:
- 生成多种类型的数据（用户数据、传感器数据、交易数据）
- 提供REST API接口
- 自动保存数据到JSON文件

**API端点**:
- `POST /generate` - 生成新数据
  - 参数: `{"type": "user|sensor|transaction", "num": 数量}`
- `GET /data` - 获取当前数据
- `POST /clear` - 清空数据

**使用方法**:
```bash
# 使用默认端口 1004
python synthetic_data.py

# 指定端口号
python synthetic_data.py --port 8080

# 指定主机和端口
python synthetic_data.py --host 127.0.0.1 --port 5000

# 查看帮助信息
python synthetic_data.py --help
```

**命令行参数**:
- `--port`: 设置服务器端口号 (默认: 1004)
- `--host`: 设置服务器主机地址 (默认: 0.0.0.0)

### 2. `listener.py` - 数据监听服务
**端口**: 1005

**功能**:
- 读取本地JSON文件数据
- 接收外部发送的数据并存储到message.json文件
- 管理消息文件

**API端点**:
- `GET /data` - 读取本地JSON文件数据
- `POST /receive` - 接收外部数据并保存到message.json
- `GET /messages` - 获取message.json文件数据
- `POST /clear_messages` - 清空消息文件

**使用方法**:
```bash
python listener.py
```

### 3. `sender.py` - 数据发送服务 (已废弃)
**端口**: 1005

**状态**: 此服务已废弃，不再维护和使用

**原功能**:
- 提供数据端点
- 接收外部数据

**注意**: 请使用 `listener.py` 作为主要的数据接收服务

## 数据文件

### 1. `data.json` - 数据文件
存储由 `synthetic_data.py` 生成的结构化数据

### 2. `message.json` - 消息文件
存储通过 `/receive` 端点接收到的所有消息数据，包含：
- 原始消息内容
- 接收时间戳 (`received_at`)
- 接收者信息 (`received_by`)

## 数据生成类型

### 1. 用户数据 (user)
```json
{
  "id": 0,
  "name": "user_0",
  "age": 34,
  "email": "user_0@example.com",
  "created_at": 1234567890.123
}
```

### 2. 传感器数据 (sensor)
```json
{
  "id": 0,
  "sensor_type": "temperature",
  "value": 25.5,
  "unit": "°C",
  "timestamp": 1234567890.123
}
```

## 使用示例

### 1. 启动数据生成服务
```bash
# 使用默认端口
python synthetic_data.py

# 或指定端口
python synthetic_data.py --port 8080
```

### 2. 生成数据
```bash
# 生成用户数据
curl -X POST http://localhost:1004/generate \
  -H "Content-Type: application/json" \
  -d '{"type": "user", "num": 10}'

# 生成传感器数据
curl -X POST http://localhost:1004/generate \
  -H "Content-Type: application/json" \
  -d '{"type": "sensor", "num": 5}'

# 如果使用了自定义端口，请相应修改URL
# 例如端口为8080时：
# curl -X POST http://localhost:8080/generate \
#   -H "Content-Type: application/json" \
#   -d '{"type": "sensor", "num": 5}'
```

### 3. 启动监听服务
```bash
python listener.py
```

### 4. 获取数据
```bash
# 从listener获取数据
curl http://localhost:1005/data

# 从synthetic_data获取数据
curl http://localhost:1004/data

# 如果使用了自定义端口，请相应修改URL
# 例如端口为8080时：
# curl http://localhost:8080/data
```

### 5. 发送数据到listener（自动保存到message.json）
```bash
# 发送简单消息
curl -X POST http://localhost:1005/receive \
  -H "Content-Type: application/json" \
  -d '{"message": "测试数据", "timestamp": 1234567890}'

# 发送复杂消息
curl -X POST http://localhost:1005/receive \
  -H "Content-Type: application/json" \
  -d '{
    "type": "error",
    "content": "连接失败",
    "level": "error",
    "user_id": 123
  }'
```

### 6. 查看消息文件数据
```bash
# 获取所有消息
curl http://localhost:1005/messages

# 清空消息文件
curl -X POST http://localhost:1005/clear_messages
```

## 消息存储机制

当通过 `POST /receive` 接收数据时，系统会：

1. **验证数据**: 检查是否为有效的JSON格式
2. **添加元数据**: 自动添加接收时间戳和来源信息
3. **保存到文件**: 将数据追加到 `message.json` 文件中
4. **返回状态**: 返回保存状态

### 消息文件格式
```json
[
  {
    "message": "原始消息内容",
    "received_at": 1234567890.123,
    "received_by": "Ubuntu B"
  },
  {
    "type": "error",
    "content": "连接失败",
    "level": "error",
    "received_at": 1234567891.456,
    "received_by": "Ubuntu B"
  }
]
```

## 测试

运行测试脚本:
```bash
python test_data_generation.py
```

测试脚本会验证：
- 数据生成功能
- 消息接收和存储功能
- 消息持久化功能
- 消息管理功能
- API端点响应

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐
│  synthetic_data │    │    listener     │
│   (端口:1004)   │    │   (端口:1005)   │
└─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
    data.json              data.json
                                    │
                                    ▼
                              message.json
```

**注意**: `sender.py` 服务已废弃，不再包含在系统架构中

## CORS 支持

系统已启用跨域资源共享 (CORS) 支持，允许来自不同域的前端应用访问API：

### 响应头
- `Access-Control-Allow-Origin: *` - 允许所有域访问
- `Access-Control-Allow-Methods: GET, POST, OPTIONS` - 允许的HTTP方法
- `Access-Control-Allow-Headers: Content-Type` - 允许的请求头

### 测试CORS
```bash
# 运行CORS测试
python test_cors.py
```

### 前端JavaScript示例
```javascript
// 从不同域访问API
fetch('http://localhost:1004/data')
  .then(response => response.json())
  .then(data => console.log(data));

// 发送数据到listener
fetch('http://localhost:1005/receive', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Hello from frontend',
    timestamp: Date.now()
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 注意事项

1. 确保Flask已安装: `pip install flask`
2. 确保Flask-CORS已安装: `pip install flask-cors`
3. 确保requests已安装: `pip install requests`
4. 不同服务使用不同端口，避免冲突
5. 数据文件 `data.json` 和 `message.json` 会在运行时自动创建
6. `message.json` 文件会持续增长，定期清理或归档
7. 消息存储是追加模式，不会覆盖现有数据
8. 系统不再使用内存队列，所有数据直接存储到文件
9. CORS配置允许所有域访问，生产环境建议限制特定域 