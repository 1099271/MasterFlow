import logging
import sys
import os
import datetime
import colorama
from logging.handlers import RotatingFileHandler

# 初始化colorama以支持跨平台的彩色输出
colorama.init()

# 为不同日志级别定义颜色
COLORS = {
    'DEBUG': colorama.Fore.BLUE,
    'INFO': colorama.Fore.GREEN,
    'WARNING': colorama.Fore.YELLOW,
    'ERROR': colorama.Fore.RED,
    'CRITICAL': colorama.Fore.RED + colorama.Style.BRIGHT,
}

RESET = colorama.Style.RESET_ALL

class ColorFormatter(logging.Formatter):
    """
    自定义日志格式化器，用于添加颜色到控制台输出
    """
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        super().__init__(fmt, datefmt, style, validate)
        
    def format(self, record):
        """
        格式化日志记录，添加颜色代码
        """
        # 保存原始消息
        original_msg = record.msg
        # 获取对应级别的颜色
        color = COLORS.get(record.levelname, colorama.Fore.WHITE)
        # 添加颜色到消息
        record.msg = f"{color}{record.msg}{colorama.Style.RESET_ALL}"
        # 格式化记录
        formatted = super().format(record)
        # 恢复原始消息以避免影响文件日志
        record.msg = original_msg
        return formatted

def setup_logger(name='root', level='INFO', log_file_path=None):
    """
    设置日志配置
    
    Args:
        name: 日志名称
        level: 日志级别
        log_file_path: 日志文件路径
    """
    # 获取根日志器
    logger = logging.getLogger()
    
    # 清除现有的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 设置日志级别
    logger.setLevel(getattr(logging, level))
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level))
    
    # 设置彩色格式化器
    console_format = '%(asctime)s - %(levelname)s - %(message)s'
    console_handler.setFormatter(ColorFormatter(console_format))
    
    # 添加控制台处理器
    logger.addHandler(console_handler)
    
    # 如果指定了日志文件路径，添加文件处理器
    if log_file_path:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # 创建文件处理器(使用RotatingFileHandler支持文件轮换)
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, level))
        
        # 设置文件格式化器(不带颜色)
        file_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        file_handler.setFormatter(logging.Formatter(file_format))
        
        # 添加文件处理器
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name):
    """
    获取配置好的日志器
    
    Args:
        name: 日志器名称
    
    Returns:
        Logger: 配置好的日志器
    """
    return logging.getLogger(name)

# 便捷的日志记录函数
def debug(msg, *args, **kwargs):
    logging.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    logging.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    logging.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    logging.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    logging.critical(msg, *args, **kwargs)

# 初始化根日志器
root_logger = get_logger('root')

def debug(msg, *args, **kwargs):
    """Debug级别日志"""
    root_logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    """Info级别日志"""
    root_logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    """Warning级别日志"""
    root_logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    """Error级别日志"""
    root_logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    """Critical级别日志"""
    root_logger.critical(msg, *args, **kwargs) 