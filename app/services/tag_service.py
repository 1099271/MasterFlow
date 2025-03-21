import os
import json
import traceback
from typing import Dict, Any, List, Optional, Tuple, TypeVar, Generic, Callable

import numpy as np
from sentence_transformers import SentenceTransformer, util

from app.config.settings import settings
from app.database.db import get_db
from sqlalchemy import text
from app.services.llm_service import LlmService
from app.services.tag_comparison.tag_similarity_analyzer import TagSimilarityAnalyzer
from app.services.xhs_service import XhsService
from app.database.tag_dao import TagDAO
from app.utils.logger import get_logger, info, warning, error, debug

from rich import print as rich_print

os.environ['NUMEXPR_MAX_THREADS'] = '16'
logger = get_logger(__name__)

T = TypeVar('T')

class TagService:
    def __init__(self, model_name='distiluse-v2'):
        """
        初始化标签服务
        
        Args:
            model_name: 使用的预训练模型名称，可选值：'distiluse-v2', 'bge'
        """
        self.analyzer = TagSimilarityAnalyzer(model_name=model_name)
        self.tag_dao = TagDAO()
    
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
    
    def compare_and_save_tags(self, note_id: str, llm_name: str, collected_tags: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        比较标签并保存结果
        
        Args:
            note_id: 笔记ID
            llm_name: LLM模型名称
            collected_tags: 收集到的标签，格式为 {"geo": [...], "cultural": [...]}
            
        Returns:
            包含各类标签对比结果的字典
        """
        results = {}
        db = next(get_db())
        
        try:
            for tag_type, tags in collected_tags.items():
                # 获取标准标签
                standard_tags = self.tag_dao.get_standard_tags(tag_type)
                
                # 进行标签对比
                comparison_result = self.analyzer.compare_tags(
                    collected_tags=tags,
                    standard_tags=standard_tags,
                    visualize=False
                )
                
                # 保存结果到数据库
                scores = comparison_result.get('detailed_scores', {})
                success = self.tag_dao.save_comparison_result(
                    db=db,
                    note_id=note_id,
                    llm_name=llm_name,
                    tag_type=tag_type,
                    collected_tags=comparison_result.get('collected_tags', []),
                    standard_tags=comparison_result.get('standard_tags', []),
                    similarity_matrix=comparison_result.get('similarity_matrix', np.array([[0]])).tolist(),
                    scores={
                        'max_similarity': scores.get('max_similarity', 0.0),
                        'optimal_matching': scores.get('optimal_matching', 0.0),
                        'threshold_matching': scores.get('threshold_matching', 0.0),
                        'average_similarity': scores.get('average_similarity', 0.0),
                        'coverage': scores.get('coverage', 0.0)
                    },
                    weighted_score=comparison_result.get('score', 0),
                    interpretation=self.analyzer.get_interpretation(comparison_result.get('score', 0)),
                    compare_model_name=self.analyzer.model_name
                )
                
                if not success:
                    raise Exception(f"保存标签对比结果失败: {note_id} - {tag_type}")
                
                results[tag_type] = comparison_result
            
            return results
        finally:
            db.close()
    
    def get_tag_comparison_results(self, note_id: str, llm_name: str = None) -> List[Dict[str, Any]]:
        """
        获取笔记的标签对比结果
        
        Args:
            note_id: 笔记ID
            llm_name: 可选的LLM模型名称过滤
            
        Returns:
            标签对比结果列表
        """
        return self.tag_dao.get_comparison_results(note_id, llm_name)
    
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
    
    def similar_tag(self):
        """给标签做相似度匹配"""
        # 示例标签
        tag1 = "护肤"
        tag2 = "美白精华"

        # 使用当前实例的 analyzer 进行编码
        embedding1 = self.analyzer.model.encode(tag1)
        embedding2 = self.analyzer.model.encode(tag2)

        similarity = util.cos_sim(embedding1, embedding2).item()
        rich_print(similarity)
    
    def analyse_tag_similarity(self, note_id: str = None, llm_name: str = None):
        """
        分析标签相似度并存储结果
        
        Args:
            note_id (str, optional): 指定笔记ID，如果为None则分析所有未分析的笔记
            llm_name (str, optional): 指定LLM模型名称进行过滤
        """
        db = next(get_db())
        try:
            # 查询需要分析的笔记
            if note_id:
                query = text("""
                    SELECT d.note_id, l.llm_name, 
                           l.geo_tags, l.cultural_tags
                    FROM llm_note_diagnosis l
                    JOIN xhs_note_details d ON l.note_id = d.note_id
                    LEFT JOIN tag_comparison_results t 
                        ON l.note_id = t.note_id 
                        AND l.llm_name = t.llm_name
                    WHERE d.note_id = :note_id
                    -- AND t.id IS NULL
                """)
                result = db.execute(query, {"note_id": note_id})
            else:
                query = text("""
                    SELECT d.note_id, l.llm_name, 
                           l.geo_tags, l.cultural_tags
                    FROM llm_note_diagnosis l
                    JOIN xhs_note_details d ON l.note_id = d.note_id
                    LEFT JOIN tag_comparison_results t 
                        ON l.note_id = t.note_id 
                        AND l.llm_name = t.llm_name
                    WHERE t.id IS NULL
                    AND (:llm_name IS NULL OR l.llm_name = :llm_name)
                """)
                result = db.execute(query, {"llm_name": llm_name})
            
            notes = [(row[0], row[1], json.loads(row[2]) if row[2] else [], 
                     json.loads(row[3]) if row[3] else []) for row in result]
            
            if not notes:
                info("没有需要分析的笔记")
                return
            
            total = len(notes)
            for idx, (note_id, llm_name, geo_tags, cultural_tags) in enumerate(notes, 1):
                info(f"正在处理 {idx}/{total}: {note_id} - {llm_name}")
                
                # 处理可能的字符串列表问题
                if isinstance(geo_tags, str):
                    try:
                        geo_tags = json.loads(geo_tags)
                    except:
                        # 如果是一个字符串，尝试将其转换为列表
                        geo_tags = [tag.strip() for tag in geo_tags.strip('[]').replace('"', '').split(',') if tag.strip()]
                
                if isinstance(cultural_tags, str):
                    try:
                        cultural_tags = json.loads(cultural_tags)
                    except:
                        # 如果是一个字符串，尝试将其转换为列表
                        cultural_tags = [tag.strip() for tag in cultural_tags.strip('[]').replace('"', '').split(',') if tag.strip()]
                
                try:
                    # 准备标签数据
                    collected_tags = {
                        "geo": geo_tags,
                        "cultural": cultural_tags
                    }
                    
                    # 执行对比并保存
                    results = self.compare_and_save_tags(
                        note_id=note_id,
                        llm_name=llm_name,
                        collected_tags=collected_tags
                    )
                    
                    # 打印分析结果
                    print(f"\n=== {note_id} 标签相似度分析结果 ===")
                    for tag_type, result in results.items():
                        print(f"\n【{tag_type}】")
                        print(f"相似度得分: {result['score']:.2f}")
                        print(f"解释: {self.analyzer.get_interpretation(result['score'])}")
                        print("\n收集标签:", ", ".join(result['collected_tags']))
                        print("标准标签:", ", ".join(result['standard_tags']))
                        print("\n详细得分:")
                        for metric, score in result['detailed_scores'].items():
                            print(f"  - {metric}: {score:.2f}")
                        print("="*50)
                    
                except Exception as e:
                    error(f"处理笔记 {note_id} 时出错: {str(e)}")
                    traceback.print_exc()
                    continue
                
        except Exception as e:
            error(f"标签分析过程出错: {str(e)}")
            traceback.print_exc()
        finally:
            db.close()
            
    def init_standard_tags(self):
        """初始化标准标签到数据库"""
        standard_tags = {
            "geo": [
                "泸沽湖", "温泉村", "瓦拉壁", "云南", "丽江", 
                "四川", "里格", "大落水", "摩梭村"
            ],
            "cultural": [
                "摩梭族", "走婚", "成丁礼", "成年礼", "阿妈", 
                "阿乌", "格姆女神", "女权主义", "母系氏族", 
                "大家庭", "藏传佛教", "民族服饰"
            ]
        }
        
        db = next(get_db())
        try:
            for tag_type, tags in standard_tags.items():
                for tag_name in tags:
                    success = self.tag_dao.save_standard_tag(
                        db=db,
                        tag_name=tag_name,
                        tag_type=tag_type
                    )
                    if not success:
                        raise Exception(f"保存标准标签失败: {tag_name}")
            db.commit()
            info("标准标签初始化完成")
        except Exception as e:
            error(f"标准标签初始化失败: {str(e)}")
            db.rollback()
        finally:
            db.close()