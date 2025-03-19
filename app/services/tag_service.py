import json
import traceback
import requests
import os
from typing import Dict, Any, List, Optional, Tuple, Type, TypeVar, Generic, Callable

from app.config.settings import settings
from app.models.xhs_dao import XhsDAO
from app.models.xhs_models import XhsSearchResponse, XhsNote, XhsAutherNotesResponse, XhsComment, XhsCommentsResponse, XhsNoteDetail, XhsNoteDetailResponse, XhsTopicDiscussion, XhsTopicsResponse
from app.services.xhs_service import XhsService
from app.database.db import get_db
from sqlalchemy import text
from app.utils.logger import get_logger, info, warning, error, debug

from rich import print as rich_print

logger = get_logger(__name__)

T = TypeVar('T')

class TagService:
    
    @staticmethod
    def get_tags_from_db():
        """
        查询数据库中的标签
        """
        return []
    
    @staticmethod
    def make_tags_from_note(note_id: str):
        """
        给指定的笔记提取标签

        Args:
            note_id (str): _description_
        """
        
        db = next(get_db())

        try:
            # 获取笔记详情
            if note_id:
                query = text("""
                    select note_id, note_display_title, note_desc
                    from xhs_note_details
                    where note_desc != '' and note_desc is not null 
                    and note_create_time >= '2024-01-01'
                    and note_id = :note_id
            """)
                result = db.execute(query, {"note_id": note_id})
            else:
                query = text("""
                    select note_id, note_display_title, note_desc
                    from xhs_note_details
                    where note_desc != '' and note_desc is not null 
                    and note_create_time >= '2024-01-01'
                """)
                result = db.execute(query)
            
            notes = [(row[0], row[1], row[2]) for row in result]
            if len(notes) == 0:
                info("没有需要处理的数据")
                return []
            
            for index, (note_id, note_display_title, note_desc) in enumerate(notes):
                info(f"处理第 {index} 条数据")
                try:
                    note_content = f"""【标题】：{note_display_title}
【描述】：{note_desc}"""
                    parameters = {
                        "USER_INPUT": note_content,
                        "CONVERSATION_NAME": note_id
                    }
                    # result = XhsService._call_coze_api(
                    #     workflow_id="7483469389816447014",
                    #     parameters=parameters,
                    #     log_file_prefix="make_tags_from_note"
                    # )
                    with open(f"logs/coze_http_request/make_tags_from_note/20250319/205306.json", "r", encoding="utf-8") as f:
                        result = json.load(f)
                    data_json = json.loads(result["data"])
                    response_text = data_json["data"]
                    cleaned_json_string = response_text.strip("```json").strip("```").strip()
                    response_json = json.loads(cleaned_json_string)
                    
                except Exception as e:  
                    error(f"出错: {note_id} - {e}")
                    traceback.print_exc()
                
        except Exception as e:
            error(f"提取标签失败: {e}")
            raise e
        finally:
            db.close()
                
        return []