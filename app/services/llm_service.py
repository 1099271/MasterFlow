from typing import Optional, Dict, Any
from app.models.llm_dao import LlmDAO
from app.database.db import get_db
from app.utils.logger import get_logger, info, error

logger = get_logger(__name__)

class LlmService:
    """LLM服务类"""
    
    @staticmethod
    def store_note_diagnosis(note_id: str, llm_alias: str, diagnosis_data: Dict[str, Any]) -> bool:
        """
        存储笔记诊断结果
        
        Args:
            note_id: 笔记ID
            llm_alias: 模型名称
            diagnosis_data: 诊断数据
            
        Returns:
            bool: 是否成功
        """
        try:
            db = next(get_db())
            
            # 存储诊断结果
            diagnosis = LlmDAO.store_note_diagnosis(
                db=db,
                note_id=note_id,
                llm_name=llm_alias,
                diagnosis_data=diagnosis_data
            )
            
            return diagnosis is not None
            
        except Exception as e:
            error(f"存储笔记诊断结果时出错: {str(e)}")
            return False