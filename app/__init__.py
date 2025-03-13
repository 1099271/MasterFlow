# MasterFlow API应用程序
# 版本: 1.0.0 

import os
from app.utils.logger import setup_logger

# 设置日志配置
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

# 初始化日志配置
setup_logger(
    name="root",
    level="INFO",
    log_file_path=os.path.join(log_dir, "app.log")
) 