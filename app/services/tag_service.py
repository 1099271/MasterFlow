import json
import traceback
from typing import Dict, Any, List, Optional, Tuple, Type, TypeVar, Generic, Callable

from sentence_transformers import SentenceTransformer, util

from app.config.settings import settings
from app.database.db import get_db
from sqlalchemy import text
from app.services.llm_service import LlmService
from app.services.xhs_service import XhsService
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
            # llm_alias = "deepseek-r1:coze"
            llm_alias = "qwen-max:coze"
            if note_id:
                query = text("""
                    select d.note_id, d.note_display_title, d.note_desc
                    from xhs_note_details as d left join llm_note_diagnosis as l
                    on d.note_id = l.note_id and l.llm_name = :llm_alias
                    where d.note_desc != '' and d.note_desc is not null 
                    and d.note_create_time >= '2023-01-01'
                    and l.note_id is null
                    and d.note_id = :note_id
            """)
                result = db.execute(query, {"note_id": note_id, "llm_alias": llm_alias})
            else:
                query = text("""
                    select d.note_id, d.note_display_title, d.note_desc
                    from xhs_note_details as d left join llm_note_diagnosis as l
                    on d.note_id = l.note_id and l.llm_name = :llm_alias
                    where d.note_desc != '' and d.note_desc is not null 
                    and d.note_create_time >= '2023-01-01'
                    and l.note_id is null
                """)
                result = db.execute(query, {"llm_alias": llm_alias})
            
            notes = [(row[0], row[1], row[2]) for row in result]
            if len(notes) == 0:
                info("没有需要处理的数据")
                return []
            notes_length = len(notes)
            for index, (note_id, note_display_title, note_desc) in enumerate(notes):
                info(f"处理第 {index+1}/{notes_length} 条数据")
                try:
                    note_content = f"""【标题】：{note_display_title}
【描述】：{note_desc}"""
                    diagnosis_data = LlmService.request_llm(llm_alias=llm_alias, prompt=note_content, log_file_prefix="make_tags_from_note")
                    # diagnosis_data = TagService._req_coze_api(note_content=note_content, note_id=note_id)
                    success = LlmService.store_note_diagnosis(note_id=note_id, llm_alias=llm_alias, diagnosis_data=diagnosis_data)
                    if success:
                        info(f"{note_id} 更新成功")
                    else:
                        error(f"{note_id} 更新失败")
                except Exception as e:  
                    error(f"出错: {note_id} - {e}")
                    traceback.print_exc()
                
        except Exception as e:
            error(f"提取标签失败: {e}")
            raise e
        finally:
            db.close()
                
        return []
    
    @staticmethod
    def _req_coze_api(note_content: str, note_id: str):
        """
        处理coze的响应
        """
        # 调用coze api
        parameters = {
            "USER_INPUT": note_content,
            "CONVERSATION_NAME": note_id
        }
        result = XhsService._call_coze_api(
            workflow_id="7483469389816447014",
            parameters=parameters,
            log_file_prefix="make_tags_from_note"
        )
        # debug model
        # with open(f"logs/coze_http_request/make_tags_from_note/20250321/101508.json", "r", encoding="utf-8") as f:
        #     result = json.load(f)
        data_json = json.loads(result["data"])
        response_text = data_json["data"]
        if response_text.startswith("```json"):
            response_text = response_text.strip("```json").strip("```").strip()
        response_text = response_text.replace("False", "false")
        response_text = response_text.replace("True", "true")
        return json.loads(response_text)
    
    @staticmethod
    def similar_tag():
        model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
        # 示例标签
        tag1 = "护肤"
        tag2 = "美白精华"

        embedding1 = model.encode(tag1)
        embedding2 = model.encode(tag2)

        similarity = util.cos_sim(embedding1, embedding2).item()
        rich_print(similarity)
        return []