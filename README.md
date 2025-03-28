# MasterFlow

MasterFlow 是一个基于 FastAPI 开发的市场营销工作流管理系统，专注于小红书数据的采集、分析和管理。系统采用现代化的技术栈，提供高效的数据处理和分析能力。

## 功能特性

- 🔍 **小红书数据采集**
  - 关键词搜索笔记
  - 获取笔记详情和评论
  - 采集作者信息
  - 话题讨论量分析

- 🏷️ **智能标签分析**
  - 基于大语言模型的标签提取
  - 标签相似度比较
  - 标签管理和标准化

- 📊 **数据分析与可视化**
  - 笔记数据统计
  - 作者画像分析
  - 话题热度趋势

- 🔒 **安全认证**
  - JWT 认证
  - 用户权限管理
  - 数据访问控制

## 文档中心

MasterFlow 提供了详细的文档，帮助您快速了解和使用系统：

### 1. 系统概述
- [架构说明](docs/architecture.md) - 系统架构和目录结构
- [核心代码逻辑](docs/core_logic.md) - 核心模块功能和实现

### 2. 数据库设计
- [数据库设计文档](docs/database/design.md) - 数据库表结构和关系
- [数据库SQL脚本](docs/database/xhs_database.sql) - 数据库创建脚本

### 3. API参考
- [API接口文档](docs/api_reference.md) - 系统API接口说明

### 4. 部署与维护
- [部署指南](docs/deployment.md) - 系统部署步骤
- [环境配置说明](.env.example) - 环境变量配置

### 5. 其他资源
- [提示词示例](docs/prompt/) - 标签提取提示词
- [Coze集成文档](docs/coze/) - Coze平台集成

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+
- Redis 6.0+ (可选)

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/your-org/masterflow.git
cd masterflow
```

2. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的参数
```

5. 初始化数据库
```bash
mysql -u your_user -p your_database < docs/database/xhs_database.sql
```

6. 启动应用
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 开发指南

### 代码结构

```
masterflow/
├── app/                    # 应用主目录
│   ├── api/               # API路由
│   ├── core/              # 核心功能
│   ├── models/            # 数据模型
│   ├── schemas/           # 数据模式
│   └── services/          # 业务服务
├── docs/                  # 文档目录
├── tests/                 # 测试目录
├── .env.example          # 环境变量示例
├── requirements.txt      # 项目依赖
└── README.md            # 项目说明
```

### 开发规范

- 遵循 PEP 8 编码规范
- 使用类型注解
- 编写单元测试
- 保持代码文档更新

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目维护者：[Your Name](mailto:your.email@example.com)
- 项目主页：[GitHub](https://github.com/your-org/masterflow)
- 问题反馈：[Issues](https://github.com/your-org/masterflow/issues)