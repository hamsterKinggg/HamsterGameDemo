# 仓鼠互动游戏 - API接口文档 (MVP)

> 版本：v0.1  
> Base URL: `http://localhost:8000/api`

---

## 通用说明

- 除登录外，所有接口需在Header携带：`Authorization: Bearer <token>`
- 响应格式：JSON
- 状态值范围：0-100

---

## 1. 登录

**POST** `/auth/device`

### 请求
```json
{ "device_id": "uuid-or-hash" }
```

### 响应
```json
{
  "token": "jwt-token",
  "user_id": "u_123",
  "current_node": "start",
  "stats": {
    "hunger": 80,
    "energy": 100,
    "cleanliness": 90,
    "happiness": 75,
    "health": 100
  },
  "inventory": ["apple"],
  "equipped_skin": "default"
}
```

---

## 2. 获取剧情节点

**GET** `/story/node/{node_id}`

### 响应
```json
{
  "node_id": "n_001",
  "type": "story",
  "video_url": "https://cdn.xxx.com/videos/n_001.mp4",
  "choices": [
    {
      "choice_id": "c1",
      "text": "喂食"
    },
    {
      "choice_id": "c2",
      "text": "玩耍"
    }
  ],
  "prefetch": ["https://cdn.xxx.com/videos/n_002.mp4"]
}
```

---

## 3. 提交剧情选择

**POST** `/story/choice`

### 请求
```json
{
  "node_id": "n_001",
  "choice_id": "c1"
}
```

### 响应
```json
{
  "next_node": "n_002",
  "updated_stats": {
    "hunger": 90,
    "energy": 55
  },
  "reward": {
    "items": ["cookie"]
  }
}
```

---

## 4. 获取小游戏题目

**GET** `/minigame/{node_id}`

### 响应
```json
{
  "node_id": "q_001",
  "attempt_id": "att_abc123",
  "question": "仓鼠每天需要喝多少水？",
  "options": [
    { "id": "a", "text": "5-10ml" },
    { "id": "b", "text": "50-100ml" },
    { "id": "c", "text": "不需要喝水" }
  ]
}
```

---

## 5. 提交小游戏答案

**POST** `/minigame/submit`

### 请求
```json
{
  "node_id": "q_001",
  "attempt_id": "att_abc123",
  "answer_id": "a"
}
```

### 响应
```json
{
  "correct": true,
  "next_node": "n_003",
  "updated_stats": {
    "happiness": 85
  },
  "reward": {
    "items": []
  }
}
```

---

## 6. 使用道具

**POST** `/item/use`

### 请求
```json
{
  "item_id": "apple"
}
```

### 响应
```json
{
  "success": true,
  "updated_stats": {
    "hunger": 100
  },
  "inventory": []
}
```

---

## 7. 装备皮肤

**POST** `/skin/equip`

### 请求
```json
{
  "skin_id": "hat_strawberry"
}
```

### 响应
```json
{
  "success": true,
  "equipped_skin": "hat_strawberry",
  "idle_video_url": "https://cdn.xxx.com/videos/idle_strawberry.mp4"
}
```

---

## 错误响应格式

```json
{
  "error": "invalid_choice",
  "message": "选项不存在"
}
```

常见错误码：
- `invalid_token` - token无效或过期
- `invalid_node` - 节点不存在
- `invalid_choice` - 选项不合法
- `invalid_attempt` - attempt_id无效或已使用
- `item_not_found` - 道具不存在
- `skin_not_unlocked` - 皮肤未解锁
