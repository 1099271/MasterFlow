from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from app.models.llm_models import LlmNoteDiagnosis
from datetime import datetime
import json
from app.utils.logger import get_logger, info, warning, error

logger = get_logger(__name__)

class LlmDAO:
    """LLM数据访问对象"""
    
    @staticmethod
    def store_note_diagnosis(db: Session, note_id: str, llm_name: str, diagnosis_data: Dict[str, Any]) -> Optional[LlmNoteDiagnosis]:
        """存储笔记诊断结果"""
        try:
            # 检查是否已存在诊断记录
            diagnosis = db.query(LlmNoteDiagnosis).filter(
                LlmNoteDiagnosis.note_id == note_id
            ).first()
            
            # 准备数据
            keywords = diagnosis_data.get('keywords', {})
            user_data = diagnosis_data.get('data', {}).get('user', {})
            note_data = diagnosis_data.get('data', {}).get('note', {})
            
            if note_data.get('has_visited'):
                if isinstance(note_data.get('has_visited'), str):
                    has_visited = note_data.get('has_visited').lower() == "true"
                elif isinstance(note_data.get('has_visited'), bool):
                    has_visited = note_data.get('has_visited')
                else:
                    has_visited = False
            
            diagnosis_dict = {
                "note_id": note_id,
                "llm_name": llm_name,
                "geo_tags": json.dumps(keywords.get('location', []), ensure_ascii=False),
                "cultural_tags": json.dumps(keywords.get('culture', []), ensure_ascii=False),
                "other_tags": json.dumps(keywords.get('others', []), ensure_ascii=False),
                "user_gender": user_data.get('gendar'),
                "user_age_range": user_data.get('age_range'),
                "user_location": user_data.get('location'),
                "user_tags": json.dumps(user_data.get('others', []), ensure_ascii=False),
                "post_summary": json.dumps(note_data.get('instra', ''), ensure_ascii=False),
                "content_tendency": note_data.get('preference'),
                "content_tendency_reason": json.dumps(note_data.get('preference_reason', ''), ensure_ascii=False),
                "has_visited": has_visited,
                "diagnosed_at": datetime.now()
            }
            
            if not diagnosis:
                # 创建新记录
                diagnosis = LlmNoteDiagnosis(**diagnosis_dict)
                db.add(diagnosis)
                info(f"创建新的诊断记录: {note_id}")
            else:
                # 更新现有记录
                for key, value in diagnosis_dict.items():
                    setattr(diagnosis, key, value)
                diagnosis.updated_at = datetime.now()
                info(f"更新诊断记录: {note_id}")
            
            db.flush()
            db.commit()
            return diagnosis
            
        except Exception as e:
            db.rollback()
            error(f"存储诊断结果时出错: {str(e)}")
            return None