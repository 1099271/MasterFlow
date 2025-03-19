# MasterFlow

## 项目简介
MasterFlow是一个基于FastAPI开发的市场营销工作流管理系统，旨在提供更高效的市场营销工作流程。

## 主要功能
- 用户管理：支持用户注册、登录和权限控制
- 物品管理：提供物品信息的增删改查功能
- 小红书数据集成：支持小红书相关数据的管理和操作

## 技术栈
- 后端框架：FastAPI
- 数据库：MySQL
- ORM：SQLAlchemy
- 认证：JWT (JSON Web Tokens)
- 其他工具：Python-dotenv, Pydantic, Uvicorn

## 环境要求
- Python 3.8+
- MySQL 5.7+
- Torch 2.6.0+cu126

## 部署步骤

### 1. 克隆项目
```bash
git clone [项目地址]
cd MasterFlow
```

### 2. 创建并激活虚拟环境
1. 创建虚拟环境
```bash
python -m venv .venv
```

2. 激活虚拟环境

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 环境配置
1. 复制环境变量示例文件
```bash
cp .env.example .env
```

2. 修改.env文件，配置以下必要参数：
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=masterflow
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### 5. 数据库配置
1. 创建数据库
```sql
CREATE DATABASE masterflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```


### 6. 启动应用
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动后可以通过以下地址访问：
- API文档：http://localhost:8000/docs
- 交互式API文档：http://localhost:8000/redoc

## API文档
项目启动后，可以通过访问 `/docs` 或 `/redoc` 路径查看详细的API文档。

## 开发说明
- 代码结构说明：
  - `app/api`: API路由定义
  - `app/models`: 数据模型定义
  - `app/config`: 配置文件
  - `app/database`: 数据库配置
  - `app/utils`: 工具函数
  - `docs`: 数据库设计和接口文档
  - `logs`: 日志目录