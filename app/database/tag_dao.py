from typing import List, Dict, Any, Optional
import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db import get_db
from app.models.tag_models import TagStandard, TagComparisonResult
from app.utils.logger import get_logger, error

logger = get_logger(__name__)

class TagDAO:
    @staticmethod
    def get_standard_tags(tag_type: str) -> List[str]:
        """获取指定类型的标准标签列表"""
        db = next(get_db())
        try:
            query = select(TagStandard.tag_name).where(TagStandard.tag_type == tag_type)
            result = db.execute(query)
            return [row[0] for row in result]
        finally:
            db.close()
    
    @staticmethod
    def save_standard_tag(db: Session, tag_name: str, tag_type: str) -> bool:
        """保存标准标签"""
        try:
            db_tag = TagStandard(
                tag_name=tag_name,
                tag_type=tag_type
            )
            db.add(db_tag)
            return True
        except Exception as e:
            error(f"保存标准标签失败: {str(e)}")
            return False
    
    @staticmethod
    def save_comparison_result(
        db: Session,
        note_id: str,
        llm_name: str,
        tag_type: str,
        collected_tags: List[str],
        standard_tags: List[str],
        similarity_matrix: List[List[float]],
        scores: Dict[str, float],
        weighted_score: float,
        interpretation: str,
        compare_model_name: str = "distiluse-base-multilingual-cased-v2"
    ) -> bool:
        """保存标签对比结果，如果已存在则更新"""
        try:
            # 查找是否已存在记录
            query = db.query(TagComparisonResult).filter(
                TagComparisonResult.note_id == note_id,
                TagComparisonResult.llm_name == llm_name,
                TagComparisonResult.tag_type == tag_type,
                TagComparisonResult.compare_model_name == compare_model_name
            )
            existing_result = query.first()
            
            result_dict = {
                "note_id": note_id,
                "llm_name": llm_name,
                "tag_type": tag_type,
                "compare_model_name": compare_model_name,
                "collected_tags": json.dumps(collected_tags, ensure_ascii=False),
                "standard_tags": json.dumps(standard_tags, ensure_ascii=False),
                "similarity_matrix": json.dumps(similarity_matrix, ensure_ascii=False),
                "max_similarity": float(scores['max_similarity']),
                "optimal_matching": float(scores['optimal_matching']),
                "threshold_matching": float(scores['threshold_matching']),
                "average_similarity": float(scores['average_similarity']),
                "coverage": float(scores['coverage']),
                "weighted_score": float(weighted_score),
                "interpretation": interpretation
            }
            
            if existing_result:
                # 更新现有记录
                for key, value in result_dict.items():
                    setattr(existing_result, key, value)
                existing_result.updated_at = datetime.now()
                db.flush()
                db.commit()
            else:
                # 创建新记录
                db_result = TagComparisonResult(**result_dict)
                db.add(db_result)
                db.commit()
                
            return True
        except Exception as e:
            error(f"保存对比结果失败: {str(e)}")
            db.rollback()
            return False
    
    @staticmethod
    def get_comparison_results(
        note_id: str,
        llm_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """获取笔记的标签对比结果"""
        db = next(get_db())
        try:
            query = select(TagComparisonResult).where(
                TagComparisonResult.note_id == note_id
            )
            if llm_name:
                query = query.where(TagComparisonResult.llm_name == llm_name)
            
            results = db.execute(query).scalars().all()
            return [result.__dict__ for result in results]
        finally:
            db.close() 