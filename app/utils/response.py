from typing import Any, Optional, Dict
from fastapi import HTTPException
import logging
import traceback

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseBase:
    """统一响应基类"""
    @staticmethod
    def success(*, data: Any = None, msg: str = "操作成功") -> Dict[str, Any]:
        """成功响应"""
        return {
            "code": 0,
            "msg": msg,
            "data": data
        }
    
    @staticmethod
    def error(*, code: int = 500, msg: str = "操作失败", data: Any = None) -> Dict[str, Any]:
        """错误响应"""
        return {
            "code": code,
            "msg": msg,
            "data": data
        }

def handle_error(e: Exception, operation: str) -> None:
    """统一错误处理"""
    error_detail = f"{str(e)}\n{''.join(traceback.format_tb(e.__traceback__))}"
    logger.error(f"执行{operation}时发生错误: {error_detail}")
    if isinstance(e, HTTPException):
        raise e
    raise HTTPException(
        status_code=500,
        detail=ResponseBase.error(msg=f"执行{operation}时发生错误: {str(e)}")
    ) 