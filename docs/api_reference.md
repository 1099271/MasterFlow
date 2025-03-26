# MasterFlow API 接口文档

## 接口概述

MasterFlow 系统提供了一系列 RESTful API 接口，用于小红书数据的采集、分析和管理。所有API均基于 HTTP 协议，采用 JSON 格式进行数据交换。

## 基础信息

- **基础URL**: `http://localhost:8000`
- **API文档**: `/docs` 或 `/redoc`
- **认证方式**: JWT (Bearer Token)

## 认证相关接口

### 1. 用户注册

- **URL**: `/api/users/register`
- **方法**: `POST`
- **描述**: 创建新用户
- **请求体**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **响应**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "is_active": "boolean"
  }
  ```

### 2. 用户登录

- **URL**: `/api/auth/token`
- **方法**: `POST`
- **描述**: 获取访问令牌
- **请求体**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **响应**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

### 3. 获取当前用户信息

- **URL**: `/api/users/me`
- **方法**: `GET`
- **描述**: 获取当前登录用户信息
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "is_active": "boolean"
  }
  ```

## 小红书数据接口

### 1. 关键词搜索

- **URL**: `/api/xhs/search`
- **方法**: `GET`
- **描述**: 通过关键词搜索小红书笔记
- **参数**:
  - `keyword`: 搜索关键词 (必填)
  - `page`: 页码，默认为1
  - `page_size`: 每页数量，默认为20
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "items": [
      {
        "note_id": "string",
        "note_url": "string",
        "auther_user_id": "string",
        "auther_nick_name": "string",
        "note_display_title": "string",
        "note_cover_url_pre": "string",
        "note_liked_count": "integer"
      }
    ],
    "total": "integer",
    "page": "integer",
    "page_size": "integer"
  }
  ```

### 2. 获取笔记详情

- **URL**: `/api/xhs/notes/{note_id}`
- **方法**: `GET`
- **描述**: 获取特定笔记的详细信息
- **路径参数**:
  - `note_id`: 笔记ID (必填)
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "note_id": "string",
    "auther_user_id": "string",
    "auther_nick_name": "string",
    "note_display_title": "string",
    "note_desc": "string",
    "note_create_time": "string (datetime)",
    "note_liked_count": "integer",
    "comment_count": "integer",
    "note_image_list": ["string"],
    "note_tags": ["string"]
  }
  ```

### 3. 获取笔记评论

- **URL**: `/api/xhs/notes/{note_id}/comments`
- **方法**: `GET`
- **描述**: 获取笔记的评论列表
- **路径参数**:
  - `note_id`: 笔记ID (必填)
- **查询参数**:
  - `cursor`: 分页游标，默认为空
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "comments": [
      {
        "comment_id": "string",
        "comment_user_id": "string",
        "comment_user_nickname": "string",
        "comment_content": "string",
        "comment_like_count": "integer",
        "comment_create_time": "string (datetime)",
        "comment_sub_comments": []
      }
    ],
    "has_more": "boolean",
    "cursor": "string"
  }
  ```

### 4. 获取作者信息

- **URL**: `/api/xhs/authers/{auther_id}`
- **方法**: `GET`
- **描述**: 获取作者详细信息
- **路径参数**:
  - `auther_id`: 作者ID (必填)
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "auther_user_id": "string",
    "auther_nick_name": "string",
    "auther_avatar": "string",
    "auther_desc": "string",
    "auther_fans": "integer",
    "auther_follows": "integer",
    "auther_interaction": "integer",
    "auther_red_id": "string"
  }
  ```

### 5. 获取作者笔记列表

- **URL**: `/api/xhs/authers/{auther_id}/notes`
- **方法**: `GET`
- **描述**: 获取作者的笔记列表
- **路径参数**:
  - `auther_id`: 作者ID (必填)
- **查询参数**:
  - `cursor`: 分页游标，默认为空
  - `page_size`: 每页数量，默认为20
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "notes": [
      {
        "note_id": "string",
        "note_url": "string",
        "note_display_title": "string",
        "note_cover_url_pre": "string",
        "note_liked_count": "integer",
        "note_create_time": "string (datetime)"
      }
    ],
    "has_more": "boolean",
    "cursor": "string"
  }
  ```

### 6. 获取话题讨论量

- **URL**: `/api/xhs/topics/discussions`
- **方法**: `GET`
- **描述**: 获取话题讨论量数据
- **查询参数**:
  - `topic_name`: 话题名称 (必填)
  - `days`: 查询天数，默认为30
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "topic_name": "string",
    "discussions": [
      {
        "date": "string (date)",
        "view_num": "integer"
      }
    ]
  }
  ```

## 标签分析接口

### 1. 提取笔记标签

- **URL**: `/api/tags/extract`
- **方法**: `POST`
- **描述**: 从笔记内容中提取标签
- **请求体**:
  ```json
  {
    "note_id": "string",
    "llm_model": "string" // 可选，默认使用配置的模型
  }
  ```
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "note_id": "string",
    "extracted_tags": ["string"],
    "success": "boolean",
    "llm_model": "string"
  }
  ```

### 2. 标签相似度比较

- **URL**: `/api/tags/compare`
- **方法**: `POST`
- **描述**: 比较标签组之间的相似度
- **请求体**:
  ```json
  {
    "collected_tags": ["string"],
    "standard_tags": ["string"],
    "visualize": "boolean" // 可选，是否生成可视化，默认为false
  }
  ```
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "score": "float",
    "detailed_scores": {
      "max_similarity": "float",
      "optimal_matching": "float",
      "coverage": "float"
    },
    "interpretation": "string"
  }
  ```

### 3. 获取标签比较结果

- **URL**: `/api/tags/comparison_results`
- **方法**: `GET`
- **描述**: 获取已保存的标签比较结果
- **查询参数**:
  - `note_id`: 笔记ID (必填)
  - `llm_name`: 模型名称 (可选)
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "results": [
      {
        "note_id": "string",
        "llm_name": "string",
        "collected_tags": ["string"],
        "standard_tags": ["string"],
        "score": "float",
        "created_at": "string (datetime)"
      }
    ]
  }
  ```

### 4. 批量标签分析

- **URL**: `/api/tags/analyze_batch`
- **方法**: `POST`
- **描述**: 批量分析多条笔记的标签
- **请求体**:
  ```json
  {
    "note_ids": ["string"],
    "llm_model": "string" // 可选，默认使用配置的模型
  }
  ```
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "total": "integer",
    "success_count": "integer",
    "failed_count": "integer",
    "results": [
      {
        "note_id": "string",
        "success": "boolean",
        "message": "string"
      }
    ]
  }
  ```

## 项目管理接口

### 1. 创建项目

- **URL**: `/api/items/`
- **方法**: `POST`
- **描述**: 创建新项目
- **请求体**:
  ```json
  {
    "title": "string",
    "description": "string"
  }
  ```
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "id": "integer",
    "title": "string",
    "description": "string",
    "owner_id": "integer",
    "created_at": "string (datetime)"
  }
  ```

### 2. 获取项目列表

- **URL**: `/api/items/`
- **方法**: `GET`
- **描述**: 获取项目列表
- **查询参数**:
  - `skip`: 跳过的条数，默认为0
  - `limit`: 限制返回的条数，默认为100
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  [
    {
      "id": "integer",
      "title": "string",
      "description": "string",
      "owner_id": "integer",
      "created_at": "string (datetime)"
    }
  ]
  ```

### 3. 获取单个项目

- **URL**: `/api/items/{item_id}`
- **方法**: `GET`
- **描述**: 获取单个项目详情
- **路径参数**:
  - `item_id`: 项目ID (必填)
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "id": "integer",
    "title": "string",
    "description": "string",
    "owner_id": "integer",
    "created_at": "string (datetime)"
  }
  ```

### 4. 更新项目

- **URL**: `/api/items/{item_id}`
- **方法**: `PUT`
- **描述**: 更新项目信息
- **路径参数**:
  - `item_id`: 项目ID (必填)
- **请求体**:
  ```json
  {
    "title": "string",
    "description": "string"
  }
  ```
- **认证**: 需要有效的访问令牌
- **响应**:
  ```json
  {
    "id": "integer",
    "title": "string",
    "description": "string",
    "owner_id": "integer",
    "created_at": "string (datetime)"
  }
  ```

### 5. 删除项目

- **URL**: `/api/items/{item_id}`
- **方法**: `DELETE`
- **描述**: 删除项目
- **路径参数**:
  - `item_id`: 项目ID (必填)
- **认证**: 需要有效的访问令牌
- **响应**: 状态码 204 (无内容)

## 错误处理

所有API接口遵循统一的错误处理机制，错误响应格式如下：

```json
{
  "detail": {
    "code": "string", // 错误代码
    "message": "string" // 错误消息
  }
}
```

常见错误代码：

| 状态码 | 错误代码        | 描述                   |
|--------|-----------------|------------------------|
| 400    | BAD_REQUEST     | 请求参数错误           |
| 401    | UNAUTHORIZED    | 未认证或令牌无效       |
| 403    | FORBIDDEN       | 权限不足               |
| 404    | NOT_FOUND       | 资源不存在             |
| 422    | VALIDATION_ERROR| 请求数据验证失败       |
| 500    | SERVER_ERROR    | 服务器内部错误         |

## 请求速率限制

为了保护API不被滥用，系统实施了请求速率限制：

- 匿名用户: 100次请求/小时
- 认证用户: 1000次请求/小时

超过限制将返回429状态码，并附带以下响应：

```json
{
  "detail": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": "integer (seconds)"
  }
}
```

## API版本控制

当前API版本为v1，建议在请求头中包含API版本信息：

```
Accept: application/json; version=1.0
```

未来版本更新将通过API版本控制机制保持向后兼容。 