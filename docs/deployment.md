# MasterFlow 部署指南

## 系统要求

### 硬件要求

- **CPU**：至少4核心，推荐8核心
- **内存**：最小8GB，推荐16GB以上（特别是运行向量模型时）
- **存储**：至少50GB可用空间，SSD存储设备以提高数据库性能
- **网络**：稳定的互联网连接，如果部署在云服务器上，推荐至少1Mbps带宽

### 软件要求

- **操作系统**：
  - Linux (Ubuntu 20.04/22.04 推荐)
  - Windows 10/11
  - macOS 11.0+
- **Python 环境**：
  - Python 3.8+ (推荐Python 3.10)
  - 虚拟环境管理工具 (venv, conda等)
- **数据库**：
  - MySQL 5.7+ / MariaDB 10.5+
- **其他服务**：
  - (可选) Redis 6.0+ 用于缓存和任务队列
  - (可选) Nginx 用于反向代理

## 部署步骤

### 1. 准备环境

#### 安装Python

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-venv
```

**CentOS/RHEL**:
```bash
sudo yum install -y python3 python3-pip python3-devel gcc openssl-devel
```

**Windows**:
从[Python官网](https://www.python.org/downloads/)下载安装包安装。

#### 安装MySQL

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql_secure_installation
```

**CentOS/RHEL**:
```bash
sudo yum install -y mysql-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
sudo mysql_secure_installation
```

**Windows**:
从[MySQL官网](https://dev.mysql.com/downloads/installer/)下载安装包安装。

#### 创建MySQL数据库和用户

```sql
CREATE DATABASE masterflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'masterflow_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON masterflow.* TO 'masterflow_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. 克隆项目

```bash
git clone https://github.com/your-org/masterflow.git
cd masterflow
```

### 3. 设置Python虚拟环境

```bash
python -m venv .venv

# 在Linux/macOS上激活虚拟环境
source .venv/bin/activate

# 在Windows上激活虚拟环境
# .venv\Scripts\activate
```

### 4. 安装依赖包

```bash
pip install -r requirements.txt
```

特别说明：对于需要GPU加速的用户，可能需要单独安装PyTorch CUDA版本：

```bash
pip install torch==2.6.0+cu126 -f https://download.pytorch.org/whl/torch_stable.html
```

### 5. 配置环境变量

复制环境变量示例文件并进行修改：

```bash
cp .env.example .env
```

编辑`.env`文件，配置以下必要参数：

```ini
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=masterflow_user
DB_PASSWORD=your_password
DB_NAME=masterflow

# JWT配置
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 应用配置
DEBUG=True  # 生产环境设置为False
ENVIRONMENT=development  # 生产环境设置为production

# 模型配置
MODEL_PATH=./models
EMBEDDING_MODEL=distiluse-base-multilingual-cased-v2

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=./logs
```

### 6. 初始化数据库

导入基础数据库结构：

```bash
mysql -u masterflow_user -p masterflow < docs/database/xhs_database.sql
```

### 7. 启动应用

开发环境：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

生产环境：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 8. (可选) 设置Nginx反向代理

创建Nginx配置文件:

```bash
sudo nano /etc/nginx/sites-available/masterflow
```

添加以下内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件配置
    location /static {
        alias /path/to/masterflow/static;
        expires 30d;
    }
}
```

启用站点配置并重启Nginx：

```bash
sudo ln -s /etc/nginx/sites-available/masterflow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 生产环境部署建议

### 使用Gunicorn作为WSGI服务器

安装Gunicorn：

```bash
pip install gunicorn
```

创建启动脚本`start.sh`：

```bash
#!/bin/bash
cd /path/to/masterflow
source .venv/bin/activate
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

设置权限并执行：

```bash
chmod +x start.sh
./start.sh
```

### 设置Systemd服务

创建服务文件：

```bash
sudo nano /etc/systemd/system/masterflow.service
```

添加以下内容：

```ini
[Unit]
Description=MasterFlow API Service
After=network.target

[Service]
User=your_user
Group=your_group
WorkingDirectory=/path/to/masterflow
ExecStart=/path/to/masterflow/.venv/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=on-failure
RestartSec=5s
Environment="PATH=/path/to/masterflow/.venv/bin"

[Install]
WantedBy=multi-user.target
```

启用并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable masterflow
sudo systemctl start masterflow
```

### 使用Supervisor管理进程

安装Supervisor：

```bash
sudo apt install -y supervisor
```

创建配置文件：

```bash
sudo nano /etc/supervisor/conf.d/masterflow.conf
```

添加以下内容：

```ini
[program:masterflow]
command=/path/to/masterflow/.venv/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
directory=/path/to/masterflow
user=your_user
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

重新加载Supervisor配置：

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start masterflow
```

## 数据库备份

### 自动备份脚本

创建备份脚本`backup.sh`：

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/masterflow_$DATE.sql"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u masterflow_user -p'your_password' masterflow > $BACKUP_FILE

# 压缩备份文件
gzip $BACKUP_FILE

# 删除30天前的备份
find $BACKUP_DIR -name "masterflow_*.sql.gz" -type f -mtime +30 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
```

设置权限并添加到crontab：

```bash
chmod +x backup.sh
crontab -e
```

添加定时任务，每天凌晨2点执行备份：

```
0 2 * * * /path/to/masterflow/backup.sh >> /path/to/masterflow/logs/backup.log 2>&1
```

## 监控

### 使用Prometheus和Grafana

1. 安装Prometheus插件：

```bash
pip install prometheus-fastapi-instrumentator
```

2. 在`app/main.py`中添加以下代码：

```python
from prometheus_fastapi_instrumentator import Instrumentator

# 在应用创建后添加
Instrumentator().instrument(app).expose(app)
```

3. 配置Prometheus以抓取指标：

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'masterflow'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
```

4. 设置Grafana仪表板以可视化指标

## 安全最佳实践

1. **永远保持依赖包更新**：
```bash
pip install -U pip
pip install -U -r requirements.txt
```

2. **使用HTTPS**：
   - 在Nginx中配置SSL证书
   - 可以使用Let's Encrypt提供的免费证书

3. **安全环境变量**：
   - 不要在代码中硬编码敏感信息
   - 确保`.env`文件不会被提交到版本控制
   - 定期轮换密钥和密码

4. **限制数据库访问**：
   - 数据库用户只应具有必要的权限
   - 限制数据库仅接受本地连接

5. **启用防火墙**：
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
```

## 故障排除

### 常见问题

1. **数据库连接问题**
   - 检查数据库凭据是否正确
   - 确认MySQL服务是否运行
   - 检查防火墙设置

2. **应用无法启动**
   - 检查日志文件中的错误信息
   - 验证所有依赖包是否正确安装
   - 确认环境变量配置正确

3. **性能问题**
   - 检查数据库索引是否正确设置
   - 考虑增加Gunicorn工作进程数
   - 监控内存使用情况，可能需要更多资源

### 日志查看

主要日志位置：
- 应用日志：`logs/app.log`
- Uvicorn日志：标准输出或Systemd日志
- Nginx日志：`/var/log/nginx/`

查看系统服务日志：
```bash
sudo journalctl -u masterflow.service -f
```

## 升级指南

1. 备份数据库
```bash
./backup.sh
```

2. 更新代码
```bash
git pull origin main
```

3. 更新依赖
```bash
source .venv/bin/activate
pip install -U -r requirements.txt
```

4. 执行数据库迁移（如果有）
```bash
# 假设使用了某种迁移工具
# alembic upgrade head
```

5. 重启服务
```bash
sudo systemctl restart masterflow
# 或
sudo supervisorctl restart masterflow
```

## 联系与支持

如有部署问题，请联系系统管理员或通过以下渠道获取支持：

- 项目仓库Issue区
- 技术支持邮箱：support@example.com

---

注意：此部署文档基于系统当前版本，后续版本可能会有变更，请定期查看更新。 