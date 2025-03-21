import json
import traceback
from typing import Dict, Any, List, Optional, Tuple, Type, TypeVar, Generic, Callable

import numpy as np
from sentence_transformers import SentenceTransformer, util

from app.config.settings import settings
from app.database.db import get_db
from sqlalchemy import text
from app.services.llm_service import LlmService
from app.services.tag_comparison.tag_similarity_analyzer import TagSimilarityAnalyzer
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
                    response_text = LlmService.request_llm(llm_alias=llm_alias, prompt=note_content, log_file_prefix="make_tags_from_note")
                    # response_text = TagService._req_coze_api(note_content=note_content, note_id=note_id)
                    response_text = response_text.replace("False", "false")
                    response_text = response_text.replace("True", "true")
                    diagnosis_data = json.loads(response_text)
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
        return response_text
    
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
    
    @staticmethod
    def analyse_tag_similarity():
        # 标准标签组
        standard_geo_tags = ["泸沽湖", "温泉村", "瓦拉壁", "云南", "丽江", "四川", "里格", "大落水", "摩梭村"]
        standard_cultural_tags = ["摩梭族", "走婚", "成丁礼", "成年礼", "阿妈", "阿乌", "格姆女神", "女权主义", "母系氏族", "大家庭", "藏传佛教", "民族服饰"]
        
        # 收集的标签示例
        geo_tags = ["泸沽湖", "云南风景", "丽江古城", "高原湖泊"]
        cultural_tags = ["摩梭文化", "母系社会", "走婚制度", "民族传统", "藏族文化"]
        
        # 创建分析器
        analyzer = TagSimilarityAnalyzer()
        
        # 分析各类标签组的相似度
        results = {}
        
        geo_result = analyzer.compare_tags(
            geo_tags,
            standard_geo_tags,
            visualize=True
        )
        
        cultural_result = analyzer.compare_tags(
            cultural_tags,
            standard_cultural_tags,
            visualize=True
        )
        
        # 打印结果
        print("\n=== 标签相似度分析结果 ===\n")
        
        print(f"相似度得分: {geo_result['score']:.2f}")
        print(f"解释: {analyzer.get_interpretation(geo_result['score'])}")
        print("\n详细得分:")
        for metric, score in geo_result['detailed_scores'].items():
            print(f"  - {metric}: {score:.2f}")
            print("\n收集标签:")
            print(", ".join(geo_result['collected_tags']))
            print("\n标准标签:")
            print(", ".join(geo_result['standard_tags']))
            print("\n" + "="*50 + "\n")
        
        # 计算总体相似度得分
        if geo_result:
            overall_score = np.mean([geo_result['score'] for geo_result in geo_result.values()])
            print(f"总体相似度得分: {overall_score:.2f}")
            print(f"总体解释: {analyzer.get_interpretation(overall_score)}")